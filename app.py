from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
import requests
import time
from werkzeug.utils import secure_filename

from modules.qr_scanner import decode_qr, detect_qr_type
from modules.url_verification import verify_url
from modules.risk_analyzer import analyze_risk


# =========================================================
# APP CONFIGURATION
# =========================================================

app = Flask(__name__)

app.secret_key = "truescan_secret_key"

DATABASE = os.path.join(
    app.root_path,
    "truescan.db"
)

VIRUSTOTAL_API_KEY = os.environ.get(
    "VIRUSTOTAL_API_KEY"
)

VT_HEADERS = {
    "x-apikey": VIRUSTOTAL_API_KEY
} if VIRUSTOTAL_API_KEY else {}


# =========================================================
# DATABASE
# =========================================================

def get_db():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_db()

    # USERS
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'User'
        )
    """)

    # HISTORY
    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            scan_type TEXT,
            value TEXT,
            result TEXT,
            score INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # REPORTS
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            url TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # DEFAULT ADMIN
    admin = conn.execute(
        """
        SELECT *
        FROM users
        WHERE email=?
        """,
        ("admin@truscan.com",)
    ).fetchone()

    if not admin:

        conn.execute("""
            INSERT INTO users
            (name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, (
            "Administrator",
            "admin@truscan.com",
            "1234",
            "Administrator"
        ))

    conn.commit()

    conn.close()


# =========================================================
# VIRUSTOTAL
# =========================================================

def check_virustotal(url):

    if not VIRUSTOTAL_API_KEY:

        return {
            "available": False,
            "malicious": 0,
            "suspicious": 0,
            "harmless": 0,
            "undetected": 0,
            "message": "VirusTotal API key is not loaded."
        }

    try:

        # Submit URL to VirusTotal
        response = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=VT_HEADERS,
            data={
                "url": url
            },
            timeout=20
        )

        if response.status_code not in (200, 201):

            print(
                "VirusTotal submit error:",
                response.status_code,
                response.text[:300]
            )

            return {
                "available": False,
                "malicious": 0,
                "suspicious": 0,
                "harmless": 0,
                "undetected": 0,
                "message": "VirusTotal URL submission failed."
            }

        data = response.json()

        analysis_id = data.get(
            "data",
            {}
        ).get(
            "id"
        )

        if not analysis_id:

            return {
                "available": False,
                "malicious": 0,
                "suspicious": 0,
                "harmless": 0,
                "undetected": 0,
                "message": "VirusTotal analysis ID was not received."
            }

        # Wait for analysis
        analysis_url = (
            "https://www.virustotal.com/api/v3/analyses/"
            + analysis_id
        )

        analysis_data = None

        for _ in range(5):

            time.sleep(2)

            result_response = requests.get(
                analysis_url,
                headers=VT_HEADERS,
                timeout=20
            )

            if result_response.status_code != 200:

                continue

            analysis_data = result_response.json()

            status = (
                analysis_data
                .get("data", {})
                .get("attributes", {})
                .get("status")
            )

            if status == "completed":

                break

        if not analysis_data:

            return {
                "available": False,
                "malicious": 0,
                "suspicious": 0,
                "harmless": 0,
                "undetected": 0,
                "message": "VirusTotal analysis result unavailable."
            }

        attributes = (
            analysis_data
            .get("data", {})
            .get("attributes", {})
        )

        stats = attributes.get(
            "stats",
            {}
        )

        malicious = int(
            stats.get("malicious", 0)
        )

        suspicious = int(
            stats.get("suspicious", 0)
        )

        harmless = int(
            stats.get("harmless", 0)
        )

        undetected = int(
            stats.get("undetected", 0)
        )

        return {
            "available": True,
            "malicious": malicious,
            "suspicious": suspicious,
            "harmless": harmless,
            "undetected": undetected,
            "message": "VirusTotal analysis completed."
        }

    except requests.RequestException as e:

        print(
            "VirusTotal connection error:",
            e
        )

        return {
            "available": False,
            "malicious": 0,
            "suspicious": 0,
            "harmless": 0,
            "undetected": 0,
            "message": "VirusTotal could not be reached."
        }

    except Exception as e:

        print(
            "VirusTotal error:",
            e
        )

        return {
            "available": False,
            "malicious": 0,
            "suspicious": 0,
            "harmless": 0,
            "undetected": 0,
            "message": "VirusTotal analysis failed."
        }


# =========================================================
# COMBINE LOCAL + VIRUSTOTAL ANALYSIS
# =========================================================

def perform_security_analysis(content):

    try:

        # Local URL verification
        url_result = verify_url(
            content
        )

    except Exception as e:

        print(
            "URL VERIFICATION ERROR:",
            e
        )

        url_result = {}

    try:

        # Existing local risk analyzer
        risk_result = analyze_risk(
            url_result
        )

    except Exception as e:

        print(
            "RISK ANALYZER ERROR:",
            e
        )

        risk_result = {
            "score": 0,
            "status": "Information",
            "reasons": []
        }

    try:

        local_score = int(
            risk_result.get(
                "score",
                0
            )
        )

    except:

        local_score = 0

    local_status = risk_result.get(
        "status",
        "Information"
    )

    reasons = risk_result.get(
        "reasons",
        []
    )

    if not isinstance(reasons, list):

        reasons = [
            str(reasons)
        ]

    # -----------------------------------------------------
    # VirusTotal only for HTTP/HTTPS URLs
    # -----------------------------------------------------

    is_url = (
        content.lower().startswith("http://")
        or
        content.lower().startswith("https://")
    )

    vt_result = {
        "available": False,
        "malicious": 0,
        "suspicious": 0,
        "harmless": 0,
        "undetected": 0,
        "message": "VirusTotal check not required."
    }

    if is_url:

        vt_result = check_virustotal(
            content
        )

    # -----------------------------------------------------
    # Combine Results
    # -----------------------------------------------------

    final_score = local_score

    if vt_result["available"]:

        malicious = vt_result["malicious"]

        suspicious = vt_result["suspicious"]

        # Increase score according to VT findings
        if malicious > 0:

            final_score = max(
                final_score,
                min(
                    100,
                    70 + malicious * 5
                )
            )

            reasons.append(
                f"VirusTotal detected "
                f"{malicious} malicious security engine result(s)."
            )

        elif suspicious > 0:

            final_score = max(
                final_score,
                min(
                    100,
                    40 + suspicious * 5
                )
            )

            reasons.append(
                f"VirusTotal reported "
                f"{suspicious} suspicious security engine result(s)."
            )

        else:

            reasons.append(
                "VirusTotal did not report malicious detections."
            )

    # Keep score between 0 and 100
    final_score = max(
        0,
        min(
            100,
            int(final_score)
        )
    )

    # -----------------------------------------------------
    # Final Status
    # -----------------------------------------------------

    if final_score >= 70:

        final_status = "High Risk"

    elif final_score >= 40:

        final_status = "Medium Risk"

    else:

        final_status = "Low Risk"

    if not reasons:

        if final_status == "High Risk":

            reasons.append(
                "The submitted content shows high-risk indicators."
            )

        elif final_status == "Medium Risk":

            reasons.append(
                "The submitted content contains suspicious indicators."
            )

        else:

            reasons.append(
                "No major security risk was detected."
            )

    return {
        "score": final_score,
        "status": final_status,
        "reasons": reasons,
        "virustotal": vt_result
    }


# =========================================================
# SAVE HISTORY
# =========================================================

def save_history(
    scan_type,
    value,
    result,
    score
):

    try:

        conn = get_db()

        conn.execute("""
            INSERT INTO history
            (user_email, scan_type, value, result, score)
            VALUES (?, ?, ?, ?, ?)
        """, (
            session.get("email"),
            scan_type,
            value,
            result,
            score
        ))

        conn.commit()

        conn.close()

    except Exception as e:

        print(
            "HISTORY ERROR:",
            e
        )


# =========================================================
# SPLASH
# =========================================================

@app.route("/")
def splash():

    return render_template(
        "splash.html"
    )


# =========================================================
# NORMAL LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        conn = get_db()

        user = conn.execute("""
            SELECT *
            FROM users
            WHERE email=?
            AND password=?
        """, (
            email,
            password
        )).fetchone()

        conn.close()

        if user:

            session["email"] = user["email"]

            session["name"] = user["name"]

            session["role"] = user["role"]

            if user["role"] == "Administrator":

                return redirect(
                    url_for("admin")
                )

            return redirect(
                url_for("dashboard")
            )

        return render_template(
            "login.html",
            error="Invalid email or password"
        )

    return render_template(
        "login.html"
    )


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route(
    "/admin-login",
    methods=["GET", "POST"]
)
def admin_login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        conn = get_db()

        admin_user = conn.execute("""
            SELECT *
            FROM users
            WHERE email=?
            AND password=?
            AND role='Administrator'
        """, (
            email,
            password
        )).fetchone()

        conn.close()

        if admin_user:

            session["email"] = admin_user["email"]

            session["name"] = admin_user["name"]

            session["role"] = "Administrator"

            return redirect(
                url_for("admin")
            )

        return render_template(
            "login.html",
            error="Invalid administrator credentials"
        )

    return render_template(
        "login.html"
    )


# =========================================================
# REGISTER
# =========================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            request.form.get(
                "confirm",
                ""
            )
        )

        if not name:

            name = (
                email.split("@")[0]
                if email
                else "User"
            )

        if not email or not password:

            return render_template(
                "register.html",
                message="Please fill all required fields"
            )

        if password != confirm_password:

            return render_template(
                "register.html",
                message="Passwords do not match"
            )

        try:

            conn = get_db()

            conn.execute("""
                INSERT INTO users
                (name, email, password, role)
                VALUES (?, ?, ?, ?)
            """, (
                name,
                email,
                password,
                "User"
            ))

            conn.commit()

            conn.close()

            return redirect(
                url_for("login")
            )

        except sqlite3.IntegrityError:

            return render_template(
                "register.html",
                message="Email already registered"
            )

    return render_template(
        "register.html"
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if "email" not in session:

        return redirect(
            url_for("login")
        )

    return render_template(
        "dashboard.html",
        name=session.get(
            "name",
            "User"
        ),
        email=session.get(
            "email",
            ""
        )
    )


# =========================================================
# QR CAMERA PAGE
# =========================================================

@app.route("/qr_camera")
def qr_camera():

    if "email" not in session:

        return redirect(
            url_for("login")
        )

    return render_template(
        "qr_camera.html"
    )


# =========================================================
# CAMERA QR ANALYSIS
# =========================================================

@app.route(
    "/analyze-qr",
    methods=["POST"]
)
def analyze_qr():

    if "email" not in session:

        return redirect(
            url_for("login")
        )

    decoded_text = ""

    # FORM DATA
    if request.form:

        decoded_text = request.form.get(
            "qr_data",
            ""
        ).strip()

    # JSON DATA
    if not decoded_text and request.is_json:

        data = request.get_json(
            silent=True
        )

        if data:

            decoded_text = str(
                data.get(
                    "qr_data",
                    ""
                )
            ).strip()

    if not decoded_text:

        return render_template(
            "result.html",
            result="No QR data received.",
            qr_type="Unknown",
            score=0,
            status="Information",
            reasons=[
                "The QR code could not be analyzed."
            ],
            virustotal={
                "available": False
            }
        )

    try:

        # Detect QR type
        try:

            qr_type = detect_qr_type(
                decoded_text
            )

        except:

            qr_type = "Unknown"

        # Security analysis
        analysis = perform_security_analysis(
            decoded_text
        )

        score = analysis["score"]

        status = analysis["status"]

        reasons = analysis["reasons"]

        vt_result = analysis["virustotal"]

        # Save
        save_history(
            "QR Camera",
            decoded_text,
            status,
            score
        )

        return render_template(
            "result.html",
            result=decoded_text,
            qr_type=qr_type,
            score=score,
            status=status,
            reasons=reasons,
            virustotal=vt_result
        )

    except Exception as e:

        print(
            "CAMERA QR ERROR:",
            e
        )

        return render_template(
            "result.html",
            result=decoded_text,
            qr_type="Unknown",
            score=0,
            status="Unable to Analyze",
            reasons=[
                "An error occurred while analyzing the QR code."
            ],
            virustotal={
                "available": False
            }
        )


# =========================================================
# QR IMAGE UPLOAD
# =========================================================

@app.route(
    "/qr-upload",
    methods=["GET", "POST"]
)
def qr_upload():

    if "email" not in session:

        return redirect(
            url_for("login")
        )

    if request.method == "POST":

        qr_image = request.files.get(
            "qr_image"
        )

        if not qr_image:

            return render_template(
                "qr_upload.html",
                error="Please select a QR image."
            )

        if not qr_image.filename:

            return render_template(
                "qr_upload.html",
                error="Please select a valid QR image."
            )

        try:

            upload_folder = os.path.join(
                app.root_path,
                "uploads",
                "qr_images"
            )

            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            filename = secure_filename(
                qr_image.filename
            )

            if not filename:

                return render_template(
                    "qr_upload.html",
                    error="Invalid image filename."
                )

            file_path = os.path.join(
                upload_folder,
                filename
            )

            qr_image.save(
                file_path
            )

            # REAL QR DECODING
            qr_result = decode_qr(
                file_path
            )

            if not qr_result.get(
                "success",
                False
            ):

                return render_template(
                    "qr_upload.html",
                    error=qr_result.get(
                        "message",
                        "QR code could not be decoded."
                    )
                )

            decoded_text = qr_result.get(
                "data",
                ""
            )

            if not decoded_text:

                return render_template(
                    "qr_upload.html",
                    error="No QR data was detected."
                )

            qr_type = qr_result.get(
                "type",
                "Unknown"
            )

            # Security analysis
            analysis = perform_security_analysis(
                decoded_text
            )

            score = analysis["score"]

            status = analysis["status"]

            reasons = analysis["reasons"]

            vt_result = analysis["virustotal"]

            # Save history
            save_history(
                "QR Image",
                decoded_text,
                status,
                score
            )

            return render_template(
                "result.html",
                result=decoded_text,
                qr_type=qr_type,
                score=score,
                status=status,
                reasons=reasons,
                virustotal=vt_result
            )

        except Exception as e:

            print(
                "QR UPLOAD ERROR:",
                e
            )

            return render_template(
                "qr_upload.html",
                error="Unable to analyze this QR image."
            )

    return render_template(
        "qr_upload.html"
    )


# =========================================================
# LINK CHECKER
# =========================================================

@app.route(
    "/link-checker",
    methods=["GET", "POST"]
)
def link_checker():

    if "email" not in session:

        return redirect(
            url_for("login")
        )

    if request.method == "POST":

        url = request.form.get(
            "url",
            ""
        ).strip()

        if not url:

            return render_template(
                "link_checker.html",
                error="Please enter a URL."
            )

        try:

            # Security analysis
            analysis = perform_security_analysis(
                url
            )

            score = analysis["score"]

            status = analysis["status"]

            reasons = analysis["reasons"]

            vt_result = analysis["virustotal"]

            # Save history
            save_history(
                "Link",
                url,
                status,
                score
            )

            return render_template(
                "result.html",
                result=url,
                qr_type="Website / URL",
                score=score,
                status=status,
                reasons=reasons,
                virustotal=vt_result
            )

        except Exception as e:

            print(
                "LINK ERROR:",
                e
            )

            return render_template(
                "link_checker.html",
                error="Unable to analyze this link."
            )

    return render_template(
        "link_checker.html"
    )


# =========================================================
# HISTORY
# =========================================================

@app.route("/history")
def history():

    if "email" not in session:

        return redirect(
            url_for("login")
        )

    conn = get_db()

    records = conn.execute("""
        SELECT *
        FROM history
        WHERE user_email=?
        ORDER BY id DESC
    """, (
        session["email"],
    )).fetchall()

    conn.close()

    return render_template(
        "history.html",
        records=records
    )


# =========================================================
# PROFILE
# =========================================================

@app.route("/profile")
def profile():

    if "email" not in session:

        return redirect(
            url_for("login")
        )

    conn = get_db()

    user = conn.execute(
        """
        SELECT *
        FROM users
        WHERE email=?
        """,
        (
            session["email"],
        )
    ).fetchone()

    conn.close()

    return render_template(
        "profile.html",
        user=user
    )


# =========================================================
# REPORT
# =========================================================

@app.route(
    "/report",
    methods=["GET", "POST"]
)
def report():

    if "email" not in session:

        return redirect(
            url_for("login")
        )

    if request.method == "POST":

        category = request.form.get(
            "category",
            ""
        )

        url = request.form.get(
            "url",
            ""
        )

        message = request.form.get(
            "message",
            ""
        )

        conn = get_db()

        conn.execute("""
            INSERT INTO reports
            (category, url, message)
            VALUES (?, ?, ?)
        """, (
            category,
            url,
            message
        ))

        conn.commit()

        conn.close()

        return render_template(
            "report.html",
            success="Scam report submitted successfully!"
        )

    return render_template(
        "report.html"
    )


# =========================================================
# ADMIN PANEL
# =========================================================

@app.route("/admin")
def admin():

    if "email" not in session:

        return redirect(
            url_for("login")
        )

    if session.get(
        "role"
    ) != "Administrator":

        return redirect(
            url_for("dashboard")
        )

    conn = get_db()

    users = conn.execute("""
        SELECT *
        FROM users
        ORDER BY id DESC
    """).fetchall()

    reports = conn.execute("""
        SELECT *
        FROM reports
        ORDER BY id DESC
    """).fetchall()

    total_users = conn.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    total_scans = conn.execute(
        "SELECT COUNT(*) FROM history"
    ).fetchone()[0]

    total_reports = conn.execute(
        "SELECT COUNT(*) FROM reports"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "admin.html",
        users=users,
        reports=reports,
        total_users=total_users,
        total_scans=total_scans,
        total_reports=total_reports
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    init_db()

    print("")
    print("===================================")
    print("       TRUESCAN SERVER STARTED")
    print("===================================")
    print("VirusTotal API:",
          "LOADED" if VIRUSTOTAL_API_KEY else "NOT LOADED")
    print("Open: http://127.0.0.1:5000")
    print("===================================")
    print("")

    app.run(
        host="127.0.0.1",
        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        ),
        debug=True
    )
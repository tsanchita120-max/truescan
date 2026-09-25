from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

from modules.qr_scanner import decode_qr, detect_qr_type
from modules.url_verification import verify_url
from modules.risk_analyzer import analyze_risk


app = Flask(__name__)
app.secret_key = "truescan_secret_key"

DATABASE = "truescan.db"


# ================= DATABASE =================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'User'
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            url TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

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

    # DEFAULT ADMIN
    admin = conn.execute(
        "SELECT * FROM users WHERE email=?",
        ("admin@truscan.com",)
    ).fetchone()

    if not admin:

        conn.execute("""
            INSERT INTO users
            (name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, (
            "Admin",
            "admin@truscan.com",
            "1234",
            "Administrator"
        ))

    conn.commit()
    conn.close()


# ================= SPLASH =================

@app.route("/")
def splash():
    return render_template("splash.html")


# ================= LOGIN =================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        conn = get_db()

        user = conn.execute("""
            SELECT *
            FROM users
            WHERE email=? AND password=?
        """, (email, password)).fetchone()

        conn.close()

        if user:

            session["email"] = user["email"]
            session["name"] = user["name"]
            session["role"] = user["role"]

            if user["role"] == "Administrator":
                return redirect(url_for("admin"))

            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid email or password"
        )

    return render_template("login.html")


# ================= REGISTER =================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        confirm_password = request.form.get(
            "confirm_password",
            request.form.get("confirm", "")
        )

        if not name:
            name = email.split("@")[0] if email else "User"

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

            return redirect(url_for("login"))

        except sqlite3.IntegrityError:

            return render_template(
                "register.html",
                message="Email already registered"
            )

    return render_template("register.html")


# ================= DASHBOARD =================

@app.route("/dashboard")
def dashboard():

    if "email" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        name=session.get("name", "User"),
        email=session.get("email", "")
    )


# ================= QR CAMERA PAGE =================

@app.route("/qr_camera")
def qr_camera():

    if "email" not in session:
        return redirect(url_for("login"))

    return render_template("qr_camera.html")


# ================= QR CAMERA ANALYSIS =================

@app.route("/analyze-qr", methods=["POST"])
def analyze_qr():

    if "email" not in session:
        return {
            "success": False,
            "message": "Please login first."
        }

    data = request.get_json()

    if not data or not data.get("qr_data"):

        return {
            "success": False,
            "message": "No QR data received."
        }

    decoded_text = data["qr_data"].strip()

    # URL VERIFICATION
    url_result = verify_url(decoded_text)

    # RISK ANALYSIS
    risk_result = analyze_risk(url_result)

    score = risk_result["score"]
    status = risk_result["status"]
    reasons = risk_result["reasons"]

    # QR TYPE
    qr_type = detect_qr_type(decoded_text)

    # SAVE HISTORY
    conn = get_db()

    conn.execute("""
        INSERT INTO history
        (user_email, scan_type, value, result, score)
        VALUES (?, ?, ?, ?, ?)
    """, (
        session["email"],
        "QR Camera",
        decoded_text,
        status,
        score
    ))

    conn.commit()
    conn.close()

    return {
        "success": True,
        "data": decoded_text,
        "qr_type": qr_type,
        "score": score,
        "status": status,
        "reasons": reasons
    }


# ================= QR IMAGE UPLOAD =================

@app.route("/qr-upload", methods=["GET", "POST"])
def qr_upload():

    if "email" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        qr_image = request.files.get("qr_image")

        if not qr_image:

            return render_template(
                "qr_upload.html",
                error="Please select a QR image."
            )

        try:

            upload_folder = os.path.join(
                "uploads",
                "qr_images"
            )

            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            filename = qr_image.filename

            file_path = os.path.join(
                upload_folder,
                filename
            )

            qr_image.save(file_path)

            # REAL QR DECODING
            qr_result = decode_qr(file_path)

            if not qr_result["success"]:

                return render_template(
                    "qr_upload.html",
                    error=qr_result["message"]
                )

            decoded_text = qr_result["data"]
            qr_type = qr_result["type"]

            # URL VERIFICATION
            url_result = verify_url(decoded_text)

            # RISK ANALYSIS
            risk_result = analyze_risk(url_result)

            score = risk_result["score"]
            status = risk_result["status"]
            reasons = risk_result["reasons"]

            # SAVE HISTORY
            conn = get_db()

            conn.execute("""
                INSERT INTO history
                (user_email, scan_type, value, result, score)
                VALUES (?, ?, ?, ?, ?)
            """, (
                session["email"],
                "QR Image",
                decoded_text,
                status,
                score
            ))

            conn.commit()
            conn.close()

            # RESULT
            return render_template(
                "result.html",
                result=decoded_text,
                qr_type=qr_type,
                score=score,
                status=status,
                reasons=reasons
            )

        except Exception as e:

            print("QR ERROR:", e)

            return render_template(
                "qr_upload.html",
                error="Unable to analyze this QR image."
            )

    return render_template("qr_upload.html")


# ================= LINK CHECKER =================

@app.route("/link-checker", methods=["GET", "POST"])
def link_checker():

    if "email" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        url = request.form.get("url", "").strip()

        if not url:

            return render_template(
                "link_checker.html",
                error="Please enter a URL"
            )

        # USE SAME URL ANALYSIS ENGINE
        url_result = verify_url(url)

        risk_result = analyze_risk(url_result)

        score = risk_result["score"]
        status = risk_result["status"]
        reasons = risk_result["reasons"]

        # SAVE HISTORY
        conn = get_db()

        conn.execute("""
            INSERT INTO history
            (user_email, scan_type, value, result, score)
            VALUES (?, ?, ?, ?, ?)
        """, (
            session["email"],
            "Link",
            url,
            status,
            score
        ))

        conn.commit()
        conn.close()

        return render_template(
            "result.html",
            result=url,
            qr_type="URL",
            score=score,
            status=status,
            reasons=reasons
        )

    return render_template("link_checker.html")


# ================= HISTORY =================

@app.route("/history")
def history():

    if "email" not in session:
        return redirect(url_for("login"))

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


# ================= PROFILE =================

@app.route("/profile")
def profile():

    if "email" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    user = conn.execute(
        "SELECT * FROM users WHERE email=?",
        (session["email"],)
    ).fetchone()

    conn.close()

    return render_template(
        "profile.html",
        user=user
    )


# ================= REPORT =================

@app.route("/report", methods=["GET", "POST"])
def report():

    if "email" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        category = request.form.get("category")
        url = request.form.get("url")
        message = request.form.get("message")

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

    return render_template("report.html")


# ================= ADMIN =================

@app.route("/admin")
def admin():

    if "email" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "Administrator":
        return redirect(url_for("dashboard"))

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


# ================= LOGOUT =================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ================= START =================

if __name__ == "__main__":

    init_db()

    print("\n===================================")
    print("       TRUESCAN SERVER STARTED")
    print("===================================")
    print("Open: http://127.0.0.1:5000")
    print("===================================\n")

    app.run(
        host="127.0.0.1",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )
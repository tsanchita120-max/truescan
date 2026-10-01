from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
from werkzeug.utils import secure_filename

from modules.qr_scanner import decode_qr, detect_qr_type
from modules.url_verification import verify_url
from modules.risk_analyzer import analyze_risk


app = Flask(__name__)

app.secret_key = "truescan_secure_secret_key_2026"

DATABASE = os.path.join(
    app.root_path,
    "truescan.db"
)

UPLOAD_FOLDER = os.path.join(
    app.root_path,
    "uploads",
    "qr_images"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# =========================================================
# DATABASE
# =========================================================

def get_db():

    conn = sqlite3.connect(
        DATABASE
    )

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            mobile TEXT,
            role TEXT DEFAULT 'User',
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

    conn.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            category TEXT,
            url TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Default administrator
    admin = conn.execute(
        "SELECT * FROM users WHERE email = ?",
        ("admin@truscan.com",)
    ).fetchone()

    if not admin:

        conn.execute("""
            INSERT INTO users
            (name, email, password, mobile, role)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "Administrator",
            "admin@truscan.com",
            "1234",
            "",
            "Administrator"
        ))

    conn.commit()
    conn.close()


# =========================================================
# DATABASE MIGRATION
# =========================================================

def ensure_database_columns():

    conn = get_db()

    columns = conn.execute(
        "PRAGMA table_info(users)"
    ).fetchall()

    existing_columns = [
        column["name"]
        for column in columns
    ]

    if "mobile" not in existing_columns:

        conn.execute(
            "ALTER TABLE users ADD COLUMN mobile TEXT"
        )

    if "role" not in existing_columns:

        conn.execute(
            "ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'User'"
        )

    conn.commit()
    conn.close()


# =========================================================
# LOGIN HELPERS
# =========================================================

def user_logged_in():

    return "email" in session


def admin_logged_in():

    return (
        session.get("email") == "admin@truscan.com"
        and session.get("role") == "Administrator"
    )


# =========================================================
# HOME
# =========================================================

@app.route("/")
def index():

    if user_logged_in():

        if admin_logged_in():

            return redirect(
                url_for("admin")
            )

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "splash.html"
    )


# =========================================================
# USER LOGIN
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
        ).strip()

        conn = get_db()

        user = conn.execute("""
            SELECT *
            FROM users
            WHERE email = ?
            AND password = ?
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
            error="Invalid email or password."
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
        ).strip()

        conn = get_db()

        admin = conn.execute("""
            SELECT *
            FROM users
            WHERE email = ?
            AND password = ?
            AND role = 'Administrator'
        """, (
            email,
            password
        )).fetchone()

        conn.close()

        if admin:

            session["email"] = admin["email"]
            session["name"] = admin["name"]
            session["role"] = admin["role"]

            return redirect(
                url_for("admin")
            )

        return render_template(
            "admin_login.html",
            error="Invalid administrator credentials."
        )

    return render_template(
        "admin_login.html"
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
        ).strip()

        mobile = request.form.get(
            "mobile",
            ""
        ).strip()

        if not name or not email or not password:

            return render_template(
                "register.html",
                error="Please fill all required fields."
            )

        conn = get_db()

        existing = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        if existing:

            conn.close()

            return render_template(
                "register.html",
                error="An account with this email already exists."
            )

        conn.execute("""
            INSERT INTO users
            (name, email, password, mobile, role)
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            email,
            password,
            mobile,
            "User"
        ))

        conn.commit()
        conn.close()

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html"
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if not user_logged_in():

        return redirect(
            url_for("login")
        )

    conn = get_db()

    recent_scans = conn.execute("""
        SELECT *
        FROM history
        WHERE user_email = ?
        ORDER BY id DESC
        LIMIT 5
    """, (
        session["email"],
    )).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        recent_scans=recent_scans
    )


# =========================================================
# QR CAMERA
# =========================================================

@app.route("/qr_camera")
def qr_camera():

    if not user_logged_in():

        return redirect(
            url_for("login")
        )

    return render_template(
        "qr_camera.html"
    )


# =========================================================
# QR CAMERA ANALYSIS
# =========================================================

@app.route(
    "/analyze-qr",
    methods=["POST"]
)
def analyze_qr():

    if not user_logged_in():

        return redirect(
            url_for("login")
        )

    decoded_text = ""

    if request.form:

        decoded_text = request.form.get(
            "qr_data",
            ""
        ).strip()

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
            ]
        )

    try:

        qr_type = detect_qr_type(
            decoded_text
        )

        url_result = verify_url(
            decoded_text
        )

        risk_result = analyze_risk(
            url_result
        )

        score = risk_result.get(
            "score",
            0
        )

        status = risk_result.get(
            "status",
            "Information"
        )

        reasons = risk_result.get(
            "reasons",
            []
        )

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

        return render_template(
            "result.html",
            result=decoded_text,
            qr_type=qr_type,
            score=score,
            status=status,
            reasons=reasons
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
            ]
        )


# =========================================================
# QR IMAGE UPLOAD
# =========================================================

@app.route(
    "/qr-upload",
    methods=["GET", "POST"]
)
def qr_upload():

    if not user_logged_in():

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
                error="Please select a valid image."
            )

        try:

            filename = secure_filename(
                qr_image.filename
            )

            file_path = os.path.join(
                UPLOAD_FOLDER,
                filename
            )

            qr_image.save(
                file_path
            )

            qr_result = decode_qr(
                file_path
            )

            if not qr_result["success"]:

                return render_template(
                    "qr_upload.html",
                    error=qr_result["message"]
                )

            decoded_text = qr_result["data"]

            qr_type = qr_result["type"]

            url_result = verify_url(
                decoded_text
            )

            risk_result = analyze_risk(
                url_result
            )

            score = risk_result["score"]

            status = risk_result["status"]

            reasons = risk_result["reasons"]

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

            return render_template(
                "result.html",
                result=decoded_text,
                qr_type=qr_type,
                score=score,
                status=status,
                reasons=reasons
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

    if not user_logged_in():

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

            url_result = verify_url(
                url
            )

            risk_result = analyze_risk(
                url_result
            )

            score = risk_result["score"]

            status = risk_result["status"]

            reasons = risk_result["reasons"]

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
                qr_type="Website / URL",
                score=score,
                status=status,
                reasons=reasons
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

    if not user_logged_in():

        return redirect(
            url_for("login")
        )

    conn = get_db()

    scans = conn.execute("""
        SELECT *
        FROM history
        WHERE user_email = ?
        ORDER BY id DESC
    """, (
        session["email"],
    )).fetchall()

    conn.close()

    return render_template(
        "history.html",
        scans=scans
    )


# =========================================================
# PROFILE
# =========================================================

@app.route("/profile")
def profile():

    if not user_logged_in():

        return redirect(
            url_for("login")
        )

    conn = get_db()

    user = conn.execute("""
        SELECT *
        FROM users
        WHERE email = ?
    """, (
        session["email"],
    )).fetchone()

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

    if not user_logged_in():

        return redirect(
            url_for("login")
        )

    if request.method == "POST":

        category = request.form.get(
            "category",
            ""
        ).strip()

        url = request.form.get(
            "url",
            ""
        ).strip()

        message = request.form.get(
            "message",
            ""
        ).strip()

        conn = get_db()

        conn.execute("""
            INSERT INTO reports
            (email, category, url, message)
            VALUES (?, ?, ?, ?)
        """, (
            session["email"],
            category,
            url,
            message
        ))

        conn.commit()
        conn.close()

        return render_template(
            "report.html",
            success="Report submitted successfully."
        )

    return render_template(
        "report.html"
    )


# =========================================================
# ADMIN PANEL
# =========================================================

@app.route("/admin")
def admin():

    if not admin_logged_in():

        return redirect(
            url_for("admin_login")
        )

    conn = get_db()

    users = conn.execute("""
        SELECT *
        FROM users
        ORDER BY id DESC
    """).fetchall()

    scans = conn.execute("""
        SELECT *
        FROM history
        ORDER BY id DESC
    """).fetchall()

    reports = conn.execute("""
        SELECT *
        FROM reports
        ORDER BY id DESC
    """).fetchall()

    total_users = conn.execute("""
        SELECT COUNT(*) AS count
        FROM users
        WHERE role != 'Administrator'
    """).fetchone()["count"]

    total_scans = conn.execute("""
        SELECT COUNT(*) AS count
        FROM history
    """).fetchone()["count"]

    total_reports = conn.execute("""
        SELECT COUNT(*) AS count
        FROM reports
    """).fetchone()["count"]

    conn.close()

    return render_template(
        "admin.html",
        users=users,
        scans=scans,
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

    ensure_database_columns()

print("===================================")
print("Open: http://127.0.0.1:5000")
print("Open on network: http://192.168.0.103:5000")
print("===================================")
print("")

app.run(
    host="0.0.0.0",
    port=int(
        os.environ.get(
            "PORT",
            5000
        )
    ),
    debug=True
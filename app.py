from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify
)

import sqlite3
import os
import uuid
import re

from werkzeug.utils import secure_filename

from modules.qr_scanner import decode_qr, detect_qr_type
from modules.url_verification import verify_url
from modules.risk_analyzer import analyze_risk


# =========================================================
# APP CONFIGURATION
# =========================================================

app = Flask(__name__)

app.secret_key = "truescan_secure_secret_key_2026"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE = os.path.join(
    BASE_DIR,
    "truescan.db"
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "static",
    "uploads"
)

PROFILE_FOLDER = os.path.join(
    UPLOAD_FOLDER,
    "profile"
)

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    PROFILE_FOLDER,
    exist_ok=True
)


# =========================================================
# LANGUAGE SETTINGS
# =========================================================

SUPPORTED_LANGUAGES = {
    "en": "English",
    "mr": "मराठी",
    "hi": "हिन्दी"
}


def get_language():
    language = session.get(
        "language",
        "en"
    )

    if language not in SUPPORTED_LANGUAGES:
        language = "en"

    return language


@app.route(
    "/set-language",
    methods=["POST"]
)
def set_language():

    language = request.form.get(
        "language",
        "en"
    ).strip().lower()

    if language not in SUPPORTED_LANGUAGES:
        return jsonify({
            "success": False,
            "message": "Unsupported language."
        }), 400

    session["language"] = language

    return jsonify({
        "success": True,
        "language": language,
        "language_name": SUPPORTED_LANGUAGES[language]
    })


@app.context_processor
def inject_language():

    return {
        "current_language": get_language(),
        "supported_languages": SUPPORTED_LANGUAGES
    }
# =========================================================
# GLOBAL TRUESCAN LANGUAGE SCRIPT
# =========================================================

@app.after_request
def inject_truescan_language(response):

    content_type = response.headers.get(
        "Content-Type",
        ""
    )

    if (
        "text/html" in content_type
        and response.status_code == 200
    ):

        try:

            html = response.get_data(
                as_text=True
            )

            if "truescan-language.js" not in html:

                script_tag = """
<script src="/static/js/truescan-language.js"></script>
"""

                if "</body>" in html:

                    html = html.replace(
                        "</body>",
                        script_tag + "</body>",
                        1
                    )

                elif "</BODY>" in html:

                    html = html.replace(
                        "</BODY>",
                        script_tag + "</BODY>",
                        1
                    )

                else:

                    html += script_tag

                response.set_data(html)

        except Exception as e:

            print(
                "LANGUAGE SCRIPT INJECTION ERROR:",
                e
            )

    return response

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

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            mobile TEXT,

            role TEXT DEFAULT 'User',

            profile_image TEXT,

            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_email TEXT,

            scan_type TEXT,

            value TEXT,

            result TEXT,

            score INTEGER DEFAULT 0,

            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS reports (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            email TEXT,

            category TEXT,

            url TEXT,

            message TEXT,

            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS alerts (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            email TEXT,

            title TEXT,

            message TEXT,

            risk_score INTEGER DEFAULT 0,

            is_read INTEGER DEFAULT 0,

            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP
        )
    """)

    admin = conn.execute("""
        SELECT *
        FROM users
        WHERE email = ?
    """, (
        "admin@truscan.com",
    )).fetchone()

    if not admin:

        conn.execute("""
            INSERT INTO users
            (
                name,
                email,
                password,
                mobile,
                role
            )
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


def ensure_database_columns():

    conn = get_db()

    columns = conn.execute(
        "PRAGMA table_info(users)"
    ).fetchall()

    column_names = [
        column["name"]
        for column in columns
    ]

    if "mobile" not in column_names:

        conn.execute("""
            ALTER TABLE users
            ADD COLUMN mobile TEXT
        """)

    if "role" not in column_names:

        conn.execute("""
            ALTER TABLE users
            ADD COLUMN role TEXT DEFAULT 'User'
        """)

    if "profile_image" not in column_names:

        conn.execute("""
            ALTER TABLE users
            ADD COLUMN profile_image TEXT
        """)

    conn.commit()

    conn.close()


# =========================================================
# BASIC HELPERS
# =========================================================

def user_logged_in():

    return "email" in session


def admin_logged_in():

    return (
        "email" in session
        and
        session.get("role") == "Administrator"
    )


def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )


# =========================================================
# HISTORY
# =========================================================

def save_history(
    email,
    scan_type,
    value,
    result,
    score
):

    conn = get_db()

    conn.execute("""
        INSERT INTO history
        (
            user_email,
            scan_type,
            value,
            result,
            score
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        email,
        scan_type,
        value,
        result,
        score
    ))

    conn.commit()

    conn.close()


# =========================================================
# ALERTS
# =========================================================

def create_security_alert(
    email,
    title,
    message,
    score
):

    conn = get_db()

    conn.execute("""
        INSERT INTO alerts
        (
            email,
            title,
            message,
            risk_score,
            is_read
        )
        VALUES (?, ?, ?, ?, 0)
    """, (
        email,
        title,
        message,
        score
    ))

    conn.commit()

    conn.close()


def generate_security_alert(
    email,
    value,
    status,
    score
):

    if score >= 60:

        create_security_alert(
            email,
            "Dangerous Scan Detected",
            "TRUESCAN detected a potentially dangerous QR code or link.",
            score
        )

    elif score >= 30:

        create_security_alert(
            email,
            "Suspicious Scan Detected",
            "TRUESCAN detected suspicious indicators in the scanned content.",
            score
        )


# =========================================================
# SMART SECURITY FEATURES
# =========================================================

def generate_security_explanation(
    status,
    score,
    reasons
):

    reasons = reasons or []

    if status == "Dangerous" or score >= 60:

        explanation = (
            "This QR code or link shows strong indicators "
            "of a potentially dangerous destination. "
            "Avoid opening it or entering personal information."
        )

        action = (
            "Avoid opening this link. Verify the source "
            "through an official website or trusted contact."
        )

    elif status == "Suspicious" or score >= 30:

        explanation = (
            "This QR code or link contains suspicious indicators. "
            "The destination should be verified before you continue."
        )

        action = (
            "Verify the website and sender before opening "
            "the link or entering personal information."
        )

    else:

        explanation = (
            "No major suspicious indicators were detected "
            "during the current security analysis."
        )

        action = (
            "Continue with normal security precautions and "
            "verify the destination before sharing sensitive information."
        )

    return {
        "explanation": explanation,
        "action": action,
        "why_risky": reasons
    }


# =========================================================
# THREAT PATTERN DETECTION
# =========================================================

def detect_threat_patterns(
    value,
    reasons=None
):

    value = str(
        value or ""
    ).strip().lower()

    reasons = reasons or []

    patterns = []

    # HTTP instead of HTTPS

    if value.startswith("http://"):

        patterns.append(
            "The link uses HTTP instead of HTTPS."
        )

    # URL SHORTENERS

    shorteners = [
        "bit.ly",
        "tinyurl.com",
        "t.co",
        "goo.gl",
        "ow.ly",
        "is.gd",
        "buff.ly"
    ]

    if any(
        domain in value
        for domain in shorteners
    ):

        patterns.append(
            "A shortened URL was detected."
        )

    # SUSPICIOUS KEYWORDS

    suspicious_words = [
        "login",
        "verify",
        "verification",
        "password",
        "account",
        "update",
        "bank",
        "payment",
        "otp",
        "confirm"
    ]

    found_words = [
        word
        for word in suspicious_words
        if word in value
    ]

    if found_words:

        patterns.append(
            "Suspicious keywords detected: "
            + ", ".join(found_words)
        )

    # IP ADDRESS URL

    if re.search(
        r"https?://(?:\d{1,3}\.){3}\d{1,3}",
        value
    ):

        patterns.append(
            "The URL uses an IP address instead of a normal domain."
        )

    # VERY LONG URL

    if len(value) > 200:

        patterns.append(
            "The URL is unusually long."
        )

    # @ SYMBOL

    if "@" in value:

        patterns.append(
            "The URL contains an @ character."
        )

    # EXISTING RISK REASONS

    for reason in reasons:

        reason = str(reason)

        if (
            reason
            and
            reason not in patterns
        ):

            patterns.append(
                reason
            )

    return patterns


# =========================================================
# RECOMMENDED ACTION
# =========================================================

def get_recommended_action(
    status,
    score
):

    if status == "Dangerous" or score >= 60:

        return {
            "level": "Dangerous",
            "action": "Avoid opening this link."
        }

    if status == "Suspicious" or score >= 30:

        return {
            "level": "Suspicious",
            "action": "Verify the destination before opening."
        }

    return {
        "level": "Safe",
        "action": "Continue with normal security precautions."
    }


# =========================================================
# REPEATED THREAT DETECTION
# =========================================================

def check_repeated_threat(
    email,
    value
):

    if not email or not value:

        return {
            "repeated": False,
            "count": 0
        }

    conn = get_db()

    try:

        row = conn.execute("""
            SELECT COUNT(*)
            FROM history
            WHERE user_email = ?
            AND value = ?
            AND result IN (
                'Suspicious',
                'Dangerous'
            )
        """, (
            email,
            value
        )).fetchone()

        count = (
            row[0]
            if row
            else 0
        )

        return {
            "repeated": count > 0,
            "count": count
        }

    except Exception as e:

        print(
            "REPEATED THREAT ERROR:",
            e
        )

        return {
            "repeated": False,
            "count": 0
        }

    finally:

        conn.close()


# =========================================================
# BUILD SMART SECURITY DATA
# =========================================================

def build_smart_security_data(
    email,
    value,
    status,
    score,
    reasons
):

    threat_patterns = detect_threat_patterns(
        value,
        reasons
    )

    explanation = generate_security_explanation(
        status,
        score,
        reasons
    )

    recommended_action = get_recommended_action(
        status,
        score
    )

    repeated_threat = check_repeated_threat(
        email,
        value
    )

    return {

        "security_explanation":
            explanation["explanation"],

        "recommended_action":
            explanation["action"],

        "why_risky":
            explanation["why_risky"],

        "threat_patterns":
            threat_patterns,

        "recommended_action_data":
            recommended_action,

        "repeated_threat":
            repeated_threat["repeated"],

        "repeated_threat_count":
            repeated_threat["count"]
    }


# =========================================================
# SPLASH
# =========================================================

@app.route("/")
def splash():

    return render_template(
        "splash.html"
    )


# =========================================================
# LOGIN
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

        admin_user = conn.execute("""
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

        if admin_user:

            session["email"] = admin_user["email"]

            session["name"] = admin_user["name"]

            session["role"] = admin_user["role"]

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

        confirm_password = request.form.get(
            "confirm_password",
            request.form.get(
                "confirm",
                ""
            )
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

        if password != confirm_password:

            return render_template(
                "register.html",
                error="Passwords do not match."
            )

        conn = get_db()

        existing = conn.execute("""
            SELECT *
            FROM users
            WHERE email = ?
        """, (
            email,
        )).fetchone()

        if existing:

            conn.close()

            return render_template(
                "register.html",
                error="An account with this email already exists."
            )

        conn.execute("""
            INSERT INTO users
            (
                name,
                email,
                password,
                mobile,
                role
            )
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

    total_scans = conn.execute("""
        SELECT COUNT(*)
        FROM history
        WHERE user_email = ?
    """, (
        session["email"],
    )).fetchone()[0]

    unread_alerts = conn.execute("""
        SELECT COUNT(*)
        FROM alerts
        WHERE email = ?
        AND is_read = 0
    """, (
        session["email"],
    )).fetchone()[0]

    daily_rows = conn.execute("""
        SELECT
            date(
                datetime(
                    created_at,
                    '+5 hours',
                    '+30 minutes'
                )
            ) AS scan_date,
            COUNT(*) AS scan_count
        FROM history
        WHERE user_email = ?
        GROUP BY scan_date
        ORDER BY scan_date DESC
        LIMIT 7
    """, (
        session["email"],
    )).fetchall()

    conn.close()

    daily_scans = list(
        reversed(daily_rows)
    )

    daily_max = max(
        [
            row["scan_count"]
            for row in daily_scans
        ] or [0]
    )

    weekly_total = sum(
        row["scan_count"]
        for row in daily_scans
    )

    return render_template(
        "dashboard.html",
        recent_scans=recent_scans,
        total_scans=total_scans,
        unread_alerts=unread_alerts,
        daily_scans=daily_scans,
        daily_max=daily_max,
        weekly_total=weekly_total,
        name=session.get(
            "name",
            "User"
        ),
        email=session.get(
            "email",
            ""
        ),
        current_language=get_language()
    )


# =========================================================
# QR CAMERA
# =========================================================

@app.route("/qr_camera")
@app.route("/qr-camera")
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

        smart_data = build_smart_security_data(
            session["email"],
            decoded_text,
            status,
            score,
            reasons
        )

        save_history(
            session["email"],
            "QR Camera",
            decoded_text,
            status,
            score
        )

        generate_security_alert(
            session["email"],
            decoded_text,
            status,
            score
        )

        if smart_data["repeated_threat"]:

            create_security_alert(
                session["email"],
                "Previously Detected Threat",
                "This QR/link was previously detected as suspicious or dangerous.",
                score
            )

        return render_template(
            "result.html",
            result=decoded_text,
            qr_type=qr_type,
            score=score,
            status=status,
            reasons=reasons,
            **smart_data
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
            security_explanation=(
                "TRUESCAN could not complete the security analysis."
            ),
            recommended_action=(
                "Please try scanning the QR code again."
            ),
            why_risky=[],
            threat_patterns=[],
            recommended_action_data={
                "level": "Unknown",
                "action": "Try the scan again."
            },
            repeated_threat=False,
            repeated_threat_count=0
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

        if not allowed_file(
            qr_image.filename
        ):

            return render_template(
                "qr_upload.html",
                error="Only PNG, JPG, JPEG and WEBP images are allowed."
            )

        file_path = None

        try:

            extension = qr_image.filename.rsplit(
                ".",
                1
            )[1].lower()

            filename = secure_filename(
                str(uuid.uuid4())
                + "."
                + extension
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

            smart_data = build_smart_security_data(
                session["email"],
                decoded_text,
                status,
                score,
                reasons
            )

            save_history(
                session["email"],
                "QR Image",
                decoded_text,
                status,
                score
            )

            generate_security_alert(
                session["email"],
                decoded_text,
                status,
                score
            )

            if smart_data["repeated_threat"]:

                create_security_alert(
                    session["email"],
                    "Previously Detected Threat",
                    "This QR/link was previously detected as suspicious or dangerous.",
                    score
                )

            return render_template(
                "result.html",
                result=decoded_text,
                qr_type=qr_type,
                score=score,
                status=status,
                reasons=reasons,
                **smart_data
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

        finally:

            if (
                file_path
                and
                os.path.exists(file_path)
            ):

                try:

                    os.remove(
                        file_path
                    )

                except OSError:

                    pass

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

            smart_data = build_smart_security_data(
                session["email"],
                url,
                status,
                score,
                reasons
            )

            save_history(
                session["email"],
                "Link",
                url,
                status,
                score
            )

            generate_security_alert(
                session["email"],
                url,
                status,
                score
            )

            if smart_data["repeated_threat"]:

                create_security_alert(
                    session["email"],
                    "Previously Detected Threat",
                    "This QR/link was previously detected as suspicious or dangerous.",
                    score
                )

            return render_template(
                "result.html",
                result=url,
                qr_type="Website / URL",
                score=score,
                status=status,
                reasons=reasons,
                **smart_data
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

    records = conn.execute("""
        SELECT *
        FROM history
        WHERE user_email = ?
        ORDER BY id DESC
    """, (
        session["email"],
    )).fetchall()

    total_scans = len(records)

    conn.close()

    return render_template(
        "history.html",
        records=records,
        scans=records,
        total_scans=total_scans
    )


# =========================================================
# ALERTS
# =========================================================

@app.route("/alerts")
def alerts():

    if not user_logged_in():

        return redirect(
            url_for("login")
        )

    conn = get_db()

    alert_list = conn.execute("""
        SELECT *
        FROM alerts
        WHERE email = ?
        ORDER BY id DESC
    """, (
        session["email"],
    )).fetchall()

    unread_count = conn.execute("""
        SELECT COUNT(*)
        FROM alerts
        WHERE email = ?
        AND is_read = 0
    """, (
        session["email"],
    )).fetchone()[0]

    conn.close()

    return render_template(
        "alerts.html",
        alerts=alert_list,
        unread_count=unread_count
    )


# =========================================================
# MARK ALERTS READ
# =========================================================

@app.route("/alerts-read")
def alerts_read():

    if not user_logged_in():

        return redirect(
            url_for("login")
        )

    conn = get_db()

    conn.execute("""
        UPDATE alerts
        SET is_read = 1
        WHERE email = ?
    """, (
        session["email"],
    ))

    conn.commit()

    conn.close()

    return redirect(
        url_for("alerts")
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
# PROFILE IMAGE
# =========================================================

@app.route(
    "/upload-profile-image",
    methods=["POST"]
)
def upload_profile_image():

    if not user_logged_in():

        return redirect(
            url_for("login")
        )

    profile_image = request.files.get(
        "profile_image"
    )

    if (
        not profile_image
        or
        not profile_image.filename
    ):

        return redirect(
            url_for("profile")
        )

    if not allowed_file(
        profile_image.filename
    ):

        return redirect(
            url_for("profile")
        )

    extension = profile_image.filename.rsplit(
        ".",
        1
    )[1].lower()

    filename = secure_filename(
        str(uuid.uuid4())
        + "."
        + extension
    )

    file_path = os.path.join(
        PROFILE_FOLDER,
        filename
    )

    try:

        profile_image.save(
            file_path
        )

        conn = get_db()

        old_user = conn.execute("""
            SELECT profile_image
            FROM users
            WHERE email = ?
        """, (
            session["email"],
        )).fetchone()

        old_image = (
            old_user["profile_image"]
            if old_user
            else None
        )

        conn.execute("""
            UPDATE users
            SET profile_image = ?
            WHERE email = ?
        """, (
            filename,
            session["email"]
        ))

        conn.commit()

        conn.close()

        if old_image:

            old_path = os.path.join(
                PROFILE_FOLDER,
                old_image
            )

            if os.path.exists(old_path):

                try:

                    os.remove(
                        old_path
                    )

                except OSError:

                    pass

    except Exception as e:

        print(
            "PROFILE IMAGE ERROR:",
            e
        )

        if os.path.exists(file_path):

            try:

                os.remove(
                    file_path
                )

            except OSError:

                pass

    return redirect(
        url_for("profile")
    )


# =========================================================
# SECURITY SETTINGS
# =========================================================

@app.route("/security-settings")
def security_settings():

    if not user_logged_in():

        return redirect(
            url_for("login")
        )

    return render_template(
        "security_settings.html"
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
            (
                email,
                category,
                url,
                message
            )
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
            success="Scam report submitted successfully."
        )

    return render_template(
        "report.html"
    )


# =========================================================
# ADMIN
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
        SELECT COUNT(*)
        FROM users
        WHERE role != 'Administrator'
    """).fetchone()[0]

    total_scans = conn.execute("""
        SELECT COUNT(*)
        FROM history
    """).fetchone()[0]

    total_reports = conn.execute("""
        SELECT COUNT(*)
        FROM reports
    """).fetchone()[0]

    total_alerts = conn.execute("""
        SELECT COUNT(*)
        FROM alerts
    """).fetchone()[0]

    conn.close()

    return render_template(
        "admin.html",
        users=users,
        scans=scans,
        reports=reports,
        total_users=total_users,
        total_scans=total_scans,
        total_reports=total_reports,
        total_alerts=total_alerts
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

    print("")
    print("===================================")
    print("       TRUESCAN SERVER STARTED")
    print("===================================")
    print("Local:   http://127.0.0.1:5000")
    print("Network: http://0.0.0.0:5000")
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
    )
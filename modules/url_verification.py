import re

from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# =========================================================
# SHORTENED URL SERVICES
# =========================================================

SHORTENED_SERVICES = [
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "is.gd",
    "cutt.ly",
    "shorturl.at",
    "js.tc",
    "ow.ly",
    "buff.ly",
    "rebrand.ly",
    "soo.gd",
    "s2r.co",
    "tiny.cc",
    "lnkd.in",
    "rb.gy"
]


# =========================================================
# SUSPICIOUS KEYWORDS
# =========================================================

SUSPICIOUS_WORDS = [
    "login",
    "verify",
    "verification",
    "password",
    "account",
    "update",
    "secure",
    "urgent",
    "claim",
    "reward",
    "prize",
    "free",
    "otp",
    "bank",
    "wallet",
    "payment",
    "signin",
    "confirm"
]


# =========================================================
# CHECK SHORTENED DOMAIN
# =========================================================

def is_shortened_domain(domain):

    domain = domain.lower().strip()

    return any(
        shortener == domain
        or domain.endswith("." + shortener)
        for shortener in SHORTENED_SERVICES
    )


# =========================================================
# FOLLOW REDIRECTS
# =========================================================

def follow_redirects(url, max_redirects=5):

    result = {
        "success": False,
        "final_url": url,
        "redirect_detected": False,
        "redirect_count": 0,
        "redirect_chain": [url],
        "error": ""
    }

    current_url = url

    for _ in range(max_redirects):

        try:

            request = Request(
                current_url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 "
                        "(Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 "
                        "(KHTML, like Gecko) "
                        "Chrome/154.0 Safari/537.36"
                    )
                }
            )

            response = urlopen(
                request,
                timeout=5
            )

            final_url = response.geturl()

            response.close()

            if final_url != current_url:

                result["redirect_detected"] = True

                result["redirect_count"] += 1

                result["redirect_chain"].append(
                    final_url
                )

                current_url = final_url

                continue

            result["success"] = True

            result["final_url"] = current_url

            return result

        except HTTPError as e:

            location = e.headers.get(
                "Location"
            )

            if location:

                result["redirect_detected"] = True

                result["redirect_count"] += 1

                result["redirect_chain"].append(
                    location
                )

                current_url = location

                continue

            result["error"] = (
                "HTTP error: "
                + str(e.code)
            )

            result["final_url"] = current_url

            return result

        except URLError as e:

            result["error"] = (
                "Unable to follow the link."
            )

            result["final_url"] = current_url

            return result

        except Exception as e:

            result["error"] = (
                "Redirect check failed."
            )

            result["final_url"] = current_url

            return result

    result["final_url"] = current_url

    result["error"] = (
        "Too many redirects detected."
    )

    result["redirect_detected"] = True

    return result


# =========================================================
# URL VERIFICATION
# =========================================================

def verify_url(url):

    result = {

        "is_url": False,

        "https": False,

        "suspicious": False,

        "score": 0,

        "status": "Information",

        "reasons": [],

        # New redirect fields
        "shortened_url": False,

        "redirect_detected": False,

        "redirect_count": 0,

        "final_url": url,

        "redirect_chain": [],

        "redirect_error": ""

    }

    # =====================================================
    # EMPTY URL
    # =====================================================

    if not url:

        result["reasons"].append(
            "No URL found."
        )

        return result

    url = url.strip()

    result["final_url"] = url

    # =====================================================
    # HTTP / HTTPS CHECK
    # =====================================================

    if not re.match(
        r"^https?://",
        url,
        re.IGNORECASE
    ):

        result["reasons"].append(
            "The scanned content is not an HTTP/HTTPS URL."
        )

        return result

    result["is_url"] = True

    # =====================================================
    # PARSE URL
    # =====================================================

    try:

        parsed = urlparse(url)

        domain = parsed.hostname or ""

        domain = domain.lower()

    except Exception:

        result["score"] += 30

        result["reasons"].append(
            "The URL format could not be parsed correctly."
        )

        result["status"] = "Suspicious"

        result["suspicious"] = True

        return result

    # =====================================================
    # HTTPS CHECK
    # =====================================================

    if parsed.scheme.lower() == "https":

        result["https"] = True

        result["reasons"].append(
            "The website uses HTTPS."
        )

    else:

        result["score"] += 20

        result["reasons"].append(
            "The website does not use HTTPS."
        )

    # =====================================================
    # IP ADDRESS CHECK
    # =====================================================

    ip_pattern = (
        r"^\d{1,3}"
        r"(\.\d{1,3}){3}"
        r"(?::\d+)?$"
    )

    if re.match(
        ip_pattern,
        parsed.netloc
    ):

        result["score"] += 25

        result["reasons"].append(
            "The URL uses an IP address instead of a normal domain."
        )

    # =====================================================
    # SHORTENED URL CHECK
    # =====================================================

    if is_shortened_domain(domain):

        result["shortened_url"] = True

        result["score"] += 25

        result["reasons"].append(
            "The URL uses a shortened-link service."
        )

        # =================================================
        # FOLLOW SHORTENED URL
        # =================================================

        redirect_result = follow_redirects(
            url,
            max_redirects=5
        )

        result["redirect_detected"] = (
            redirect_result["redirect_detected"]
        )

        result["redirect_count"] = (
            redirect_result["redirect_count"]
        )

        result["final_url"] = (
            redirect_result["final_url"]
        )

        result["redirect_chain"] = (
            redirect_result["redirect_chain"]
        )

        result["redirect_error"] = (
            redirect_result["error"]
        )

        # =================================================
        # REDIRECT RESULT
        # =================================================

        if result["redirect_detected"]:

            result["score"] += 10

            result["reasons"].append(
                "The shortened URL redirects to another destination."
            )

        if result["redirect_count"] >= 3:

            result["score"] += 10

            result["reasons"].append(
                "The URL uses multiple redirects."
            )

        if result["redirect_error"]:

            result["reasons"].append(
                result["redirect_error"]
            )

    # =====================================================
    # FINAL URL ANALYSIS
    # =====================================================

    analysis_url = result["final_url"]

    try:

        final_parsed = urlparse(
            analysis_url
        )

        final_domain = (
            final_parsed.hostname
            or ""
        ).lower()

    except Exception:

        final_parsed = parsed

        final_domain = domain

    # =====================================================
    # FINAL DOMAIN DIFFERENCE
    # =====================================================

    if (
        result["redirect_detected"]
        and final_domain
        and final_domain != domain
    ):

        result["reasons"].append(
            "The link redirects to a different domain."
        )

    # =====================================================
    # SUSPICIOUS KEYWORD CHECK
    # =====================================================

    found_words = []

    lower_url = analysis_url.lower()

    for word in SUSPICIOUS_WORDS:

        if word in lower_url:

            found_words.append(
                word
            )

    if found_words:

        result["score"] += min(
            len(found_words) * 5,
            25
        )

        result["reasons"].append(
            "Suspicious keywords found: "
            + ", ".join(found_words)
        )

    # =====================================================
    # @ SYMBOL
    # =====================================================

    if "@" in analysis_url:

        result["score"] += 20

        result["reasons"].append(
            "The URL contains an @ symbol."
        )

    # =====================================================
    # VERY LONG URL
    # =====================================================

    if len(analysis_url) > 150:

        result["score"] += 10

        result["reasons"].append(
            "The URL is unusually long."
        )

    # =====================================================
    # MANY SUBDOMAINS
    # =====================================================

    if final_domain.count(".") >= 4:

        result["score"] += 10

        result["reasons"].append(
            "The domain contains many subdomains."
        )

    # =====================================================
    # SUSPICIOUS HYPHEN PATTERN
    # =====================================================

    if final_domain.count("-") >= 3:

        result["score"] += 10

        result["reasons"].append(
            "The domain contains multiple hyphens."
        )

    # =====================================================
    # NON-STANDARD PORT
    # =====================================================

    try:

        final_port = final_parsed.port

        if final_port:

            if final_port not in [
                80,
                443
            ]:

                result["score"] += 10

                result["reasons"].append(
                    "The URL uses a non-standard network port."
                )

    except ValueError:

        result["score"] += 10

        result["reasons"].append(
            "The URL contains an invalid network port."
        )

    # =====================================================
    # KEEP SCORE BETWEEN 0 AND 100
    # =====================================================

    result["score"] = min(
        result["score"],
        100
    )

    # =====================================================
    # FINAL STATUS
    # =====================================================

    if result["score"] >= 60:

        result["status"] = "Dangerous"

        result["suspicious"] = True

    elif result["score"] >= 30:

        result["status"] = "Suspicious"

        result["suspicious"] = True

    else:

        result["status"] = "Safe"

        result["suspicious"] = False

    # =====================================================
    # NOTHING SUSPICIOUS
    # =====================================================

    if not result["reasons"]:

        result["reasons"].append(
            "No common suspicious indicators were detected."
        )

    return result
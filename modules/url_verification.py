import re
from urllib.parse import urlparse


def verify_url(url):

    result = {
        "is_url": False,
        "https": False,
        "suspicious": False,
        "score": 0,
        "reasons": []
    }

    if not url:
        result["reasons"].append("No URL found.")
        return result

    url = url.strip()

    # Check HTTP / HTTPS URL
    if not re.match(r"^https?://", url, re.IGNORECASE):
        result["reasons"].append(
            "QR contains data that is not an HTTP/HTTPS URL."
        )
        return result

    result["is_url"] = True

    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    # HTTPS check
    if parsed.scheme.lower() == "https":
        result["https"] = True
    else:
        result["score"] += 20
        result["reasons"].append(
            "The website does not use HTTPS."
        )

    # IP address URL
    ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}(:\d+)?$"

    if re.match(ip_pattern, domain):
        result["score"] += 25
        result["reasons"].append(
            "The URL uses an IP address instead of a normal domain."
        )

    # Shortened URL
    shorteners = [
        "bit.ly",
        "tinyurl.com",
        "t.co",
        "is.gd",
        "cutt.ly",
        "shorturl.at",
        "js.tc"
    ]

    for shortener in shorteners:
        if shortener in domain:
            result["score"] += 25
            result["reasons"].append(
                "The URL uses a shortened-link service."
            )
            break

    # Suspicious keywords
    suspicious_words = [
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
        "bank"
    ]

    found_words = []

    for word in suspicious_words:
        if word in url.lower():
            found_words.append(word)

    if found_words:
        result["score"] += min(
            len(found_words) * 5,
            25
        )

        result["reasons"].append(
            "Suspicious keywords found: "
            + ", ".join(found_words)
        )

    # @ symbol
    if "@" in url:
        result["score"] += 20
        result["reasons"].append(
            "The URL contains an @ symbol."
        )

    # Very long URL
    if len(url) > 150:
        result["score"] += 10
        result["reasons"].append(
            "The URL is unusually long."
        )

    # Many subdomains
    if domain.count(".") >= 4:
        result["score"] += 10
        result["reasons"].append(
            "The domain contains many subdomains."
        )

    # Maximum score
    result["score"] = min(
        result["score"],
        100
    )

    if result["score"] >= 60:
        result["suspicious"] = True

    return result
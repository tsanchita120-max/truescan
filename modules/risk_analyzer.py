def analyze_risk(url_result):

    score = url_result.get("score", 0)
    reasons = url_result.get("reasons", [])

    # QR data is not a URL
    if not url_result.get("is_url", False):
        return {
            "score": 0,
            "status": "Information",
            "reasons": reasons
        }

    # Final risk status
    if score >= 60:
        status = "Dangerous"

    elif score >= 30:
        status = "Suspicious"

    else:
        status = "Safe"

    # No suspicious indicators
    if not reasons:
        reasons = [
            "No common suspicious indicators were detected."
        ]

    return {
        "score": score,
        "status": status,
        "reasons": reasons
    }
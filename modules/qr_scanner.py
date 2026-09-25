import cv2


def detect_qr_type(data):
    if not data:
        return "Unknown"

    text = data.strip().lower()

    if text.startswith("http://") or text.startswith("https://"):
        return "Website / URL"

    if text.startswith("upi://"):
        return "UPI Payment"

    if text.startswith("mailto:"):
        return "Email"

    if text.startswith("tel:"):
        return "Phone Number"

    if text.startswith("wifi:"):
        return "Wi-Fi"

    if text.startswith("smsto:") or text.startswith("sms:"):
        return "SMS"

    if text.startswith("begin:vcard"):
        return "Contact / vCard"

    return "Text"


def decode_qr(image_path):

    image = cv2.imread(image_path)

    if image is None:
        return {
            "success": False,
            "data": None,
            "type": "Unknown",
            "message": "Unable to read image."
        }

    detector = cv2.QRCodeDetector()

    data, points, _ = detector.detectAndDecode(image)

    if data:
        return {
            "success": True,
            "data": data,
            "type": detect_qr_type(data),
            "message": "QR code detected successfully."
        }

    return {
        "success": False,
        "data": None,
        "type": "Unknown",
        "message": "No readable QR code found."
    }

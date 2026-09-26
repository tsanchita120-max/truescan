import cv2


def detect_qr_type(data):

    if not data:
        return "Unknown"

    text = data.strip().lower()

    if text.startswith("http://") or text.startswith("https://"):
        return "Website / URL"

    if text.startswith("upi://"):
        return "UPI Payment"

    if text.startswith("wifi:"):
        return "Wi-Fi Network"

    if text.startswith("mailto:"):
        return "Email"

    if text.startswith("tel:"):
        return "Phone Number"

    if text.startswith("sms:") or text.startswith("smsto:"):
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
            "message": "Unable to read the uploaded image."
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

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    data, points, _ = detector.detectAndDecode(gray)

    if data:
        return {
            "success": True,
            "data": data,
            "type": detect_qr_type(data),
            "message": "QR code detected successfully."
        }

    resized = cv2.resize(
        image,
        None,
        fx=1.5,
        fy=1.5,
        interpolation=cv2.INTER_CUBIC
    )

    data, points, _ = detector.detectAndDecode(resized)

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
        "message": "No readable QR code found in the image."
    }

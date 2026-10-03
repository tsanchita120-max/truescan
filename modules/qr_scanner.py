import cv2
import os
import re


# =========================================================
# QR TYPE DETECTION
# =========================================================

def detect_qr_type(data):

    data = str(data or "").strip()

    if not data:
        return "Unknown"

    lower_data = data.lower()

    # Website / URL
    if lower_data.startswith("http://") or lower_data.startswith("https://"):
        return "Website / URL"

    # Email
    if lower_data.startswith("mailto:"):
        return "Email"

    # Phone
    if lower_data.startswith("tel:"):
        return "Phone Number"

    # SMS
    if lower_data.startswith("sms:"):
        return "SMS"

    # WiFi
    if lower_data.startswith("wifi:"):
        return "Wi-Fi"

    # Location
    if lower_data.startswith("geo:"):
        return "Location"

    # UPI
    if lower_data.startswith("upi://"):
        return "UPI Payment"

    # WhatsApp
    if "wa.me/" in lower_data or "whatsapp.com" in lower_data:
        return "WhatsApp"

    # Common social links
    social_domains = [
        "instagram.com",
        "facebook.com",
        "twitter.com",
        "x.com",
        "linkedin.com",
        "youtube.com",
        "t.me"
    ]

    if any(domain in lower_data for domain in social_domains):
        return "Social / Website"

    # vCard
    if "begin:vcard" in lower_data:
        return "Contact / vCard"

    # Plain text
    return "Text"


# =========================================================
# CLEAN QR RESULT
# =========================================================

def clean_qr_data(data):

    if data is None:
        return ""

    data = str(data)

    data = data.replace("\x00", "")

    return data.strip()


# =========================================================
# NORMALIZE IMAGE
# =========================================================

def prepare_image(image):

    if image is None:
        return []

    images = []

    # Original
    images.append(image)

    # Grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    images.append(gray)

    # Slight blur
    blur = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    images.append(blur)

    # OTSU threshold
    _, otsu = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    images.append(otsu)

    # Adaptive threshold
    adaptive = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        5
    )

    images.append(adaptive)

    # Sharpen image
    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (3, 3)
    )

    sharpened = cv2.morphologyEx(
        gray,
        cv2.MORPH_CLOSE,
        kernel
    )

    images.append(sharpened)

    # Enlarged versions
    height, width = gray.shape[:2]

    if width < 1200 or height < 1200:

        scale = 2

        enlarged = cv2.resize(
            image,
            None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_CUBIC
        )

        images.append(enlarged)

        enlarged_gray = cv2.cvtColor(
            enlarged,
            cv2.COLOR_BGR2GRAY
        )

        images.append(enlarged_gray)

        _, enlarged_binary = cv2.threshold(
            enlarged_gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        images.append(enlarged_binary)

    return images


# =========================================================
# SINGLE IMAGE DECODER
# =========================================================

def decode_single_image(detector, image):

    if image is None:
        return ""

    try:

        data, points, _ = detector.detectAndDecode(
            image
        )

        data = clean_qr_data(data)

        if data:
            return data

    except Exception:
        pass

    return ""


# =========================================================
# MULTIPLE QR DECODER
# =========================================================

def decode_multiple_images(detector, image):

    try:

        result = detector.detectAndDecodeMulti(
            image
        )

        if not result:
            return []

        retval, decoded_info, points, _ = result

        if not retval:
            return []

        results = []

        for item in decoded_info:

            item = clean_qr_data(item)

            if item and item not in results:
                results.append(item)

        return results

    except Exception:
        return []


# =========================================================
# ROTATION SUPPORT
# =========================================================

def rotated_images(image):

    results = []

    try:

        results.append(
            cv2.rotate(
                image,
                cv2.ROTATE_90_CLOCKWISE
            )
        )

        results.append(
            cv2.rotate(
                image,
                cv2.ROTATE_90_COUNTERCLOCKWISE
            )
        )

        results.append(
            cv2.rotate(
                image,
                cv2.ROTATE_180
            )
        )

    except Exception:
        pass

    return results


# =========================================================
# MAIN QR DECODER
# =========================================================

def decode_qr(file_path):

    if not file_path:

        return {
            "success": False,
            "message": "No QR image was provided.",
            "data": "",
            "type": "Unknown"
        }


    if not os.path.exists(file_path):

        return {
            "success": False,
            "message": "QR image file was not found.",
            "data": "",
            "type": "Unknown"
        }


    try:

        image = cv2.imread(
            file_path,
            cv2.IMREAD_COLOR
        )

        if image is None:

            return {
                "success": False,
                "message": "Unable to read the uploaded image.",
                "data": "",
                "type": "Unknown"
            }


        detector = cv2.QRCodeDetector()


        # =================================================
        # ATTEMPT 1
        # Original + processed images
        # =================================================

        images = prepare_image(
            image
        )

        for current_image in images:

            # Single QR
            decoded = decode_single_image(
                detector,
                current_image
            )

            if decoded:

                return {
                    "success": True,
                    "message": "QR code detected successfully.",
                    "data": decoded,
                    "type": detect_qr_type(decoded)
                }


            # Multiple QR
            multiple_results = decode_multiple_images(
                detector,
                current_image
            )

            if multiple_results:

                decoded = multiple_results[0]

                return {
                    "success": True,
                    "message": "QR code detected successfully.",
                    "data": decoded,
                    "type": detect_qr_type(decoded)
                }


        # =================================================
        # ATTEMPT 2
        # Rotated screenshots / photos
        # =================================================

        rotations = rotated_images(
            image
        )

        for rotated in rotations:

            rotated_images_list = prepare_image(
                rotated
            )

            for current_image in rotated_images_list:

                decoded = decode_single_image(
                    detector,
                    current_image
                )

                if decoded:

                    return {
                        "success": True,
                        "message": "QR code detected successfully.",
                        "data": decoded,
                        "type": detect_qr_type(decoded)
                    }


                multiple_results = decode_multiple_images(
                    detector,
                    current_image
                )

                if multiple_results:

                    decoded = multiple_results[0]

                    return {
                        "success": True,
                        "message": "QR code detected successfully.",
                        "data": decoded,
                        "type": detect_qr_type(decoded)
                    }


        # =================================================
        # QR NOT FOUND
        # =================================================

        return {
            "success": False,
            "message": (
                "No QR code was detected in this image. "
                "Please upload a clear QR screenshot, "
                "photo or QR code image."
            ),
            "data": "",
            "type": "Unknown"
        }


    except Exception as e:

        print(
            "QR DECODER ERROR:",
            e
        )

        return {
            "success": False,
            "message": (
                "Unable to analyze the QR image. "
                "Please try another clear image."
            ),
            "data": "",
            "type": "Unknown"
        }
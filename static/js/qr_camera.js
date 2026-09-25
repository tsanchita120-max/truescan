let scannedValue = "";
let scanner = null;

function onScanSuccess(decodedText) {

    scannedValue = decodedText;

    const resultBox = document.getElementById("result-box");
    const qrResult = document.getElementById("qr-result");
    const status = document.getElementById("scan-status");

    qrResult.textContent = decodedText;

    resultBox.style.display = "block";

    status.innerHTML =
        '<span class="status-circle"></span> QR Code detected successfully!';

    status.style.color = "#29d889";
}

function onScanFailure(error) {
    // QR code not detected yet
}

function startCamera() {

    const reader = document.getElementById("reader");
    const status = document.getElementById("scan-status");

    if (!reader) {
        console.error("Reader element not found");
        return;
    }

    if (typeof Html5Qrcode === "undefined") {
        status.textContent =
            "QR scanner library is not loaded.";
        return;
    }

    scanner = new Html5Qrcode("reader");

    const config = {
        fps: 10,
        qrbox: {
            width: 250,
            height: 250
        },
        aspectRatio: 1.0
    };

    scanner.start(
        { facingMode: "environment" },
        config,
        onScanSuccess,
        onScanFailure
    )
    .then(function () {

        status.innerHTML =
            '<span class="status-circle"></span> Camera is active. Point it at a QR code.';

        status.style.color = "#29d889";

    })
    .catch(function (error) {

        console.error("Camera error:", error);

        status.textContent =
            "Camera could not start. Please allow camera access.";

        status.style.color = "#ff6b6b";
    });
}


/* Start camera after page loads */
document.addEventListener("DOMContentLoaded", function () {

    setTimeout(function () {
        startCamera();
    }, 300);

});


function checkResult() {

    if (!scannedValue) {
        alert("No QR code detected.");
        return;
    }

    let risk = 10;

    const suspiciousWords = [
        "free",
        "winner",
        "prize",
        "claim",
        "reward",
        "verify",
        "urgent",
        "login"
    ];

    const text = scannedValue.toLowerCase();

    suspiciousWords.forEach(function(word) {

        if (text.includes(word)) {
            risk += 15;
        }

    });

    if (risk > 100) {
        risk = 100;
    }

    let status;

    if (risk >= 50) {
        status = "Dangerous";
    }
    else if (risk >= 30) {
        status = "Suspicious";
    }
    else {
        status = "Safe";
    }

    alert(
        "QR Analysis\n\n" +
        "Data: " + scannedValue +
        "\n\nRisk Score: " + risk + "/100" +
        "\nStatus: " + status
    );
}

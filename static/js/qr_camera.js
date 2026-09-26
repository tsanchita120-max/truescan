let scannedValue = "";
let scanner = null;
let scanCompleted = false;


// =====================================================
// QR SUCCESS
// =====================================================

function onScanSuccess(decodedText) {

    if (scanCompleted) {
        return;
    }

    if (!decodedText) {
        return;
    }

    scannedValue = decodedText.trim();
    scanCompleted = true;

    console.log("QR DETECTED:", scannedValue);

    const resultBox =
        document.getElementById("result-box");

    const qrResult =
        document.getElementById("qr-result");

    const status =
        document.getElementById("scan-status");


    // Show detected QR
    if (qrResult) {

        qrResult.textContent =
            scannedValue;
    }


    // Show result box
    if (resultBox) {

        resultBox.style.display =
            "block";
    }


    // Update status
    if (status) {

        status.innerHTML =
            '<span class="status-circle"></span> QR Code detected successfully!';

        status.style.color =
            "#29d889";
    }


    // Stop camera
    stopCamera();


    // Send to Python
    setTimeout(function () {

        sendToPython();

    }, 400);
}


// =====================================================
// QR FAILURE
// =====================================================

function onScanFailure(error) {

    // Continuous scanner errors are ignored.
}


// =====================================================
// START CAMERA
// =====================================================

function startCamera() {

    if (typeof Html5Qrcode === "undefined") {

        const status =
            document.getElementById(
                "scan-status"
            );

        if (status) {

            status.textContent =
                "Camera scanner library could not load.";
        }

        return;
    }


    const reader =
        document.getElementById("reader");


    if (!reader) {

        console.error(
            "QR reader element not found."
        );

        return;
    }


    scanner =
        new Html5Qrcode("reader");


    const config = {

        fps: 10,

        qrbox: {
            width: 250,
            height: 250
        },

        aspectRatio: 1.0
    };


    scanner.start(

        {
            facingMode: "environment"
        },

        config,

        onScanSuccess,

        onScanFailure

    )

    .then(function () {

        console.log(
            "Camera started successfully."
        );


        const status =
            document.getElementById(
                "scan-status"
            );


        if (status) {

            status.innerHTML =
                '<span class="status-circle"></span> Camera is active. Point it at a QR code.';

            status.style.color =
                "#29d889";
        }

    })

    .catch(function (error) {

        console.error(
            "CAMERA ERROR:",
            error
        );


        const status =
            document.getElementById(
                "scan-status"
            );


        if (status) {

            status.textContent =
                "Camera permission denied or unavailable.";

            status.style.color =
                "#ff6b6b";
        }
    });
}


// =====================================================
// STOP CAMERA
// =====================================================

function stopCamera() {

    if (!scanner) {
        return;
    }


    scanner.stop()

        .then(function () {

            console.log(
                "Camera stopped."
            );

        })

        .catch(function (error) {

            console.log(
                "Camera stop error:",
                error
            );
        });
}


// =====================================================
// SEND QR TO PYTHON BACKEND
// =====================================================

function sendToPython() {

    if (!scannedValue) {

        console.error(
            "No QR data available."
        );

        return;
    }


    console.log(
        "Sending QR to Python:",
        scannedValue
    );


    // Create POST form
    const form =
        document.createElement("form");


    form.method =
        "POST";


    form.action =
        "/analyze-qr";


    // QR data
    const input =
        document.createElement("input");


    input.type =
        "hidden";


    input.name =
        "qr_data";


    input.value =
        scannedValue;


    form.appendChild(
        input
    );


    document.body.appendChild(
        form
    );


    // Submit to Flask
    form.submit();
}


// =====================================================
// MANUAL ANALYZE BUTTON
// =====================================================

function checkResult() {

    if (!scannedValue) {

        alert(
            "No QR code detected."
        );

        return;
    }


    sendToPython();
}


// =====================================================
// PAGE LOAD
// =====================================================

window.addEventListener(
    "load",
    function () {

        console.log(
            "TRUESCAN QR CAMERA LOADED"
        );


        setTimeout(
            function () {

                startCamera();

            },
            500
        );
    }
);
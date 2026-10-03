let scanner = null;
let scannedValue = "";
let scanCompleted = false;
let cameraRunning = false;


/* =========================================================
   ELEMENT HELPER
========================================================= */

function getElement(id) {
    return document.getElementById(id);
}


/* =========================================================
   STATUS
========================================================= */

function setStatus(message, color) {

    const status = getElement("scan-status");

    if (status) {

        status.textContent = message;

        status.style.color =
            color || "#91a5bc";
    }
}


/* =========================================================
   QR DETECTED
========================================================= */

function onScanSuccess(decodedText, decodedResult) {

    if (scanCompleted) {
        return;
    }

    if (!decodedText) {
        return;
    }

    decodedText = decodedText.trim();

    if (!decodedText) {
        return;
    }


    /* -----------------------------------------------
       SAVE QR DATA
    ----------------------------------------------- */

    scannedValue = decodedText;

    scanCompleted = true;


    console.log("--------------------------------");
    console.log("TRUESCAN QR DETECTED");
    console.log("QR DATA:", scannedValue);
    console.log("--------------------------------");


    /* -----------------------------------------------
       SHOW RESULT BOX
    ----------------------------------------------- */

    const resultBox =
        getElement("result-box");

    const qrResult =
        getElement("qr-result");


    if (qrResult) {

        qrResult.textContent =
            scannedValue;
    }


    if (resultBox) {

        resultBox.style.display =
            "block";
    }


    /* -----------------------------------------------
       ENABLE ANALYZE BUTTON
    ----------------------------------------------- */

    const analyzeButton =
        document.querySelector(".analyze-btn");


    if (analyzeButton) {

        analyzeButton.disabled =
            false;

        analyzeButton.textContent =
            "🔍 Analyze QR Code";
    }


    /* -----------------------------------------------
       STATUS
    ----------------------------------------------- */

    setStatus(
        "QR Code detected successfully. Click Analyze QR Code.",
        "#29d889"
    );


    /* -----------------------------------------------
       STOP CAMERA
    ----------------------------------------------- */

    stopCamera();

}


/* =========================================================
   SCAN FAILURE
========================================================= */

function onScanFailure(error) {

    /*
       html5-qrcode calls this repeatedly when
       there is no QR code in the current frame.

       Do not show an error for every frame.
    */

    if (!scanCompleted) {

        setStatus(
            "Scanning... Keep the QR code inside the scan area.",
            "#55b7ff"
        );
    }
}


/* =========================================================
   START CAMERA
========================================================= */

async function startCamera() {

    console.log("--------------------------------");
    console.log("TRUESCAN CAMERA STARTING");
    console.log("--------------------------------");


    const reader =
        getElement("reader");


    if (!reader) {

        console.error(
            "ERROR: #reader element not found."
        );

        setStatus(
            "Scanner area not found.",
            "#ff6b6b"
        );

        return;
    }


    /* -----------------------------------------------
       CHECK LIBRARY
    ----------------------------------------------- */

    if (typeof Html5Qrcode === "undefined") {

        console.error(
            "ERROR: Html5Qrcode library is not loaded."
        );

        setStatus(
            "QR scanner library could not load.",
            "#ff6b6b"
        );

        return;
    }


    if (scanner) {
        return;
    }


    setStatus(
        "Starting camera...",
        "#55b7ff"
    );


    try {

        scanner =
            new Html5Qrcode("reader");


        /* -------------------------------------------
           RESPONSIVE QR BOX
        ------------------------------------------- */

        const config = {

            fps: 15,

            qrbox: function (
                viewfinderWidth,
                viewfinderHeight
            ) {

                const size =
                    Math.floor(
                        Math.min(
                            viewfinderWidth,
                            viewfinderHeight
                        ) * 0.70
                    );

                return {
                    width: size,
                    height: size
                };
            },

            aspectRatio: 1.0,

            disableFlip: false,

            formatsToSupport: [
                Html5QrcodeSupportedFormats.QR_CODE
            ]

        };


        /* -------------------------------------------
           TRY BACK CAMERA
        ------------------------------------------- */

        await scanner.start(

            {
                facingMode: "environment"
            },

            config,

            onScanSuccess,

            onScanFailure

        );


        cameraRunning = true;


        console.log(
            "CAMERA STARTED SUCCESSFULLY"
        );


        setStatus(
            "Camera active. Point the camera at a QR code.",
            "#29d889"
        );


    }

    catch (error) {

        console.error(
            "PRIMARY CAMERA ERROR:",
            error
        );


        /* -------------------------------------------
           FALLBACK TO AVAILABLE CAMERA
        ------------------------------------------- */

        try {

            if (scanner) {

                try {

                    await scanner.clear();

                } catch (e) {

                    console.warn(
                        "Scanner clear warning:",
                        e
                    );
                }

            }


            scanner = null;


            const cameras =
                await Html5Qrcode.getCameras();


            console.log(
                "AVAILABLE CAMERAS:",
                cameras
            );


            if (!cameras || cameras.length === 0) {

                throw new Error(
                    "No camera detected."
                );
            }


            /* ---------------------------------------
               SELECT CAMERA
            --------------------------------------- */

            let selectedCamera =
                cameras[0];


            for (
                const camera of cameras
            ) {

                const label =
                    (camera.label || "").toLowerCase();


                if (
                    label.includes("back") ||
                    label.includes("rear") ||
                    label.includes("environment")
                ) {

                    selectedCamera =
                        camera;

                    break;
                }
            }


            console.log(
                "SELECTED CAMERA:",
                selectedCamera
            );


            scanner =
                new Html5Qrcode("reader");


            await scanner.start(

                selectedCamera.id,

                config,

                onScanSuccess,

                onScanFailure

            );


            cameraRunning = true;


            console.log(
                "FALLBACK CAMERA STARTED"
            );


            setStatus(
                "Camera active. Point the camera at a QR code.",
                "#29d889"
            );


        }

        catch (fallbackError) {

            console.error(
                "FALLBACK CAMERA ERROR:",
                fallbackError
            );


            scanner = null;

            cameraRunning = false;


            setStatus(
                "Camera could not start. Please allow camera permission.",
                "#ff6b6b"
            );
        }
    }
}


/* =========================================================
   STOP CAMERA
========================================================= */

async function stopCamera() {

    if (!scanner) {
        return;
    }


    try {

        if (cameraRunning) {

            await scanner.stop();

            console.log(
                "CAMERA STOPPED"
            );
        }


        cameraRunning = false;


    }

    catch (error) {

        console.warn(
            "CAMERA STOP WARNING:",
            error
        );

    }
}


/* =========================================================
   ANALYZE QR
========================================================= */

function checkResult() {

    console.log("--------------------------------");
    console.log("ANALYZE BUTTON CLICKED");
    console.log("--------------------------------");


    if (!scannedValue) {

        setStatus(
            "No QR code detected.",
            "#ff6b6b"
        );

        alert(
            "No QR code detected. Please scan a QR code first."
        );

        return;
    }


    console.log(
        "QR DATA:",
        scannedValue
    );


    /* -----------------------------------------------
       GET FLASK ENDPOINT
    ----------------------------------------------- */

    const reader =
        getElement("reader");


    let endpoint =
        "/analyze-qr";


    if (
        reader &&
        reader.dataset &&
        reader.dataset.analyzeUrl
    ) {

        endpoint =
            reader.dataset.analyzeUrl;
    }


    console.log(
        "FLASK ENDPOINT:",
        endpoint
    );


    /* -----------------------------------------------
       DISABLE BUTTON
    ----------------------------------------------- */

    const button =
        document.querySelector(".analyze-btn");


    if (button) {

        button.disabled =
            true;

        button.textContent =
            "🔄 Analyzing QR...";

    }


    setStatus(
        "TRUESCAN is analyzing the QR code...",
        "#55b7ff"
    );


    /* -----------------------------------------------
       CREATE POST FORM
    ----------------------------------------------- */

    const form =
        document.createElement("form");


    form.method =
        "POST";


    form.action =
        endpoint;


    const input =
        document.createElement("input");


    input.type =
        "hidden";


    input.name =
        "qr_data";


    input.value =
        scannedValue;


    form.appendChild(input);


    document.body.appendChild(form);


    console.log(
        "SENDING QR DATA TO FLASK..."
    );


    /* -----------------------------------------------
       SEND
    ----------------------------------------------- */

    form.submit();
}


/* =========================================================
   PAGE LOAD
========================================================= */

window.addEventListener(
    "load",
    function () {

        console.log("--------------------------------");
        console.log("TRUESCAN QR CAMERA PAGE LOADED");
        console.log("--------------------------------");


        scannedValue = "";

        scanCompleted = false;


        const resultBox =
            getElement("result-box");


        if (resultBox) {

            resultBox.style.display =
                "none";
        }


        const button =
            document.querySelector(".analyze-btn");


        if (button) {

            button.disabled =
                true;

            button.textContent =
                "🔍 Analyze QR Code";
        }


        startCamera();
    }
);


/* =========================================================
   STOP CAMERA WHEN PAGE CLOSES
========================================================= */

window.addEventListener(
    "beforeunload",
    function () {

        stopCamera();

    }
);
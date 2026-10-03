document.addEventListener("DOMContentLoaded", function () {

    const languageSelect = document.getElementById("languageSelect");

    const translations = {

        en: {

            dashboardTitle: "TRUESCAN | Dashboard",

            tagline: "SCAN • DETECT • PROTECT",

            logout: "Logout",

            securityDashboard: "SECURITY DASHBOARD",

            welcome: "Welcome",

            welcomeDescription:
                "Detect suspicious QR codes and links before they become a threat.",

            securityScanner: "Security Scanner",

            chooseSecurityTool:
                "Choose a security tool",

            qrCamera:
                "QR Camera Scan",

            qrCameraDesc:
                "Scan a QR code directly using your device camera.",

            qrImage:
                "QR Image Upload",

            qrImageDesc:
                "Upload a QR image and analyze its content.",

            qrScreenshot:
                "QR Screenshot Analyzer",

            qrScreenshotDesc:
                "Upload a screenshot and automatically detect the QR code.",

            linkChecker:
                "Link Checker",

            linkCheckerDesc:
                "Check a website or suspicious URL for risk indicators.",

            reportScam:
                "Report Scam",

            reportScamDesc:
                "Report a suspicious QR code, website or online scam.",

            dailyStatistics:
                "Daily Scan Statistics",

            lastSevenDaysActivity:
                "Your scan activity for the last 7 days",

            lastSevenDays:
                "Last 7 Days",

            scan:
                "scan",

            scans:
                "scans",

            noScanActivity:
                "No scan activity available yet.",

            recentScans:
                "Recent Scans",

            latestSecurityActivity:
                "Your latest security activity",

            viewAll:
                "View All",

            safe:
                "Safe",

            suspicious:
                "Suspicious",

            dangerous:
                "Dangerous",

            noRecentScans:
                "No Recent Scans",

            recentScansDescription:
                "Your QR and link security activity will appear here.",

            home:
                "Home",

            history:
                "History",

            profile:
                "Profile"
        },


        mr: {

            dashboardTitle:
                "TRUESCAN | डॅशबोर्ड",

            tagline:
                "स्कॅन • शोधा • सुरक्षित रहा",

            logout:
                "बाहेर पडा",

            securityDashboard:
                "सुरक्षा डॅशबोर्ड",

            welcome:
                "स्वागत आहे",

            welcomeDescription:
                "धोका निर्माण होण्यापूर्वी संशयास्पद QR कोड आणि लिंक शोधा.",

            securityScanner:
                "सुरक्षा स्कॅनर",

            chooseSecurityTool:
                "सुरक्षा साधन निवडा",

            qrCamera:
                "QR कॅमेरा स्कॅन",

            qrCameraDesc:
                "तुमच्या डिव्हाइसच्या कॅमेऱ्याचा वापर करून QR कोड थेट स्कॅन करा.",

            qrImage:
                "QR इमेज अपलोड",

            qrImageDesc:
                "QR इमेज अपलोड करा आणि त्यातील माहितीचे विश्लेषण करा.",

            qrScreenshot:
                "QR स्क्रीनशॉट विश्लेषक",

            qrScreenshotDesc:
                "स्क्रीनशॉट अपलोड करा आणि त्यातील QR कोड आपोआप शोधा.",

            linkChecker:
                "लिंक तपासणी",

            linkCheckerDesc:
                "वेबसाइट किंवा संशयास्पद URL मधील सुरक्षा धोके तपासा.",

            reportScam:
                "फसवणुकीची तक्रार",

            reportScamDesc:
                "संशयास्पद QR कोड, वेबसाइट किंवा ऑनलाइन फसवणुकीची तक्रार करा.",

            dailyStatistics:
                "दैनंदिन स्कॅन आकडेवारी",

            lastSevenDaysActivity:
                "मागील 7 दिवसांतील तुमची स्कॅन गतिविधी",

            lastSevenDays:
                "मागील 7 दिवस",

            scan:
                "स्कॅन",

            scans:
                "स्कॅन",

            noScanActivity:
                "अजून कोणतीही स्कॅन गतिविधी उपलब्ध नाही.",

            recentScans:
                "अलीकडील स्कॅन",

            latestSecurityActivity:
                "तुमची अलीकडील सुरक्षा गतिविधी",

            viewAll:
                "सर्व पहा",

            safe:
                "सुरक्षित",

            suspicious:
                "संशयास्पद",

            dangerous:
                "धोकादायक",

            noRecentScans:
                "अलीकडील स्कॅन नाहीत",

            recentScansDescription:
                "तुमची QR आणि लिंक सुरक्षा गतिविधी येथे दिसेल.",

            home:
                "मुख्यपृष्ठ",

            history:
                "इतिहास",

            profile:
                "प्रोफाइल"
        },


        hi: {

            dashboardTitle:
                "TRUESCAN | डैशबोर्ड",

            tagline:
                "स्कैन • पहचानें • सुरक्षित रहें",

            logout:
                "लॉग आउट",

            securityDashboard:
                "सुरक्षा डैशबोर्ड",

            welcome:
                "स्वागत है",

            welcomeDescription:
                "खतरा बनने से पहले संदिग्ध QR कोड और लिंक की पहचान करें।",

            securityScanner:
                "सुरक्षा स्कैनर",

            chooseSecurityTool:
                "सुरक्षा टूल चुनें",

            qrCamera:
                "QR कैमरा स्कैन",

            qrCameraDesc:
                "अपने डिवाइस के कैमरे से सीधे QR कोड स्कैन करें।",

            qrImage:
                "QR इमेज अपलोड",

            qrImageDesc:
                "QR इमेज अपलोड करें और उसकी जानकारी का विश्लेषण करें।",

            qrScreenshot:
                "QR स्क्रीनशॉट विश्लेषक",

            qrScreenshotDesc:
                "स्क्रीनशॉट अपलोड करें और QR कोड को अपने आप पहचानें।",

            linkChecker:
                "लिंक चेकर",

            linkCheckerDesc:
                "वेबसाइट या संदिग्ध URL के सुरक्षा जोखिमों की जाँच करें।",

            reportScam:
                "स्कैम रिपोर्ट करें",

            reportScamDesc:
                "संदिग्ध QR कोड, वेबसाइट या ऑनलाइन स्कैम की रिपोर्ट करें।",

            dailyStatistics:
                "दैनिक स्कैन आँकड़े",

            lastSevenDaysActivity:
                "पिछले 7 दिनों की आपकी स्कैन गतिविधि",

            lastSevenDays:
                "पिछले 7 दिन",

            scan:
                "स्कैन",

            scans:
                "स्कैन",

            noScanActivity:
                "अभी तक कोई स्कैन गतिविधि उपलब्ध नहीं है।",

            recentScans:
                "हाल के स्कैन",

            latestSecurityActivity:
                "आपकी हाल की सुरक्षा गतिविधि",

            viewAll:
                "सभी देखें",

            safe:
                "सुरक्षित",

            suspicious:
                "संदिग्ध",

            dangerous:
                "खतरनाक",

            noRecentScans:
                "कोई हाल का स्कैन नहीं",

            recentScansDescription:
                "आपकी QR और लिंक सुरक्षा गतिविधि यहाँ दिखाई देगी।",

            home:
                "होम",

            history:
                "इतिहास",

            profile:
                "प्रोफ़ाइल"
        }

    };


    function applyLanguage(language) {

        if (!translations[language]) {
            language = "en";
        }

        const selectedTranslations =
            translations[language];


        /*
         * Normal text translation
         */

        document
            .querySelectorAll("[data-i18n]")
            .forEach(function (element) {

                const key =
                    element.getAttribute("data-i18n");

                if (
                    selectedTranslations[key] !== undefined
                ) {

                    element.textContent =
                        selectedTranslations[key];

                }

            });


        /*
         * Page title
         */

        if (
            selectedTranslations.dashboardTitle
        ) {

            document.title =
                selectedTranslations.dashboardTitle;

        }


        /*
         * HTML language attribute
         */

        document.documentElement.lang =
            language;


        /*
         * Save locally
         */

        localStorage.setItem(
            "truescan_language",
            language
        );


        /*
         * Save language in Flask session
         */

        fetch("/set-language", {

            method: "POST",

            headers: {
                "Content-Type":
                    "application/x-www-form-urlencoded"
            },

            body:
                "language=" +
                encodeURIComponent(language)

        }).catch(function (error) {

            console.log(
                "Language session update failed:",
                error
            );

        });

    }


    /*
     * Language selector
     */

    if (languageSelect) {

        languageSelect.addEventListener(
            "change",
            function () {

                applyLanguage(
                    this.value
                );

            }
        );

    }


    /*
     * Initial language
     *
     * Flask session has priority.
     */

    let initialLanguage =
        window.TRUESCAN_LANGUAGE;


    if (
        !initialLanguage ||
        !translations[initialLanguage]
    ) {

        initialLanguage =
            localStorage.getItem(
                "truescan_language"
            ) || "en";

    }


    if (languageSelect) {

        languageSelect.value =
            initialLanguage;

    }


    applyLanguage(
        initialLanguage
    );

});
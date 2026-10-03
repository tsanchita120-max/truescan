/* =========================================================
   TRUESCAN GLOBAL LANGUAGE SYSTEM
   English / Marathi / Hindi
   ========================================================= */

(function () {

    "use strict";


    /* =====================================================
       SUPPORTED LANGUAGES
       ===================================================== */

    const LANGUAGES = {
        en: "English",
        mr: "मराठी",
        hi: "हिन्दी"
    };


    /* =====================================================
       TRANSLATIONS
       ===================================================== */

    const translations = {

        /* ================= COMMON ================= */

        en: {

            online: "Online",
            offline: "Offline",
            logout: "Logout",
            back: "Back",
            save: "Save",
            cancel: "Cancel",
            submit: "Submit",
            delete: "Delete",
            close: "Close",
            loading: "Loading...",
            processing: "Processing...",
            success: "Success",
            error: "Error",
            warning: "Warning",
            language: "Language",

            home: "Home",
            history: "History",
            profile: "Profile",

            name: "Name",
            email: "Email",
            password: "Password",
            confirmPassword: "Confirm Password",
            date: "Date",
            status: "Status",
            type: "Type",
            content: "Content",
            result: "Result",
            user: "User",

            active: "Active",
            pending: "Pending",
            safe: "Safe",
            suspicious: "Suspicious",
            dangerous: "Dangerous",

            /* ================= AUTH ================= */

            login: "Login",
            register: "Register",
            createAccount: "Create Account",
            alreadyAccount: "Already have an account?",
            dontHaveAccount: "Don't have an account?",
            loginHere: "Login here",
            registerHere: "Register here",
            adminLogin: "Admin Login",
            administrator: "Administrator",

            /* ================= BRAND ================= */

            scanDetectProtect: "SCAN • DETECT • PROTECT",
            footer: "Your Digital Safety Partner",

            /* ================= DASHBOARD ================= */

            welcome: "Welcome",
            securityDashboard: "Security Dashboard",
            welcomeDescription:
                "Protect yourself from malicious QR codes and suspicious links.",

            securityScanner: "Security Scanner",
            chooseSecurityTool:
                "Choose a security tool to continue.",

            qrCamera: "QR Camera",
            qrCameraDesc:
                "Scan a QR code directly using your camera.",

            qrImage: "QR Image",
            qrImageDesc:
                "Upload an image containing a QR code.",

            qrScreenshot: "QR Screenshot",
            qrScreenshotDesc:
                "Analyze a screenshot and automatically detect the QR code.",

            linkChecker: "Link / URL Checker",
            linkCheckerDesc:
                "Check a link for suspicious or dangerous activity.",

            reportScam: "Report Scam",
            reportScamDesc:
                "Report a suspicious QR code or link.",

            recentScans: "Recent Scans",
            latestSecurityActivity: "Latest Security Activity",
            viewAll: "View All",
            noRecentScans: "No recent scans",
            noRecentScansDesc:
                "Your recent security activity will appear here.",

            dailyStatistics: "Daily Scan Statistics",
            lastSevenDays: "Last 7 Days",
            scan: "Scan",
            scans: "Scans",

            /* ================= CAMERA ================= */

            cameraScanner: "Camera Scanner",
            startCamera: "Start Camera",
            stopCamera: "Stop Camera",
            scanQrCode: "Scan QR Code",
            cameraPermission:
                "Please allow camera permission to scan QR codes.",
            cameraReady: "Camera ready",
            cameraScanning: "Scanning for QR code...",
            qrDetected: "QR Code detected! Opening result...",

            /* ================= UPLOAD ================= */

            uploadQr: "Upload QR",
            uploadImage: "Upload Image",
            chooseImage: "Choose Image",
            analyzeQr: "Analyze QR Image",
            qrNotDetected: "QR code not detected.",
            unableAnalyze:
                "Unable to analyze the image.",

            /* ================= SCREENSHOT ================= */

            screenshotAnalyzer: "QR Screenshot Analyzer",
            uploadScreenshot:
                "Upload Screenshot",

            /* ================= LINK ================= */

            linkAnalysis: "Link Analysis",
            enterUrl: "Enter URL or Link",
            checkLink: "Check Link",
            invalidUrl: "Invalid URL",

            /* ================= RESULT ================= */

            securityAnalysis: "Security Analysis",
            riskScore: "Risk Score",
            reasons: "Reasons",
            information: "Information",
            alerts: "Alerts",
            qrContent: "QR Content",
            qrType: "QR Type",
            protectYourself: "Protect Yourself",
            securityTip: "Security Tip",

            /* ================= HISTORY ================= */

            scanHistory: "Scan History",
            noData: "No data available",

            /* ================= PROFILE ================= */

            profileInformation: "Profile Information",
            accountInformation: "Account Information",
            updateProfile: "Update Profile",

            /* ================= SETTINGS ================= */

            securitySettings: "Security Settings",
            accountSettings: "Account Settings",
            privacySettings: "Privacy Settings",
            notificationSettings: "Notification Settings",

            /* ================= REPORT ================= */

            report: "Report",
            submitReport: "Submit Report",
            reportSuccess:
                "Your report has been submitted successfully.",
            reportedActivity:
                "Reported Suspicious Activity",
            noReports: "No reports found.",

            /* ================= ADMIN ================= */

            adminPanel: "Admin Panel",
            adminDashboardDescription:
                "Manage TRUESCAN security activity and monitor the system.",

            totalUsers: "Total Users",
            totalScans: "Total Scans",
            totalReports: "Total Reports",
            totalAlerts: "Total Alerts",

            users: "Users",
            registeredUsers: "Registered Users",
            reports: "Reports",
            noUsers: "No users found.",

            noRecentScansAdmin:
                "No recent scans found.",

            /* ================= NAVIGATION ================= */

            backToDashboard: "Back to Dashboard",

            /* ================= MISC ================= */

            selectLanguage: "Select Language",
            english: "English",
            marathi: "मराठी",
            hindi: "हिन्दी"

        },


        /* =================================================
           MARATHI
           ================================================= */

        mr: {

            online: "ऑनलाइन",
            offline: "ऑफलाइन",
            logout: "लॉगआउट",
            back: "मागे",
            save: "जतन करा",
            cancel: "रद्द करा",
            submit: "सबमिट करा",
            delete: "हटवा",
            close: "बंद करा",
            loading: "लोड होत आहे...",
            processing: "प्रक्रिया सुरू आहे...",
            success: "यशस्वी",
            error: "त्रुटी",
            warning: "चेतावणी",
            language: "भाषा",

            home: "होम",
            history: "इतिहास",
            profile: "प्रोफाइल",

            name: "नाव",
            email: "ईमेल",
            password: "पासवर्ड",
            confirmPassword: "पासवर्डची पुष्टी करा",
            date: "तारीख",
            status: "स्थिती",
            type: "प्रकार",
            content: "माहिती",
            result: "निकाल",
            user: "वापरकर्ता",

            active: "सक्रिय",
            pending: "प्रलंबित",
            safe: "सुरक्षित",
            suspicious: "संशयास्पद",
            dangerous: "धोकादायक",

            login: "लॉगिन",
            register: "नोंदणी",
            createAccount: "खाते तयार करा",
            alreadyAccount: "आधीच खाते आहे?",
            dontHaveAccount: "खाते नाही?",
            loginHere: "येथे लॉगिन करा",
            registerHere: "येथे नोंदणी करा",
            adminLogin: "ॲडमिन लॉगिन",
            administrator: "प्रशासक",

            scanDetectProtect: "स्कॅन • शोधा • सुरक्षित रहा",
            footer: "तुमचा डिजिटल सुरक्षा भागीदार",

            welcome: "स्वागत आहे",
            securityDashboard: "सुरक्षा डॅशबोर्ड",
            welcomeDescription:
                "धोकादायक QR कोड आणि संशयास्पद लिंकपासून स्वतःचे संरक्षण करा.",

            securityScanner: "सुरक्षा स्कॅनर",
            chooseSecurityTool:
                "सुरक्षा साधन निवडा.",

            qrCamera: "QR कॅमेरा",
            qrCameraDesc:
                "कॅमेऱ्याचा वापर करून थेट QR कोड स्कॅन करा.",

            qrImage: "QR इमेज",
            qrImageDesc:
                "QR कोड असलेली इमेज अपलोड करा.",

            qrScreenshot: "QR स्क्रीनशॉट",
            qrScreenshotDesc:
                "स्क्रीनशॉटचे विश्लेषण करून QR कोड आपोआप शोधा.",

            linkChecker: "लिंक / URL तपासणी",
            linkCheckerDesc:
                "लिंक संशयास्पद किंवा धोकादायक आहे का ते तपासा.",

            reportScam: "फसवणुकीची तक्रार",
            reportScamDesc:
                "संशयास्पद QR कोड किंवा लिंकची तक्रार करा.",

            recentScans: "अलीकडील स्कॅन",
            latestSecurityActivity: "अलीकडील सुरक्षा क्रिया",
            viewAll: "सर्व पहा",
            noRecentScans: "अलीकडील स्कॅन नाहीत",
            noRecentScansDesc:
                "तुमची अलीकडील सुरक्षा क्रिया येथे दिसेल.",

            dailyStatistics: "दैनंदिन स्कॅन आकडेवारी",
            lastSevenDays: "मागील ७ दिवस",
            scan: "स्कॅन",
            scans: "स्कॅन",

            cameraScanner: "कॅमेरा स्कॅनर",
            startCamera: "कॅमेरा सुरू करा",
            stopCamera: "कॅमेरा बंद करा",
            scanQrCode: "QR कोड स्कॅन करा",
            cameraPermission:
                "QR कोड स्कॅन करण्यासाठी कॅमेऱ्याची परवानगी द्या.",
            cameraReady: "कॅमेरा तयार आहे",
            cameraScanning: "QR कोड शोधत आहे...",
            qrDetected:
                "QR कोड सापडला! निकाल उघडत आहे...",

            uploadQr: "QR अपलोड करा",
            uploadImage: "इमेज अपलोड करा",
            chooseImage: "इमेज निवडा",
            analyzeQr: "QR इमेजचे विश्लेषण करा",
            qrNotDetected: "QR कोड सापडला नाही.",
            unableAnalyze:
                "इमेजचे विश्लेषण करता आले नाही.",

            screenshotAnalyzer: "QR स्क्रीनशॉट विश्लेषक",
            uploadScreenshot:
                "स्क्रीनशॉट अपलोड करा",

            linkAnalysis: "लिंक विश्लेषण",
            enterUrl: "URL किंवा लिंक टाका",
            checkLink: "लिंक तपासा",
            invalidUrl: "अवैध URL",

            securityAnalysis: "सुरक्षा विश्लेषण",
            riskScore: "जोखीम गुण",
            reasons: "कारणे",
            information: "माहिती",
            alerts: "अलर्ट",
            qrContent: "QR मधील माहिती",
            qrType: "QR प्रकार",
            protectYourself: "स्वतःचे संरक्षण करा",
            securityTip: "सुरक्षा सूचना",

            scanHistory: "स्कॅन इतिहास",
            noData: "माहिती उपलब्ध नाही",

            profileInformation: "प्रोफाइल माहिती",
            accountInformation: "खात्याची माहिती",
            updateProfile: "प्रोफाइल अपडेट करा",

            securitySettings: "सुरक्षा सेटिंग्ज",
            accountSettings: "खाते सेटिंग्ज",
            privacySettings: "गोपनीयता सेटिंग्ज",
            notificationSettings: "सूचना सेटिंग्ज",

            report: "तक्रार",
            submitReport: "तक्रार सबमिट करा",
            reportSuccess:
                "तुमची तक्रार यशस्वीरित्या सबमिट झाली.",
            reportedActivity:
                "संशयास्पद क्रियांची तक्रार",
            noReports: "तक्रारी उपलब्ध नाहीत.",

            adminPanel: "ॲडमिन पॅनेल",
            adminDashboardDescription:
                "TRUESCAN सुरक्षा क्रिया व्यवस्थापित करा आणि सिस्टमवर लक्ष ठेवा.",

            totalUsers: "एकूण वापरकर्ते",
            totalScans: "एकूण स्कॅन",
            totalReports: "एकूण तक्रारी",
            totalAlerts: "एकूण अलर्ट",

            users: "वापरकर्ते",
            registeredUsers: "नोंदणीकृत वापरकर्ते",
            reports: "तक्रारी",
            noUsers: "वापरकर्ते सापडले नाहीत.",

            noRecentScansAdmin:
                "अलीकडील स्कॅन सापडले नाहीत.",

            backToDashboard: "डॅशबोर्डवर परत जा",

            selectLanguage: "भाषा निवडा",
            english: "English",
            marathi: "मराठी",
            hindi: "हिन्दी"

        },


        /* =================================================
           HINDI
           ================================================= */

        hi: {

            online: "ऑनलाइन",
            offline: "ऑफलाइन",
            logout: "लॉगआउट",
            back: "वापस",
            save: "सहेजें",
            cancel: "रद्द करें",
            submit: "सबमिट करें",
            delete: "हटाएं",
            close: "बंद करें",
            loading: "लोड हो रहा है...",
            processing: "प्रक्रिया चल रही है...",
            success: "सफल",
            error: "त्रुटि",
            warning: "चेतावनी",
            language: "भाषा",

            home: "होम",
            history: "इतिहास",
            profile: "प्रोफाइल",

            name: "नाम",
            email: "ईमेल",
            password: "पासवर्ड",
            confirmPassword: "पासवर्ड की पुष्टि करें",
            date: "तारीख",
            status: "स्थिति",
            type: "प्रकार",
            content: "जानकारी",
            result: "परिणाम",
            user: "उपयोगकर्ता",

            active: "सक्रिय",
            pending: "लंबित",
            safe: "सुरक्षित",
            suspicious: "संदिग्ध",
            dangerous: "खतरनाक",

            login: "लॉगिन",
            register: "रजिस्टर",
            createAccount: "खाता बनाएं",
            alreadyAccount: "पहले से खाता है?",
            dontHaveAccount: "खाता नहीं है?",
            loginHere: "यहां लॉगिन करें",
            registerHere: "यहां रजिस्टर करें",
            adminLogin: "एडमिन लॉगिन",
            administrator: "प्रशासक",

            scanDetectProtect: "स्कैन • पहचानें • सुरक्षित रहें",
            footer: "आपका डिजिटल सुरक्षा साथी",

            welcome: "स्वागत है",
            securityDashboard: "सुरक्षा डैशबोर्ड",
            welcomeDescription:
                "खतरनाक QR कोड और संदिग्ध लिंक से खुद को सुरक्षित रखें.",

            securityScanner: "सुरक्षा स्कैनर",
            chooseSecurityTool:
                "सुरक्षा टूल चुनें.",

            qrCamera: "QR कैमरा",
            qrCameraDesc:
                "कैमरे का उपयोग करके सीधे QR कोड स्कैन करें.",

            qrImage: "QR इमेज",
            qrImageDesc:
                "QR कोड वाली इमेज अपलोड करें.",

            qrScreenshot: "QR स्क्रीनशॉट",
            qrScreenshotDesc:
                "स्क्रीनशॉट का विश्लेषण करके QR कोड अपने आप पहचानें.",

            linkChecker: "लिंक / URL चेकर",
            linkCheckerDesc:
                "लिंक संदिग्ध या खतरनाक है या नहीं जांचें.",

            reportScam: "स्कैम रिपोर्ट करें",
            reportScamDesc:
                "संदिग्ध QR कोड या लिंक की रिपोर्ट करें.",

            recentScans: "हाल के स्कैन",
            latestSecurityActivity: "हाल की सुरक्षा गतिविधि",
            viewAll: "सभी देखें",
            noRecentScans: "हाल के स्कैन नहीं हैं",
            noRecentScansDesc:
                "आपकी हाल की सुरक्षा गतिविधि यहां दिखाई देगी.",

            dailyStatistics: "दैनिक स्कैन आंकड़े",
            lastSevenDays: "पिछले 7 दिन",
            scan: "स्कैन",
            scans: "स्कैन",

            cameraScanner: "कैमरा स्कैनर",
            startCamera: "कैमरा शुरू करें",
            stopCamera: "कैमरा बंद करें",
            scanQrCode: "QR कोड स्कैन करें",
            cameraPermission:
                "QR कोड स्कैन करने के लिए कैमरा अनुमति दें.",
            cameraReady: "कैमरा तैयार है",
            cameraScanning: "QR कोड खोज रहा है...",
            qrDetected:
                "QR कोड मिल गया! परिणाम खोला जा रहा है...",

            uploadQr: "QR अपलोड करें",
            uploadImage: "इमेज अपलोड करें",
            chooseImage: "इमेज चुनें",
            analyzeQr: "QR इमेज का विश्लेषण करें",
            qrNotDetected: "QR कोड नहीं मिला.",
            unableAnalyze:
                "इमेज का विश्लेषण नहीं हो सका.",

            screenshotAnalyzer: "QR स्क्रीनशॉट विश्लेषक",
            uploadScreenshot:
                "स्क्रीनशॉट अपलोड करें",

            linkAnalysis: "लिंक विश्लेषण",
            enterUrl: "URL या लिंक दर्ज करें",
            checkLink: "लिंक जांचें",
            invalidUrl: "अमान्य URL",

            securityAnalysis: "सुरक्षा विश्लेषण",
            riskScore: "जोखिम स्कोर",
            reasons: "कारण",
            information: "जानकारी",
            alerts: "अलर्ट",
            qrContent: "QR जानकारी",
            qrType: "QR प्रकार",
            protectYourself: "खुद को सुरक्षित रखें",
            securityTip: "सुरक्षा सुझाव",

            scanHistory: "स्कैन इतिहास",
            noData: "कोई जानकारी उपलब्ध नहीं है",

            profileInformation: "प्रोफाइल जानकारी",
            accountInformation: "खाते की जानकारी",
            updateProfile: "प्रोफाइल अपडेट करें",

            securitySettings: "सुरक्षा सेटिंग्स",
            accountSettings: "खाता सेटिंग्स",
            privacySettings: "गोपनीयता सेटिंग्स",
            notificationSettings: "सूचना सेटिंग्स",

            report: "रिपोर्ट",
            submitReport: "रिपोर्ट सबमिट करें",
            reportSuccess:
                "आपकी रिपोर्ट सफलतापूर्वक सबमिट हो गई.",
            reportedActivity:
                "रिपोर्ट की गई संदिग्ध गतिविधि",
            noReports: "कोई रिपोर्ट नहीं मिली.",

            adminPanel: "एडमिन पैनल",
            adminDashboardDescription:
                "TRUESCAN सुरक्षा गतिविधि प्रबंधित करें और सिस्टम की निगरानी करें.",

            totalUsers: "कुल उपयोगकर्ता",
            totalScans: "कुल स्कैन",
            totalReports: "कुल रिपोर्ट",
            totalAlerts: "कुल अलर्ट",

            users: "उपयोगकर्ता",
            registeredUsers: "पंजीकृत उपयोगकर्ता",
            reports: "रिपोर्ट",
            noUsers: "कोई उपयोगकर्ता नहीं मिला.",

            noRecentScansAdmin:
                "हाल के स्कैन नहीं मिले.",

            backToDashboard: "डैशबोर्ड पर वापस जाएं",

            selectLanguage: "भाषा चुनें",
            english: "English",
            marathi: "मराठी",
            hindi: "हिन्दी"

        }

    };


    /* =====================================================
       GET LANGUAGE
       ===================================================== */

    function getLanguage() {

        let language =
            localStorage.getItem("truescanLanguage");

        if (!LANGUAGES[language]) {
            language = "en";
        }

        return language;
    }


    /* =====================================================
       TRANSLATE KEY
       ===================================================== */

    function translate(key, language) {

        language = language || getLanguage();

        if (
            translations[language] &&
            translations[language][key]
        ) {
            return translations[language][key];
        }

        if (translations.en[key]) {
            return translations.en[key];
        }

        return key;
    }


    /* =====================================================
       APPLY LANGUAGE
       ===================================================== */

    function applyLanguage(language) {

        if (!LANGUAGES[language]) {
            language = "en";
        }


        /* Save */

        localStorage.setItem(
            "truescanLanguage",
            language
        );


        /* HTML language */

        document.documentElement.lang = language;


        /* ================================================
           DATA-I18N
           ================================================ */

        document
            .querySelectorAll("[data-i18n]")
            .forEach(function (element) {

                const key =
                    element.getAttribute("data-i18n");

                const value =
                    translate(key, language);

                if (value) {
                    element.textContent = value;
                }

            });


        /* ================================================
           DATA-I18N-HTML
           ================================================ */

        document
            .querySelectorAll("[data-i18n-html]")
            .forEach(function (element) {

                const key =
                    element.getAttribute("data-i18n-html");

                const value =
                    translate(key, language);

                if (value) {
                    element.innerHTML = value;
                }

            });


        /* ================================================
           PLACEHOLDERS
           ================================================ */

        document
            .querySelectorAll("[data-i18n-placeholder]")
            .forEach(function (element) {

                const key =
                    element.getAttribute(
                        "data-i18n-placeholder"
                    );

                element.placeholder =
                    translate(key, language);

            });


        /* ================================================
           TITLES
           ================================================ */

        document
            .querySelectorAll("[data-i18n-title]")
            .forEach(function (element) {

                const key =
                    element.getAttribute(
                        "data-i18n-title"
                    );

                element.title =
                    translate(key, language);

            });


        /* ================================================
           SELECT LANGUAGE
           ================================================ */

        const selector =
            document.getElementById("languageSelect");

        if (selector) {
            selector.value = language;
        }


        /* ================================================
           SELECTORS WITH CLASS
           ================================================ */

        document
            .querySelectorAll(".language-select")
            .forEach(function (select) {

                select.value = language;

            });


        /* ================================================
           SEND LANGUAGE TO FLASK
           ================================================ */

        fetch("/set-language", {

            method: "POST",

            headers: {
                "Content-Type":
                    "application/x-www-form-urlencoded"
            },

            body:
                "language=" +
                encodeURIComponent(language)

        }).catch(function () {
            /* Flask session update is optional */
        });

    }


    /* =====================================================
       SAVE LANGUAGE
       ===================================================== */

    function saveLanguage(language) {

        applyLanguage(language);

    }


    /* =====================================================
       LANGUAGE SELECTOR
       ===================================================== */

    function setupLanguageSelector() {

        const selectors =
            document.querySelectorAll(
                "#languageSelect, .language-select"
            );


        selectors.forEach(function (selector) {

            selector.value = getLanguage();


            selector.addEventListener(
                "change",
                function () {

                    saveLanguage(this.value);

                }
            );

        });

    }


    /* =====================================================
       AUTO TRANSLATION FOR STATIC TEXT
       ===================================================== */

    const automaticText = {

        "Dashboard": "securityDashboard",
        "Security Dashboard": "securityDashboard",

        "Security Scanner": "securityScanner",
        "QR Camera": "qrCamera",
        "QR Image": "qrImage",
        "QR Screenshot": "qrScreenshot",
        "Link / URL Checker": "linkChecker",
        "Report Scam": "reportScam",

        "Recent Scans": "recentScans",
        "Latest Security Activity":
            "latestSecurityActivity",

        "Home": "home",
        "History": "history",
        "Profile": "profile",

        "Logout": "logout",
        "Online": "online",
        "Offline": "offline",

        "Back to Dashboard":
            "backToDashboard",

        "Camera Scanner": "cameraScanner",
        "Start Camera": "startCamera",
        "Stop Camera": "stopCamera",

        "Upload QR": "uploadQr",
        "Upload Image": "uploadImage",
        "Choose Image": "chooseImage",

        "Analyze QR Image": "analyzeQr",

        "QR Screenshot Analyzer":
            "screenshotAnalyzer",

        "Upload Screenshot":
            "uploadScreenshot",

        "Link Analysis": "linkAnalysis",
        "Enter URL or Link": "enterUrl",
        "Check Link": "checkLink",

        "Security Analysis":
            "securityAnalysis",

        "Risk Score": "riskScore",
        "Reasons": "reasons",
        "Information": "information",
        "Alerts": "alerts",

        "QR Content": "qrContent",
        "QR Type": "qrType",

        "Scan History": "scanHistory",

        "Profile Information":
            "profileInformation",

        "Account Information":
            "accountInformation",

        "Security Settings":
            "securitySettings",

        "Account Settings":
            "accountSettings",

        "Privacy Settings":
            "privacySettings",

        "Notification Settings":
            "notificationSettings",

        "Report": "report",
        "Submit Report": "submitReport",

        "Admin Panel": "adminPanel",
        "Total Users": "totalUsers",
        "Total Scans": "totalScans",
        "Total Reports": "totalReports",
        "Total Alerts": "totalAlerts",

        "Users": "users",
        "Registered Users":
            "registeredUsers",

        "Reports": "reports",
        "Pending": "pending",
        "Active": "active",

        "Safe": "safe",
        "Suspicious": "suspicious",
        "Dangerous": "dangerous",

        "Save": "save",
        "Cancel": "cancel",
        "Submit": "submit",
        "Delete": "delete",
        "Close": "close",

        "Login": "login",
        "Register": "register",
        "Create Account":
            "createAccount",

        "Admin Login":
            "adminLogin"

    };


    function autoTranslateTextNodes(language) {

        if (language === "en") {
            return;
        }


        const walker =
            document.createTreeWalker(
                document.body,
                NodeFilter.SHOW_TEXT
            );


        const nodes = [];

        let node;

        while (
            node = walker.nextNode()
        ) {

            nodes.push(node);

        }


        nodes.forEach(function (textNode) {

            const parent =
                textNode.parentElement;

            if (!parent) {
                return;
            }


            /* Ignore script/style */

            if (
                parent.tagName === "SCRIPT" ||
                parent.tagName === "STYLE" ||
                parent.tagName === "OPTION"
            ) {
                return;
            }


            const original =
                textNode.nodeValue.trim();


            if (!original) {
                return;
            }


            const key =
                automaticText[original];


            if (!key) {
                return;
            }


            const translated =
                translate(key, language);


            if (!translated) {
                return;
            }


            textNode.nodeValue =
                textNode.nodeValue.replace(
                    original,
                    translated
                );

        });

    }


    /* =====================================================
       INITIALIZE
       ===================================================== */

    function initialize() {

        const language =
            getLanguage();


        applyLanguage(language);


        setupLanguageSelector();


        /*
         * Also translate old pages which
         * don't yet have data-i18n.
         */

        autoTranslateTextNodes(language);

    }


    /* =====================================================
       STORAGE EVENT
       ===================================================== */

    window.addEventListener(
        "storage",
        function (event) {

            if (
                event.key ===
                "truescanLanguage"
            ) {

                applyLanguage(
                    event.newValue || "en"
                );

            }

        }
    );


    /* =====================================================
       PUBLIC FUNCTIONS
       ===================================================== */

    window.getTrueScanLanguage =
        getLanguage;

    window.translateTrueScan =
        translate;

    window.applyTrueScanLanguage =
        applyLanguage;

    window.saveTrueScanLanguage =
        saveLanguage;

    window.setupTrueScanLanguageSelector =
        setupLanguageSelector;


    /* =====================================================
       DOM READY
       ===================================================== */

    if (
        document.readyState ===
        "loading"
    ) {

        document.addEventListener(
            "DOMContentLoaded",
            initialize
        );

    } else {

        initialize();

    }


})();
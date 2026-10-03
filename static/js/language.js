(function () {
    "use strict";

    const STORAGE_KEY = "truescan_language";
    const SUPPORTED = ["en", "mr", "hi"];

    const translations = {

        /* =========================
           COMMON
        ========================= */

        "TRUESCAN": {
            en: "TRUESCAN",
            mr: "TRUESCAN",
            hi: "TRUESCAN"
        },

        "SCAN • DETECT • PROTECT": {
            en: "SCAN • DETECT • PROTECT",
            mr: "स्कॅन • शोधा • सुरक्षित रहा",
            hi: "स्कैन • पहचानें • सुरक्षित रहें"
        },

        "Online": {
            en: "Online",
            mr: "ऑनलाइन",
            hi: "ऑनलाइन"
        },

        "Logout": {
            en: "Logout",
            mr: "लॉगआउट",
            hi: "लॉगआउट"
        },

        "Back to Dashboard": {
            en: "Back to Dashboard",
            mr: "डॅशबोर्डवर परत जा",
            hi: "डैशबोर्ड पर वापस जाएँ"
        },

        "← Back to Dashboard": {
            en: "← Back to Dashboard",
            mr: "← डॅशबोर्डवर परत जा",
            hi: "← डैशबोर्ड पर वापस जाएँ"
        },

        "Home": {
            en: "Home",
            mr: "मुख्यपृष्ठ",
            hi: "होम"
        },

        "History": {
            en: "History",
            mr: "इतिहास",
            hi: "इतिहास"
        },

        "Profile": {
            en: "Profile",
            mr: "प्रोफाइल",
            hi: "प्रोफ़ाइल"
        },

        "View History →": {
            en: "View History →",
            mr: "इतिहास पहा →",
            hi: "इतिहास देखें →"
        },

        "© 2026 TRUESCAN": {
            en: "© 2026 TRUESCAN",
            mr: "© 2026 TRUESCAN",
            hi: "© 2026 TRUESCAN"
        },

        "Your Digital Safety Partner": {
            en: "Your Digital Safety Partner",
            mr: "तुमचा डिजिटल सुरक्षा साथीदार",
            hi: "आपका डिजिटल सुरक्षा साथी"
        },


        /* =========================
           DASHBOARD
        ========================= */

        "QR Code & Link Security": {
            en: "QR Code & Link Security",
            mr: "QR कोड आणि लिंक सुरक्षा",
            hi: "QR कोड और लिंक सुरक्षा"
        },

        "Welcome back": {
            en: "Welcome back",
            mr: "पुन्हा स्वागत आहे",
            hi: "आपका स्वागत है"
        },

        "Keep your QR codes and links safe with TRUESCAN.": {
            en: "Keep your QR codes and links safe with TRUESCAN.",
            mr: "TRUESCAN सोबत तुमचे QR कोड आणि लिंक सुरक्षित ठेवा.",
            hi: "TRUESCAN के साथ अपने QR कोड और लिंक सुरक्षित रखें।"
        },

        "Security Scanner": {
            en: "Security Scanner",
            mr: "सुरक्षा स्कॅनर",
            hi: "सुरक्षा स्कैनर"
        },

        "Scan QR codes and check links for security risks.": {
            en: "Scan QR codes and check links for security risks.",
            mr: "QR कोड स्कॅन करा आणि लिंकच्या सुरक्षा जोखमी तपासा.",
            hi: "QR कोड स्कैन करें और लिंक की सुरक्षा जाँचें।"
        },

        "QR Camera Scan": {
            en: "QR Camera Scan",
            mr: "QR कॅमेरा स्कॅन",
            hi: "QR कैमरा स्कैन"
        },

        "Scan a QR code directly using your camera.": {
            en: "Scan a QR code directly using your camera.",
            mr: "कॅमेराचा वापर करून थेट QR कोड स्कॅन करा.",
            hi: "अपने कैमरे से सीधे QR कोड स्कैन करें।"
        },

        "Start Scan →": {
            en: "Start Scan →",
            mr: "स्कॅन सुरू करा →",
            hi: "स्कैन शुरू करें →"
        },

        "QR Image Upload": {
            en: "QR Image Upload",
            mr: "QR प्रतिमा अपलोड",
            hi: "QR इमेज अपलोड"
        },

        "Upload a QR image and analyze its content.": {
            en: "Upload a QR image and analyze its content.",
            mr: "QR प्रतिमा अपलोड करा आणि तिचे विश्लेषण करा.",
            hi: "QR इमेज अपलोड करें और उसका विश्लेषण करें।"
        },

        "Upload Image →": {
            en: "Upload Image →",
            mr: "प्रतिमा अपलोड करा →",
            hi: "इमेज अपलोड करें →"
        },

        "Link / URL Checker": {
            en: "Link / URL Checker",
            mr: "लिंक / URL तपासणी",
            hi: "लिंक / URL चेकर"
        },

        "Check a URL for suspicious or unsafe patterns.": {
            en: "Check a URL for suspicious or unsafe patterns.",
            mr: "URL मधील संशयास्पद किंवा असुरक्षित बाबी तपासा.",
            hi: "URL में संदिग्ध या असुरक्षित संकेतों की जाँच करें।"
        },

        "Check Link →": {
            en: "Check Link →",
            mr: "लिंक तपासा →",
            hi: "लिंक जाँचें →"
        },

        "Report Spam": {
            en: "Report Spam",
            mr: "स्पॅम रिपोर्ट करा",
            hi: "स्पैम रिपोर्ट करें"
        },

        "Report a suspicious QR code or malicious link.": {
            en: "Report a suspicious QR code or malicious link.",
            mr: "संशयास्पद QR कोड किंवा धोकादायक लिंक रिपोर्ट करा.",
            hi: "संदिग्ध QR कोड या खतरनाक लिंक की रिपोर्ट करें।"
        },

        "Report Now →": {
            en: "Report Now →",
            mr: "आता रिपोर्ट करा →",
            hi: "अभी रिपोर्ट करें →"
        },

        "Security Overview": {
            en: "Security Overview",
            mr: "सुरक्षा आढावा",
            hi: "सुरक्षा अवलोकन"
        },

        "Your recent scanning activity.": {
            en: "Your recent scanning activity.",
            mr: "तुमची अलीकडील स्कॅनिंग activity.",
            hi: "आपकी हाल की स्कैनिंग गतिविधि।"
        },

        "Total Scans": {
            en: "Total Scans",
            mr: "एकूण स्कॅन",
            hi: "कुल स्कैन"
        },

        "Last 7 Days": {
            en: "Last 7 Days",
            mr: "मागील 7 दिवस",
            hi: "पिछले 7 दिन"
        },

        "Security Status": {
            en: "Security Status",
            mr: "सुरक्षा स्थिती",
            hi: "सुरक्षा स्थिति"
        },

        "Daily Scan Activity": {
            en: "Daily Scan Activity",
            mr: "दैनिक स्कॅन activity",
            hi: "दैनिक स्कैन गतिविधि"
        },

        "Your scans during the last 7 days.": {
            en: "Your scans during the last 7 days.",
            mr: "मागील 7 दिवसांमधील तुमचे स्कॅन.",
            hi: "पिछले 7 दिनों के आपके स्कैन।"
        },

        "scans": {
            en: "scans",
            mr: "स्कॅन",
            hi: "स्कैन"
        },

        "No scan activity yet.": {
            en: "No scan activity yet.",
            mr: "अजून कोणतीही स्कॅन activity नाही.",
            hi: "अभी तक कोई स्कैन गतिविधि नहीं है।"
        },

        "Recent Scans": {
            en: "Recent Scans",
            mr: "अलीकडील स्कॅन",
            hi: "हाल के स्कैन"
        },

        "Your latest security scan results.": {
            en: "Your latest security scan results.",
            mr: "तुमचे नवीनतम सुरक्षा स्कॅन परिणाम.",
            hi: "आपके नवीनतम सुरक्षा स्कैन परिणाम।"
        },

        "No Recent Scans": {
            en: "No Recent Scans",
            mr: "अलीकडील स्कॅन नाहीत",
            hi: "हाल के स्कैन नहीं हैं"
        },

        "Start a QR or link scan to see results here.": {
            en: "Start a QR or link scan to see results here.",
            mr: "परिणाम पाहण्यासाठी QR किंवा लिंक स्कॅन सुरू करा.",
            hi: "परिणाम देखने के लिए QR या लिंक स्कैन शुरू करें।"
        },


        /* =========================
           RISK
        ========================= */

        "Safe": {
            en: "Safe",
            mr: "सुरक्षित",
            hi: "सुरक्षित"
        },

        "Suspicious": {
            en: "Suspicious",
            mr: "संशयास्पद",
            hi: "संदिग्ध"
        },

        "Dangerous": {
            en: "Dangerous",
            mr: "धोकादायक",
            hi: "खतरनाक"
        },

        "Risky": {
            en: "Risky",
            mr: "जोखमीचे",
            hi: "जोखिमपूर्ण"
        },


        /* =========================
           QR CAMERA
        ========================= */

        "QR Camera Scanner": {
            en: "QR Camera Scanner",
            mr: "QR कॅमेरा स्कॅनर",
            hi: "QR कैमरा स्कैनर"
        },

        "Scan a QR code using your camera": {
            en: "Scan a QR code using your camera",
            mr: "कॅमेराचा वापर करून QR कोड स्कॅन करा",
            hi: "कैमरे का उपयोग करके QR कोड स्कैन करें"
        },

        "QR Code Detected": {
            en: "QR Code Detected",
            mr: "QR कोड सापडला",
            hi: "QR कोड मिला"
        },

        "QR data found successfully": {
            en: "QR data found successfully",
            mr: "QR डेटा यशस्वीरित्या सापडला",
            hi: "QR डेटा सफलतापूर्वक मिला"
        },

        "Detected Data": {
            en: "Detected Data",
            mr: "सापडलेला डेटा",
            hi: "मिला हुआ डेटा"
        },

        "Analyze QR Code": {
            en: "Analyze QR Code",
            mr: "QR कोडचे विश्लेषण करा",
            hi: "QR कोड का विश्लेषण करें"
        },

        "Point camera at QR": {
            en: "Point camera at QR",
            mr: "कॅमेरा QR कडे ठेवा",
            hi: "कैमरा QR की ओर रखें"
        },

        "Keep QR inside scan area": {
            en: "Keep QR inside scan area",
            mr: "QR स्कॅन क्षेत्राच्या आत ठेवा",
            hi: "QR को स्कैन क्षेत्र के अंदर रखें"
        },

        "Check security result": {
            en: "Check security result",
            mr: "सुरक्षा परिणाम तपासा",
            hi: "सुरक्षा परिणाम देखें"
        },


        /* =========================
           QR UPLOAD
        ========================= */

        "QR Image Upload": {
            en: "QR Image Upload",
            mr: "QR प्रतिमा अपलोड",
            hi: "QR इमेज अपलोड"
        },

        "Upload a QR code image to analyze it.": {
            en: "Upload a QR code image to analyze it.",
            mr: "विश्लेषण करण्यासाठी QR कोडची प्रतिमा अपलोड करा.",
            hi: "विश्लेषण के लिए QR कोड की इमेज अपलोड करें।"
        },

        "Upload QR Code Image": {
            en: "Upload QR Code Image",
            mr: "QR कोड प्रतिमा अपलोड करा",
            hi: "QR कोड इमेज अपलोड करें"
        },

        "Select PNG, JPG or JPEG image": {
            en: "Select PNG, JPG or JPEG image",
            mr: "PNG, JPG किंवा JPEG प्रतिमा निवडा",
            hi: "PNG, JPG या JPEG इमेज चुनें"
        },

        "Choose QR Image": {
            en: "Choose QR Image",
            mr: "QR प्रतिमा निवडा",
            hi: "QR इमेज चुनें"
        },

        "Image Preview": {
            en: "Image Preview",
            mr: "प्रतिमा पूर्वदृश्य",
            hi: "इमेज प्रीव्यू"
        },

        "Analyze QR Image": {
            en: "Analyze QR Image",
            mr: "QR प्रतिमेचे विश्लेषण करा",
            hi: "QR इमेज का विश्लेषण करें"
        },


        /* =========================
           LINK CHECKER
        ========================= */

        "Link Scam Checker": {
            en: "Link Scam Checker",
            mr: "लिंक सुरक्षा तपासणी",
            hi: "लिंक स्कैम चेकर"
        },

        "Check a website link for suspicious activity": {
            en: "Check a website link for suspicious activity",
            mr: "वेबसाइट लिंकची संशयास्पद activity तपासा",
            hi: "वेबसाइट लिंक की संदिग्ध गतिविधि जाँचें"
        },

        "Website / Link": {
            en: "Website / Link",
            mr: "वेबसाइट / लिंक",
            hi: "वेबसाइट / लिंक"
        },

        "Check Link Security": {
            en: "Check Link Security",
            mr: "लिंक सुरक्षा तपासा",
            hi: "लिंक सुरक्षा जाँचें"
        },

        "Enter website link": {
            en: "Enter website link",
            mr: "वेबसाइट लिंक प्रविष्ट करा",
            hi: "वेबसाइट लिंक दर्ज करें"
        },

        "Analyze suspicious signals": {
            en: "Analyze suspicious signals",
            mr: "संशयास्पद संकेतांचे विश्लेषण करा",
            hi: "संदिग्ध संकेतों का विश्लेषण करें"
        },

        "View security result": {
            en: "View security result",
            mr: "सुरक्षा परिणाम पहा",
            hi: "सुरक्षा परिणाम देखें"
        },

        "Never enter passwords, OTPs or banking details on suspicious websites.": {
            en: "Never enter passwords, OTPs or banking details on suspicious websites.",
            mr: "संशयास्पद वेबसाइटवर पासवर्ड, OTP किंवा बँकिंग माहिती कधीही टाकू नका.",
            hi: "संदिग्ध वेबसाइट पर पासवर्ड, OTP या बैंकिंग जानकारी कभी दर्ज न करें।"
        },


        /* =========================
           REPORT
        ========================= */

        "Report Scam": {
            en: "Report Scam",
            mr: "फसवणूक रिपोर्ट करा",
            hi: "स्कैम रिपोर्ट करें"
        },

        "Help us identify suspicious links and activities.": {
            en: "Help us identify suspicious links and activities.",
            mr: "संशयास्पद लिंक आणि activity ओळखण्यात आम्हाला मदत करा.",
            hi: "संदिग्ध लिंक और गतिविधियों की पहचान करने में हमारी मदद करें।"
        },

        "Scam Category": {
            en: "Scam Category",
            mr: "फसवणुकीचा प्रकार",
            hi: "स्कैम श्रेणी"
        },

        "Select scam type": {
            en: "Select scam type",
            mr: "फसवणुकीचा प्रकार निवडा",
            hi: "स्कैम प्रकार चुनें"
        },

        "QR Scam": {
            en: "QR Scam",
            mr: "QR फसवणूक",
            hi: "QR स्कैम"
        },

        "Link Scam": {
            en: "Link Scam",
            mr: "लिंक फसवणूक",
            hi: "लिंक स्कैम"
        },

        "Phishing": {
            en: "Phishing",
            mr: "फिशिंग",
            hi: "फिशिंग"
        },

        "Fake Payment": {
            en: "Fake Payment",
            mr: "बनावट पेमेंट",
            hi: "फर्जी भुगतान"
        },

        "Prize / Reward Scam": {
            en: "Prize / Reward Scam",
            mr: "बक्षीस / रिवॉर्ड फसवणूक",
            hi: "इनाम / रिवॉर्ड स्कैम"
        },

        "Other": {
            en: "Other",
            mr: "इतर",
            hi: "अन्य"
        },

        "Suspicious Link / URL": {
            en: "Suspicious Link / URL",
            mr: "संशयास्पद लिंक / URL",
            hi: "संदिग्ध लिंक / URL"
        },

        "Description": {
            en: "Description",
            mr: "वर्णन",
            hi: "विवरण"
        },

        "Submit Scam Report": {
            en: "Submit Scam Report",
            mr: "फसवणूक रिपोर्ट सबमिट करा",
            hi: "स्कैम रिपोर्ट सबमिट करें"
        },


        /* =========================
           HISTORY
        ========================= */

        "Scan History": {
            en: "Scan History",
            mr: "स्कॅन इतिहास",
            hi: "स्कैन इतिहास"
        },

        "View your previous QR and link security checks.": {
            en: "View your previous QR and link security checks.",
            mr: "तुमचे मागील QR आणि लिंक सुरक्षा तपासणी पहा.",
            hi: "अपने पिछले QR और लिंक सुरक्षा जाँच देखें।"
        },

        "No Scan History": {
            en: "No Scan History",
            mr: "स्कॅन इतिहास उपलब्ध नाही",
            hi: "कोई स्कैन इतिहास नहीं है"
        },

        "Your previous QR and link scans will appear here.": {
            en: "Your previous QR and link scans will appear here.",
            mr: "तुमचे मागील QR आणि लिंक स्कॅन येथे दिसतील.",
            hi: "आपके पिछले QR और लिंक स्कैन यहाँ दिखाई देंगे।"
        },

        "Start Scanning →": {
            en: "Start Scanning →",
            mr: "स्कॅनिंग सुरू करा →",
            hi: "स्कैनिंग शुरू करें →"
        },


        /* =========================
           ALERTS
        ========================= */

        "Security Alerts & Notifications": {
            en: "Security Alerts & Notifications",
            mr: "सुरक्षा अलर्ट आणि सूचना",
            hi: "सुरक्षा अलर्ट और सूचनाएँ"
        },

        "Unread Security Alerts": {
            en: "Unread Security Alerts",
            mr: "न वाचलेले सुरक्षा अलर्ट",
            hi: "अपठित सुरक्षा अलर्ट"
        },

        "Risk Score:": {
            en: "Risk Score:",
            mr: "जोखीम स्कोअर:",
            hi: "जोखिम स्कोर:"
        },

        "No Security Alerts": {
            en: "No Security Alerts",
            mr: "कोणतेही सुरक्षा अलर्ट नाहीत",
            hi: "कोई सुरक्षा अलर्ट नहीं हैं"
        },

        "Your account currently has no security alerts.": {
            en: "Your account currently has no security alerts.",
            mr: "तुमच्या खात्यावर सध्या कोणतेही सुरक्षा अलर्ट नाहीत.",
            hi: "आपके खाते पर वर्तमान में कोई सुरक्षा अलर्ट नहीं हैं।"
        },


        /* =========================
           PROFILE
        ========================= */

        "My Profile": {
            en: "My Profile",
            mr: "माझे प्रोफाइल",
            hi: "मेरी प्रोफ़ाइल"
        },

        "Manage your TRUESCAN account": {
            en: "Manage your TRUESCAN account",
            mr: "तुमचे TRUESCAN खाते व्यवस्थापित करा",
            hi: "अपना TRUESCAN खाता प्रबंधित करें"
        },

        "Change Photo": {
            en: "Change Photo",
            mr: "फोटो बदला",
            hi: "फोटो बदलें"
        },

        "Account Security": {
            en: "Account Security",
            mr: "खाते सुरक्षा",
            hi: "खाता सुरक्षा"
        },

        "Your account is protected by TRUESCAN. Never share your password with anyone.": {
            en: "Your account is protected by TRUESCAN. Never share your password with anyone.",
            mr: "तुमचे खाते TRUESCAN द्वारे सुरक्षित आहे. तुमचा पासवर्ड कोणासोबतही शेअर करू नका.",
            hi: "आपका खाता TRUESCAN द्वारा सुरक्षित है। अपना पासवर्ड किसी के साथ साझा न करें।"
        },

        "Your account has active security protection.": {
            en: "Your account has active security protection.",
            mr: "तुमच्या खात्यावर सक्रिय सुरक्षा संरक्षण आहे.",
            hi: "आपके खाते पर सक्रिय सुरक्षा सुरक्षा मौजूद है।"
        },

        "Security Settings": {
            en: "Security Settings",
            mr: "सुरक्षा सेटिंग्ज",
            hi: "सुरक्षा सेटिंग्स"
        },

        "Scan History": {
            en: "Scan History",
            mr: "स्कॅन इतिहास",
            hi: "स्कैन इतिहास"
        },


        /* =========================
           LOGIN / REGISTER
        ========================= */

        "Welcome Back": {
            en: "Welcome Back",
            mr: "पुन्हा स्वागत आहे",
            hi: "वापस स्वागत है"
        },

        "Login to your TRUESCAN account": {
            en: "Login to your TRUESCAN account",
            mr: "तुमच्या TRUESCAN खात्यात लॉगिन करा",
            hi: "अपने TRUESCAN खाते में लॉगिन करें"
        },

        "Email Address": {
            en: "Email Address",
            mr: "ईमेल पत्ता",
            hi: "ईमेल पता"
        },

        "Password": {
            en: "Password",
            mr: "पासवर्ड",
            hi: "पासवर्ड"
        },

        "Forgot Password?": {
            en: "Forgot Password?",
            mr: "पासवर्ड विसरलात?",
            hi: "पासवर्ड भूल गए?"
        },

        "LOGIN": {
            en: "LOGIN",
            mr: "लॉगिन",
            hi: "लॉगिन"
        },

        "Don't have an account? Create Account": {
            en: "Don't have an account? Create Account",
            mr: "खाते नाही? खाते तयार करा",
            hi: "खाता नहीं है? खाता बनाएँ"
        },

        "Admin Login": {
            en: "Admin Login",
            mr: "अॅडमिन लॉगिन",
            hi: "एडमिन लॉगिन"
        },

        "Your security is our priority": {
            en: "Your security is our priority",
            mr: "तुमची सुरक्षा आमची प्राथमिकता आहे",
            hi: "आपकी सुरक्षा हमारी प्राथमिकता है"
        },

        "Create Account": {
            en: "Create Account",
            mr: "खाते तयार करा",
            hi: "खाता बनाएँ"
        },

        "Create your TRUESCAN account": {
            en: "Create your TRUESCAN account",
            mr: "तुमचे TRUESCAN खाते तयार करा",
            hi: "अपना TRUESCAN खाता बनाएँ"
        },

        "Full Name": {
            en: "Full Name",
            mr: "पूर्ण नाव",
            hi: "पूरा नाम"
        },

        "Mobile Number": {
            en: "Mobile Number",
            mr: "मोबाईल नंबर",
            hi: "मोबाइल नंबर"
        },

        "Confirm Password": {
            en: "Confirm Password",
            mr: "पासवर्ड पुन्हा टाका",
            hi: "पासवर्ड की पुष्टि करें"
        },

        "CREATE ACCOUNT": {
            en: "CREATE ACCOUNT",
            mr: "खाते तयार करा",
            hi: "खाता बनाएँ"
        },


        /* =========================
           SECURITY SETTINGS
        ========================= */

        "Manage your TRUESCAN protection and security preferences.": {
            en: "Manage your TRUESCAN protection and security preferences.",
            mr: "तुमचे TRUESCAN संरक्षण आणि सुरक्षा preferences व्यवस्थापित करा.",
            hi: "अपनी TRUESCAN सुरक्षा और सुरक्षा प्राथमिकताएँ प्रबंधित करें।"
        },

        "Scan Protection": {
            en: "Scan Protection",
            mr: "स्कॅन संरक्षण",
            hi: "स्कैन सुरक्षा"
        },

        "Configure how TRUESCAN checks suspicious content.": {
            en: "Configure how TRUESCAN checks suspicious content.",
            mr: "TRUESCAN संशयास्पद content कसे तपासते ते सेट करा.",
            hi: "TRUESCAN संदिग्ध सामग्री की जाँच कैसे करता है, इसे सेट करें।"
        },

        "Block Dangerous Links": {
            en: "Block Dangerous Links",
            mr: "धोकादायक लिंक ब्लॉक करा",
            hi: "खतरनाक लिंक ब्लॉक करें"
        },

        "Prevent access to links identified as dangerous.": {
            en: "Prevent access to links identified as dangerous.",
            mr: "धोकादायक म्हणून ओळखल्या गेलेल्या लिंकचा access रोखा.",
            hi: "खतरनाक पहचानी गई लिंक तक पहुँच रोकें।"
        },

        "Warn Before Opening": {
            en: "Warn Before Opening",
            mr: "उघडण्यापूर्वी चेतावणी",
            hi: "खोलने से पहले चेतावनी"
        },

        "Show a warning before opening suspicious links.": {
            en: "Show a warning before opening suspicious links.",
            mr: "संशयास्पद लिंक उघडण्यापूर्वी चेतावणी दाखवा.",
            hi: "संदिग्ध लिंक खोलने से पहले चेतावनी दिखाएँ।"
        },

        "HTTPS Verification": {
            en: "HTTPS Verification",
            mr: "HTTPS पडताळणी",
            hi: "HTTPS सत्यापन"
        },

        "Check whether websites use a secure HTTPS connection.": {
            en: "Check whether websites use a secure HTTPS connection.",
            mr: "वेबसाइट सुरक्षित HTTPS connection वापरते का ते तपासा.",
            hi: "जाँचें कि वेबसाइट सुरक्षित HTTPS कनेक्शन का उपयोग करती है या नहीं।"
        },

        "Suspicious Domain Check": {
            en: "Suspicious Domain Check",
            mr: "संशयास्पद डोमेन तपासणी",
            hi: "संदिग्ध डोमेन जाँच"
        },

        "SECURITY STATUS": {
            en: "SECURITY STATUS",
            mr: "सुरक्षा स्थिती",
            hi: "सुरक्षा स्थिति"
        },

        "Strong": {
            en: "Strong",
            mr: "मजबूत",
            hi: "मजबूत"
        },

        "Trusted Devices": {
            en: "Trusted Devices",
            mr: "विश्वसनीय devices",
            hi: "विश्वसनीय डिवाइस"
        },

        "Current Device": {
            en: "Current Device",
            mr: "सध्याचे device",
            hi: "वर्तमान डिवाइस"
        },

        "This device": {
            en: "This device",
            mr: "हे device",
            hi: "यह डिवाइस"
        },

        "Current": {
            en: "Current",
            mr: "सध्याचे",
            hi: "वर्तमान"
        },

        "Logout All Devices": {
            en: "Logout All Devices",
            mr: "सर्व devices मधून लॉगआउट",
            hi: "सभी डिवाइस से लॉगआउट"
        },

        "Emergency Security": {
            en: "Emergency Security",
            mr: "आपत्कालीन सुरक्षा",
            hi: "आपातकालीन सुरक्षा"
        },

        "Clear All Scan Data": {
            en: "Clear All Scan Data",
            mr: "सर्व स्कॅन डेटा साफ करा",
            hi: "सारा स्कैन डेटा साफ करें"
        },

        "Reset Security Settings": {
            en: "Reset Security Settings",
            mr: "सुरक्षा सेटिंग्ज रीसेट करा",
            hi: "सुरक्षा सेटिंग्स रीसेट करें"
        },


        /* =========================
           RESULT
        ========================= */

        "Security Scan Result": {
            en: "Security Scan Result",
            mr: "सुरक्षा स्कॅन परिणाम",
            hi: "सुरक्षा स्कैन परिणाम"
        },

        "TRUESCAN security analysis": {
            en: "TRUESCAN security analysis",
            mr: "TRUESCAN सुरक्षा विश्लेषण",
            hi: "TRUESCAN सुरक्षा विश्लेषण"
        },

        "SECURITY STATUS": {
            en: "SECURITY STATUS",
            mr: "सुरक्षा स्थिती",
            hi: "सुरक्षा स्थिति"
        },

        "Risk Score": {
            en: "Risk Score",
            mr: "जोखीम स्कोअर",
            hi: "जोखिम स्कोर"
        },

        "Scan Information": {
            en: "Scan Information",
            mr: "स्कॅन माहिती",
            hi: "स्कैन जानकारी"
        },

        "Details detected by TRUESCAN": {
            en: "Details detected by TRUESCAN",
            mr: "TRUESCAN ने शोधलेली माहिती",
            hi: "TRUESCAN द्वारा पहचानी गई जानकारी"
        },

        "CONTENT TYPE": {
            en: "CONTENT TYPE",
            mr: "कंटेंट प्रकार",
            hi: "कंटेंट प्रकार"
        },

        "SCANNED CONTENT": {
            en: "SCANNED CONTENT",
            mr: "स्कॅन केलेला कंटेंट",
            hi: "स्कैन की गई सामग्री"
        },

        "Copy": {
            en: "Copy",
            mr: "कॉपी",
            hi: "कॉपी"
        },

        "Smart Security Analysis": {
            en: "Smart Security Analysis",
            mr: "स्मार्ट सुरक्षा विश्लेषण",
            hi: "स्मार्ट सुरक्षा विश्लेषण"
        },

        "Intelligent security insights from TRUESCAN": {
            en: "Intelligent security insights from TRUESCAN",
            mr: "TRUESCAN कडून स्मार्ट सुरक्षा माहिती",
            hi: "TRUESCAN से स्मार्ट सुरक्षा जानकारी"
        },

        "AI Security Explanation": {
            en: "AI Security Explanation",
            mr: "AI सुरक्षा स्पष्टीकरण",
            hi: "AI सुरक्षा स्पष्टीकरण"
        },

        "Why is this risky?": {
            en: "Why is this risky?",
            mr: "हे धोकादायक का आहे?",
            hi: "यह जोखिमपूर्ण क्यों है?"
        },

        "Threat Patterns Detected": {
            en: "Threat Patterns Detected",
            mr: "धोक्याचे patterns सापडले",
            hi: "खतरे के पैटर्न मिले"
        },

        "Recommended Action": {
            en: "Recommended Action",
            mr: "शिफारस केलेली कृती",
            hi: "अनुशंसित कार्रवाई"
        },

        "Check Another Link": {
            en: "Check Another Link",
            mr: "दुसरी लिंक तपासा",
            hi: "दूसरी लिंक जाँचें"
        },

        "Scan QR Image": {
            en: "Scan QR Image",
            mr: "QR प्रतिमा स्कॅन करा",
            hi: "QR इमेज स्कैन करें"
        },

        "View Scan History": {
            en: "View Scan History",
            mr: "स्कॅन इतिहास पहा",
            hi: "स्कैन इतिहास देखें"
        }
    };


    /* =====================================
       GET CURRENT LANGUAGE
    ===================================== */

    function getLanguage() {
        const saved = localStorage.getItem(STORAGE_KEY);

        if (SUPPORTED.includes(saved)) {
            return saved;
        }

        return "en";
    }


    /* =====================================
       TRANSLATE TEXT
    ===================================== */

    function translateText(text, language) {

        if (!text) {
            return text;
        }

        const clean = text.trim();

        if (!translations[clean]) {
            return text;
        }

        return translations[clean][language] || text;
    }


    /* =====================================
       TRANSLATE TEXT NODES
    ===================================== */

    function translateTextNodes(language) {

        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            {
                acceptNode: function (node) {

                    if (!node.nodeValue.trim()) {
                        return NodeFilter.FILTER_REJECT;
                    }

                    const parent = node.parentElement;

                    if (!parent) {
                        return NodeFilter.FILTER_REJECT;
                    }

                    const tag = parent.tagName.toLowerCase();

                    if (
                        tag === "script" ||
                        tag === "style" ||
                        tag === "noscript"
                    ) {
                        return NodeFilter.FILTER_REJECT;
                    }

                    if (
                        parent.closest(
                            "input, textarea, select, option"
                        )
                    ) {
                        return NodeFilter.FILTER_REJECT;
                    }

                    return NodeFilter.FILTER_ACCEPT;
                }
            }
        );

        const nodes = [];

        let node;

        while ((node = walker.nextNode())) {
            nodes.push(node);
        }

        nodes.forEach(function (textNode) {

            const original =
                textNode.textContent.trim();

            if (!original) {
                return;
            }

            const translated =
                translateText(original, language);

            if (translated !== original) {

                const leading =
                    textNode.textContent.match(/^\s*/)?.[0] || "";

                const trailing =
                    textNode.textContent.match(/\s*$/)?.[0] || "";

                textNode.textContent =
                    leading +
                    translated +
                    trailing;
            }
        });
    }


    /* =====================================
       TRANSLATE PLACEHOLDERS
    ===================================== */

    function translateInputs(language) {

        document
            .querySelectorAll(
                "input[placeholder], textarea[placeholder]"
            )
            .forEach(function (element) {

                const original =
                    element.getAttribute("data-original-placeholder") ||
                    element.getAttribute("placeholder");

                if (!original) {
                    return;
                }

                if (
                    !element.hasAttribute(
                        "data-original-placeholder"
                    )
                ) {
                    element.setAttribute(
                        "data-original-placeholder",
                        original
                    );
                }

                element.placeholder =
                    translateText(
                        original,
                        language
                    );
            });
    }


    /* =====================================
       TRANSLATE TITLE
    ===================================== */

    function translateTitles(language) {

        document
            .querySelectorAll("[title]")
            .forEach(function (element) {

                const original =
                    element.getAttribute(
                        "data-original-title"
                    ) ||
                    element.getAttribute("title");

                if (!original) {
                    return;
                }

                if (
                    !element.hasAttribute(
                        "data-original-title"
                    )
                ) {
                    element.setAttribute(
                        "data-original-title",
                        original
                    );
                }

                element.title =
                    translateText(
                        original,
                        language
                    );
            });
    }


    /* =====================================
       TRANSLATE SELECT OPTIONS
    ===================================== */

    function translateOptions(language) {

        document
            .querySelectorAll("option")
            .forEach(function (option) {

                const original =
                    option.getAttribute(
                        "data-original-text"
                    ) ||
                    option.textContent.trim();

                if (!original) {
                    return;
                }

                if (
                    !option.hasAttribute(
                        "data-original-text"
                    )
                ) {
                    option.setAttribute(
                        "data-original-text",
                        original
                    );
                }

                option.textContent =
                    translateText(
                        original,
                        language
                    );
            });
    }


    /* =====================================
       DATA-I18N SUPPORT
    ===================================== */

    function translateDataKeys(language) {

        document
            .querySelectorAll("[data-i18n]")
            .forEach(function (element) {

                const key =
                    element.getAttribute("data-i18n");

                if (
                    translations[key] &&
                    translations[key][language]
                ) {
                    element.textContent =
                        translations[key][language];
                }
            });


        document
            .querySelectorAll("[data-i18n-placeholder]")
            .forEach(function (element) {

                const key =
                    element.getAttribute(
                        "data-i18n-placeholder"
                    );

                if (
                    translations[key] &&
                    translations[key][language]
                ) {
                    element.placeholder =
                        translations[key][language];
                }
            });
    }


    /* =====================================
       LANGUAGE DROPDOWN
    ===================================== */

    function createLanguageSelector() {

        let selector =
            document.getElementById(
                "languageSelect"
            );

        if (selector) {
            return selector;
        }

        const wrapper =
            document.createElement("div");

        wrapper.className =
            "truescan-global-language";

        wrapper.innerHTML = `
            <span class="truescan-language-icon">🌐</span>

            <select id="languageSelect"
                    aria-label="Language">

                <option value="en">
                    English
                </option>

                <option value="mr">
                    मराठी
                </option>

                <option value="hi">
                    हिन्दी
                </option>

            </select>
        `;

        document.body.appendChild(wrapper);

        selector =
            wrapper.querySelector(
                "#languageSelect"
            );

        return selector;
    }


    /* =====================================
       LANGUAGE CSS
    ===================================== */

    function addLanguageStyles() {

        if (
            document.getElementById(
                "truescan-language-style"
            )
        ) {
            return;
        }

        const style =
            document.createElement("style");

        style.id =
            "truescan-language-style";

        style.textContent = `
            .truescan-global-language {
                position: fixed;
                top: 18px;
                right: 20px;
                z-index: 99999;

                display: flex;
                align-items: center;
                gap: 7px;

                padding: 6px 10px;

                border-radius: 12px;

                background: rgba(10, 31, 58, 0.96);

                border: 1px solid
                    rgba(255,255,255,0.14);

                box-shadow:
                    0 8px 25px
                    rgba(0,0,0,0.25);
            }

            .truescan-language-icon {
                font-size: 15px;
            }

            .truescan-global-language select {
                border: 0;
                outline: 0;

                background: transparent;

                color: #ffffff;

                font-size: 13px;
                font-weight: 700;

                cursor: pointer;
            }

            .truescan-global-language option {
                background: #0d2340;
                color: #ffffff;
            }

            @media (max-width: 600px) {

                .truescan-global-language {
                    top: 10px;
                    right: 10px;
                }
            }
        `;

        document.head.appendChild(style);
    }


    /* =====================================
       APPLY LANGUAGE
    ===================================== */

    function applyLanguage(language) {

        if (!SUPPORTED.includes(language)) {
            language = "en";
        }

        localStorage.setItem(
            STORAGE_KEY,
            language
        );

        document.documentElement
            .setAttribute(
                "lang",
                language
            );

        translateTextNodes(language);
        translateInputs(language);
        translateTitles(language);
        translateOptions(language);
        translateDataKeys(language);

        const selector =
            document.getElementById(
                "languageSelect"
            );

        if (selector) {
            selector.value = language;
        }
    }


    /* =====================================
       SAVE LANGUAGE TO FLASK SESSION
    ===================================== */

    async function saveLanguage(language) {

        if (!SUPPORTED.includes(language)) {
            return;
        }

        localStorage.setItem(
            STORAGE_KEY,
            language
        );

        applyLanguage(language);

        try {

            const response =
                await fetch(
                    "/set-language",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/x-www-form-urlencoded;charset=UTF-8"
                        },

                        body:
                            new URLSearchParams({
                                language: language
                            })
                    }
                );

            if (!response.ok) {
                throw new Error(
                    "Language request failed"
                );
            }

        } catch (error) {

            console.warn(
                "TRUESCAN language sync:",
                error
            );
        }
    }


    /* =====================================
       INITIALIZE
    ===================================== */

    function initializeLanguage() {

        addLanguageStyles();

        const selector =
            createLanguageSelector();

        const language =
            getLanguage();

        selector.value =
            language;

        applyLanguage(language);

        if (
            !selector.dataset
                .truescanBound
        ) {

            selector.addEventListener(
                "change",
                function () {

                    saveLanguage(
                        this.value
                    );
                }
            );

            selector.dataset
                .truescanBound = "true";
        }
    }


    /* =====================================
       PAGE LOAD
    ===================================== */

    document.addEventListener(
        "DOMContentLoaded",
        function () {

            initializeLanguage();

            /*
             * Some pages load dynamic
             * content after page load.
             */

            setTimeout(
                function () {
                    applyLanguage(
                        getLanguage()
                    );
                },
                300
            );

            setTimeout(
                function () {
                    applyLanguage(
                        getLanguage()
                    );
                },
                1000
            );
        }
    );


    /* =====================================
       GLOBAL API
    ===================================== */

    window.TRUESCAN_LANGUAGE = {

        getLanguage:
            getLanguage,

        applyLanguage:
            applyLanguage,

        saveLanguage:
            saveLanguage

    };

})();
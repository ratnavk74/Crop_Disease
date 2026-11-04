"""
Simple rule-based voice assistant for CropShield AI.

The browser performs speech-to-text (Web Speech API). The recognised sentence
is sent here, matched against farmer-friendly intents in English, Hindi and
Kannada, and answered with a localised reply plus an optional UI action.
"""

from utils.i18n import LANGUAGES, localize_recommendation, translate
from utils.recommendation import get_recommendation

LANGUAGE_WORDS = {
    "hi": ["hindi", "हिंदी", "हिन्दी", "हिंदी में", "ಹಿಂದಿ"],
    "kn": ["kannada", "ಕನ್ನಡ", "कन्नड़", "ಕನ್ನಡದಲ್ಲಿ"],
    "en": ["english", "अंग्रेजी", "अंग्रेज़ी", "ಇಂಗ್ಲಿಷ್", "ಆಂಗ್ಲ"],
}

SWITCH_WORDS = [
    "switch", "change", "language", "speak in", "talk in",
    "बदल", "भाषा", "में बोल", "में कर",
    "ಬದಲಿಸ", "ಭಾಷೆ", "ಭಾಷೆಗೆ", "ಮಾತನಾಡು",
]

DISEASE_KEYWORDS = {
    "Maize_Blight": [
        "blight", "leaf blight", "northern leaf", "nclb", "turcicum",
        "झुलसा", "ब्लाइट", "पत्ती झुलसा",
        "ಬ್ಲೈಟ್", "ಎಲೆ ಬ್ಲೈಟ್", "ಜುಲಸು",
    ],
    "Maize_Common_Rust": [
        "maize rust", "corn rust", "common rust", "sorghi",
        "मक्का रतुआ", "मक्के में रतुआ", "मक्का रस्ट",
        "ಮೆಕ್ಕೆಜೋಳ ತುಕ್ಕು", "ಮೆಕ್ಕೆಜೋಳ ರಸ್ಟ್",
    ],
    "Wheat_YellowRust": [
        "yellow rust", "stripe rust", "yellow stripe", "striiformis",
        "पीला रतुआ", "पीली पट्टी", "पीला रस्ट",
        "ಹಳದಿ ತುಕ್ಕು", "ಹಳದಿ ಪಟ್ಟಿ",
    ],
    "Wheat_BlackRust": [
        "black rust", "stem rust", "black stem", "graminis",
        "काला रतुआ", "काला तना", "ब्लैक रस्ट",
        "ಕಪ್ಪು ತುಕ್ಕು", "ಕಪ್ಪು ಕಾಂಡ",
    ],
    "Wheat_BrownRust": [
        "brown rust", "leaf rust", "brown leaf", "triticina",
        "भूरा रतुआ", "भूरी पत्ती", "ब्राउन रस्ट",
        "ಕಂದು ತುಕ್ಕು", "ಕಂದು ಎಲೆ",
    ],
}

UPLOAD_WORDS = [
    "upload", "photo", "picture", "camera", "image", "scan",
    "अपलोड", "फोटो", "तस्वीर", "कैमरा", "जाँच", "जांच",
    "ಅಪ್‌ಲೋಡ್", "ಫೋಟೋ", "ಚಿತ್ರ", "ಕ್ಯಾಮೆರಾ", "ಪರೀಕ್ಷೆ",
]

READ_WORDS = [
    "read", "speak", "listen", "say it", "advisory", "tell me",
    "सुनाओ", "पढ़ो", "बोलो", "सलाह", "बताओ",
    "ಓದು", "ಹೇಳು", "ಕೇಳಿಸು", "ಸಲಹೆ", "ಮಾತನಾಡು",
]

HOME_WORDS = ["home", "go back", "main page", "होम", "वापस", "मुख्य", "ಮುಖಪುಟ", "ಹಿಂದೆ", "ಮುಖ್ಯ"]
LOGOUT_WORDS = ["logout", "log out", "sign out", "लॉग आउट", "लॉगआउट", "ಲಾಗ್ ಔಟ್"]
TREATMENT_WORDS = [
    "treatment", "medicine", "spray", "fungicide", "dose", "dosage", "cure",
    "इलाज", "दवा", "छिड़काव", "कवकनाशी", "मात्रा", "उपाय",
    "ಚಿಕಿತ್ಸೆ", "ಔಷಧ", "ಸಿಂಪಡಣೆ", "ಶಿಲೀಂಧ್ರನಾಶಕ", "ಪ್ರಮಾಣ", "ಪರಿಹಾರ",
    "ಇಲಾಜ್", "ಮದ್ದು", "ಸಿಂಪರಣೆ", "ಶಿಲೀಂಧ್ರ",
]
SYMPTOM_WORDS = ["symptom", "sign", "identify", "लक्षण", "पहचान", "ಲಕ್ಷಣ", "ಗುರುತು"]
PREVENTION_WORDS = [
    "prevent", "prevention", "avoid", "stop", "बचाव", "रोकथाम", "बचाने",
    "ತಡೆ", "ತಡೆಗಟ್ಟ", "ಮುನ್ನೆಚ್ಚರಿಕೆ",
]
STEP_WORDS = [
    "step by step", "steps", "step", "how to prevent", "how can i prevent",
    "कदम", "चरण", "कैसे रोकें", "रोकथाम के कदम",
    "ಹಂತ", "ಹಂತಗಳು", "ಹೇಗೆ ತಡೆ", "ತಡೆಗಟ್ಟುವ ಹಂತ",
]
CAUSE_WORDS = ["why", "cause", "reason", "कारण", "क्यों", "ಏಕೆ", "ಕಾರಣ"]
SEVERITY_WORDS = ["severity", "serious", "confidence", "how bad", "गंभीर", "कितना", "विश्वास", "ತೀವ್ರ", "ಎಷ್ಟು", "ವಿಶ್ವಾಸ"]
GREETING_WORDS = ["hello", "hi", "namaste", "नमस्ते", "नमस्कार", "ನಮಸ್ಕಾರ", "ಹಲೋ"]
HELP_WORDS = ["help", "what can you do", "commands", "मदद", "सहायता", "क्या कर", "ಸಹಾಯ", "ಏನು ಮಾಡ"]


def _contains(text, words):
    return any(word in text for word in words)


def _detect_language_request(text):
    for code, words in LANGUAGE_WORDS.items():
        if _contains(text, words):
            if _contains(text, SWITCH_WORDS) or text.strip() in [w.lower() for w in words]:
                return code
    return None


def _detect_disease(text):
    for disease_key, words in DISEASE_KEYWORDS.items():
        if _contains(text, words):
            return disease_key
    return None


def _localized_info(disease_key, lang):
    if not disease_key:
        return None
    info = dict(get_recommendation(disease_key))
    info["key"] = disease_key
    return localize_recommendation(info, lang)


def _response(reply, lang, action=None, target=None, speak=True):
    return {
        "reply": reply,
        "action": action,
        "target": target,
        "speak": speak,
        "language": lang,
    }


def build_reply(text, lang="en", page="home", disease_key=None, confidence=None, is_authenticated=True):
    """
    Interpret a recognised sentence and return a localised assistant response.

    Response keys:
        reply   : text to show and (usually) speak
        action  : optional UI action (open_upload, speak_advisory, navigate, ...)
        target  : optional action target
        speak   : whether the browser should read the reply aloud
        language: language used for the reply
    """
    raw = (text or "").strip()
    low = raw.lower()
    help_text = translate("assistant_help", lang)

    if not raw:
        return _response(translate("assistant_unknown", lang, help=help_text), lang)

    # 1. Switch language
    requested_lang = _detect_language_request(low)
    if requested_lang:
        language_name = LANGUAGES[requested_lang]["native"]
        return _response(
            translate("assistant_language", lang, language=language_name),
            lang,
            action="set_language",
            target=requested_lang,
            speak=False,
        )

    # 2. Logout / home / upload / read
    if _contains(low, LOGOUT_WORDS):
        return _response(
            translate("assistant_logout", lang),
            lang,
            action="logout",
            speak=False,
        )

    if _contains(low, HOME_WORDS):
        return _response(
            translate("assistant_home", lang),
            lang,
            action="navigate",
            target="home",
        )

    if _contains(low, UPLOAD_WORDS):
        if not is_authenticated:
            return _response(translate("assistant_login_needed", lang), lang, action="navigate", target="login")
        return _response(
            translate("assistant_upload", lang),
            lang,
            action="open_upload",
        )

    # Questions about the currently open diagnosis, or a named disease.
    info = _localized_info(disease_key, lang) if disease_key else None
    detected_disease = _detect_disease(low)
    if info is None and detected_disease:
        info = _localized_info(detected_disease, lang)

    # Step-by-step prevention must be checked before the broad "read" and
    # "prevention" words, because Hindi/Kannada sentences often contain
    # "बताओ" / "ಹೇಳು" (tell/read) and "रोकथाम" / "ತಡೆ" together.
    if _contains(low, STEP_WORDS):
        if info:
            steps = info.get("prevention_steps") or []
            if steps:
                numbered = " ".join(
                    f"{index}. {step}" for index, step in enumerate(steps, start=1)
                )
                return _response(
                    translate("assistant_prevention_steps", lang, text=numbered), lang
                )
            return _response(
                translate("assistant_prevention", lang, text=info.get("prevention", "")),
                lang,
            )
        return _response(translate("assistant_no_disease", lang), lang)

    if _contains(low, HELP_WORDS):
        return _response(help_text, lang)

    if _contains(low, TREATMENT_WORDS):
        if info:
            return _response(
                translate("assistant_treatment", lang, text=info.get("treatment", "")), lang
            )
        return _response(translate("assistant_no_disease", lang), lang)

    if _contains(low, SYMPTOM_WORDS):
        if info:
            return _response(
                translate("assistant_symptoms", lang, text=info.get("symptoms", "")), lang
            )
        return _response(translate("assistant_no_disease", lang), lang)

    if _contains(low, PREVENTION_WORDS):
        if info:
            return _response(
                translate("assistant_prevention", lang, text=info.get("prevention", "")), lang
            )
        return _response(translate("assistant_no_disease", lang), lang)

    if _contains(low, CAUSE_WORDS):
        if info:
            return _response(
                translate(
                    "assistant_cause",
                    lang,
                    text=info.get("farmer_reason") or info.get("why_it_happened", ""),
                ),
                lang,
            )
        return _response(translate("assistant_no_disease", lang), lang)

    if _contains(low, SEVERITY_WORDS):
        if info:
            severity = info.get("severity", "")
            if confidence is None:
                reply = f"{info.get('display_name', '')} — {severity}"
            else:
                reply = translate(
                    "assistant_severity", lang, severity=severity, confidence=confidence
                )
            return _response(reply, lang)
        return _response(translate("assistant_no_disease", lang), lang)

    if _contains(low, READ_WORDS):
        if page == "result" and disease_key:
            return _response(
                translate("assistant_read", lang),
                lang,
                action="speak_advisory",
                speak=False,
            )
        return _response(translate("assistant_read_unavailable", lang), lang)

    # 4. A named disease without a specific question: give a useful summary
    if detected_disease:
        summary = info.get("treatment", "") if info else ""
        if len(summary) > 280:
            summary = summary[:277].rsplit(" ", 1)[0] + "…"
        return _response(
            translate(
                "assistant_disease",
                lang,
                disease=info.get("display_name", detected_disease.replace("_", " ")),
                summary=summary,
            ),
            lang,
        )

    if _contains(low, GREETING_WORDS):
        return _response(translate("assistant_greeting", lang), lang)

    if page == "result" and disease_key:
        # On a report page an unrecognised question is best answered with the
        # available command list rather than a dead end.
        return _response(translate("assistant_unknown", lang, help=help_text), lang)

    if _contains(low, ["disease", "diseases", "रोग", "बीमारी", "ರೋಗ"]):
        return _response(translate("assistant_disease_list", lang), lang)

    return _response(translate("assistant_unknown", lang, help=help_text), lang)

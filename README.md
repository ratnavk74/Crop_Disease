# 🌱 CropShield AI - Crop Disease Detection & Agronomic Advisory System

An end-to-end Deep Learning and Precision Agronomy web platform built with Flask, TensorFlow/Keras, and OpenCV. Farmers upload a leaf photo of **Wheat** or **Maize (Corn)**, the model identifies the disease, and the app explains the result in simple language with a spoken advisory in **English, Hindi, or Kannada**.

Repository: <https://github.com/ratnavk74/Crop_Disease.git>

---

## ✨ Key Features

| Feature | What it does |
| :--- | :--- |
| **Deep learning diagnosis** | MobileNetV2 transfer-learning model with confidence score for 7 maize/wheat classes. |
| **Explainable AI** | Grad-CAM heatmap highlights the lesion areas that influenced the prediction. |
| **Automatic language recognition** | Detects the browser/phone language (`Accept-Language`) on the first visit and remembers the choice in the session and user profile. |
| **Manual language switcher** | English / हिन्दी / ಕನ್ನಡ selector in the navigation bar, available on every page. |
| **Voice input** | Farmers tap the microphone and speak a question in their own language using the browser Web Speech API. |
| **Spoken replies** | The assistant answers aloud with SpeechSynthesis and also shows the reply as text. |
| **Simple reason for the disease** | A plain-language "Why did this happen?" explanation written for farmers, not agronomists. |
| **Step-by-step prevention** | A numbered checklist from pre-sowing to harvest, with a "Listen to steps" button. |
| **Farmer login** | Local SQLite accounts with hashed passwords, registration, remember-me, and a demo account. |
| **Full advisory report** | Symptoms, causes, chemical + organic treatment, resistant varieties, cultural practices, soil nutrition, and printable report. |
| **1-click test samples** | Seven preloaded leaf images for instant testing without uploading a file. |
| **REST API** | JSON endpoints for prediction, disease list, and the multilingual voice assistant. |

---

## 🗂️ Project Directory Structure

```
Crop_Disease_Enhanced/
│
├── app.py                       # Flask routes, authentication, locale context, APIs
├── requirements.txt             # Python dependencies
├── README.md                    # Setup and usage guide
├── .gitignore                   # Files that should not be committed
│
├── model/
│   └── crop_disease_model.h5   # Trained MobileNetV2 weights
│
├── utils/
│   ├── __init__.py
│   ├── auth.py                  # SQLite users, password hashing, demo seeding
│   ├── assistant.py             # Rule-based multilingual voice intents
│   ├── farmer_guides.py         # Simple reason + step-by-step prevention (EN/HI/KN)
│   ├── i18n.py                  # Language detection, UI and advisory translations
│   ├── prediction.py            # Preprocessing, CNN inference and Grad-CAM
│   └── recommendation.py        # Agronomic knowledge base
│
├── static/
│   ├── css/style.css            # Responsive UI, auth pages, voice widget, print layout
│   ├── js/main.js               # Upload preview, language switch, TTS helpers
│   ├── js/voice.js              # Speech recognition, assistant calls and actions
│   ├── samples/                 # 7 benchmark leaves
│   └── uploads/                 # Uploaded images and Grad-CAM outputs
│
└── templates/
    ├── base.html                # Navigation, language switcher, flash messages, voice panel
    ├── index.html               # Upload portal, voice-first access, sample gallery
    ├── login.html               # Farmer login + demo account fill
    ├── register.html            # Farmer registration with language preference
    └── result.html              # Diagnosis report plus step-by-step prevention
```

---

## 🌾 Supported Diseases & Classes

| Crop | Disease Key | Common Name | Pathogen | Severity |
| :--- | :--- | :--- | :--- | :--- |
| **Maize** | `Maize_Blight` | Northern Corn Leaf Blight | *Exserohilum turcicum* | Critical / High |
| **Maize** | `Maize_Common_Rust` | Common Rust of Maize | *Puccinia sorghi* | Moderate |
| **Maize** | `Maize_Healthy` | Healthy Maize Foliage | None (Optimal Health) | None / Healthy |
| **Wheat** | `Wheat_BlackRust` | Black (Stem) Rust of Wheat | *Puccinia graminis f. sp. tritici* | Critical / High |
| **Wheat** | `Wheat_BrownRust` | Brown (Leaf) Rust of Wheat | *Puccinia triticina* | Moderate |
| **Wheat** | `Wheat_YellowRust` | Yellow (Stripe) Rust of Wheat | *Puccinia striiformis* | Critical / High |
| **Wheat** | `Wheat_Healthy` | Healthy Wheat Foliage | None (Optimal Health) | None / Healthy |

---

## 🚀 How to Run

### 1. Create a virtual environment (recommended)

```powershell
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the app

```bash
python app.py
```

### 4. Open the browser

```
http://127.0.0.1:5000
```

The first visit opens the **login page**. Use the demo account shown on the page:

```
Email / phone : demo@cropshield.ai  (or 9999999999)
Password      : demo1234
```

You can also tap **Fill demo account** and then **Login**, or create your own account from the **Register** page.

> **First prediction may take a little longer** because TensorFlow loads the model and builds the Grad-CAM graph.

---

## 🌐 Language Recognition

* On the first visit the server reads the browser's `Accept-Language` header and picks the best match among **English (`en`)**, **Hindi (`hi`)**, and **Kannada (`kn`)**.
* The selected language is stored in the session. For logged-in farmers it is also saved in their profile so it follows them on the next device login.
* The navbar selector changes the language immediately (`/set-language/<code>`).
* All interface text, disease names, advisories, prevention steps, flash messages, and voice replies are localized.
* To add another language, add an entry in `LANGUAGES` and `UI` in `utils/i18n.py`, plus the disease translations, then extend `FARMER_GUIDES`.

---

## 🎤 Voice Assistant

1. Tap the floating **Voice Assistant** button, the hero **Start speaking** button, or any **Ask by voice** button.
2. Allow microphone permission when the browser asks.
3. Speak a question such as:
   * "Read the advisory"
   * "What is the treatment?"
   * "How do I prevent this step by step?"
   * "Why did this happen?"
   * "Switch to Hindi"
   * "Upload a photo"
   * "Go home"
4. The assistant shows what it heard, replies in the current language, and speaks the answer aloud.

The rule-based engine in `utils/assistant.py` understands English, Hindi, and Kannada keywords. The browser does the speech-to-text and text-to-speech, so **no extra Python speech packages are required**.

### Browser requirements

| Requirement | Details |
| :--- | :--- |
| Browser | **Google Chrome** or **Microsoft Edge** (recommended). Firefox/Safari support varies. |
| Microphone | A working microphone and permission for the site. |
| Secure URL | `http://127.0.0.1:5000`, `http://localhost:5000`, or HTTPS. Microphone access is blocked on plain HTTP for other hosts. |
| Internet | Needed for Google Fonts / Font Awesome icons, and for some cloud speech voices. |

If voice input is unavailable, the typed/example-chip questions still work, and the audio advisory buttons on the report page can read the report aloud.

---

## 🧪 Quick Test (1-Click Analysis)

The home page includes a **Quick Test Samples** gallery with seven preloaded benchmark leaves. Click **Test This Sample** on any card to see:

* the diagnosis and confidence,
* the original leaf next to the Grad-CAM heatmap,
* the simple reason for the disease,
* causes, symptoms, and treatment details,
* the numbered prevention checklist,
* the multi-language audio advisory and voice assistant.

---

## 🔐 Authentication & Security Notes

* Users are stored in `users.db` (SQLite) next to `app.py`.
* Passwords are hashed with Werkzeug PBKDF2; plain passwords are never stored.
* Protected routes: `/`, `/predict`, `/api/predict`.
* Public routes: `/login`, `/register`, `/api/assistant`, `/api/diseases`, static files.
* The Flask secret key is read from the `SECRET_KEY` environment variable, or generated once and stored in `.secret_key`.
* `users.db`, `.secret_key`, uploaded images, and Grad-CAM outputs are excluded from Git by `.gitignore`.
* Use a strong password and set `SECRET_KEY` in production. For deployment, serve the app behind HTTPS (for example with gunicorn + nginx) so the microphone works.

---

## 🔌 JSON API

### `POST /api/predict`

Upload a leaf image as multipart form data (field name `image`). Requires login.

```json
{
  "status": "success",
  "language": "hi",
  "disease": "Maize_Blight",
  "display_name": "मक्का - उत्तरी पत्ती झुलसा",
  "confidence": 94.2,
  "severity": "उच्च",
  "farmer_reason": "...",
  "prevention_steps": ["...", "..."],
  "treatment": "...",
  "prevention": "...",
  "voice": "...",
  "image_url": "/static/uploads/...",
  "gradcam_url": "/static/uploads/gradcam_..."
}
```

### `GET /api/diseases`

Returns the localized disease summary list.

### `POST /api/assistant`

```json
{
  "text": "What are the prevention steps?",
  "lang": "en",
  "page": "result",
  "disease": "Maize_Blight",
  "confidence": 94.2
}
```

Response:

```json
{
  "reply": "Prevention steps: 1. ... 2. ...",
  "action": null,
  "target": null,
  "speak": true,
  "language": "en"
}
```

Possible actions: `open_upload`, `speak_advisory`, `read_steps`, `navigate`, `set_language`, `logout`.

---

## 🛠️ Troubleshooting

| Problem | Fix |
| :--- | :--- |
| `ModuleNotFoundError` | Activate the virtual environment and run `pip install -r requirements.txt`. |
| Model file not found | Keep `model/crop_disease_model.h5` in the project. |
| Microphone button does nothing | Use Chrome/Edge, open `localhost`/`127.0.0.1`, and allow microphone permission. |
| No sound in Hindi/Kannada | Install the Hindi/Kannada voice pack in Windows Settings → Time & Language → Speech, or use Chrome which may provide cloud voices. |
| Login fails | Use `demo@cropshield.ai` / `demo1234`, or register a new account. Delete `users.db` only if you want to reset local accounts (the demo account is re-seeded on startup). |
| Port 5000 already in use | Stop the other process or change the port in `app.py`. |
| Prediction is slow the first time | TensorFlow is loading the model; later predictions are faster. |

---

## 📄 License & Disclaimer

This project is intended for educational and decision-support purposes. Agronomic advice is a recommendation, not a guarantee. Confirm chemical names, doses, and local regulations with your nearest agriculture extension officer before spraying.

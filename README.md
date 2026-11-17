# 🌱 CropShield AI - Crop Disease Detection & Agronomic Advisory System

An end-to-end Deep Learning and Precision Agronomy web platform built with Flask, TensorFlow/Keras, and OpenCV. Farmers upload a leaf photo of **Wheat** or **Maize (Corn)**, the model identifies the disease, and the app explains the result in simple language with a spoken advisory in **English, Hindi, or Kannada**.

Repository: <https://github.com/ratnavk74/Crop_Disease.git>

---

## ✨ Key Features

| Feature | What it does |
| :--- | :--- |
| **Deep learning diagnosis** | MobileNetV2 transfer-learning model with confidence score for 7 maize/wheat classes. |
| **Explainable AI** | Grad-CAM heatmap highlights the lesion areas that influenced the prediction. |
| **Generative AI view (CycleGAN)** | A compact CycleGAN translates the uploaded leaf into a synthetic diseased/healthy view. Optional: needs a trained checkpoint in `model/gan/<crop>/`. |
| **Automatic language recognition** | Detects the browser/phone language (`Accept-Language`) on the first visit and remembers the choice in the session and user profile. |
| **Manual language switcher** | English / हिन्दी / ಕನ್ನಡ selector in the navigation bar, available on every page. |
| **Voice input** | Farmers tap the microphone and speak a question in their own language using the browser Web Speech API. |
| **Spoken replies** | The assistant answers aloud with SpeechSynthesis and also shows the reply as text. |
| **Simple reason for the disease** | A plain-language "Why did this happen?" explanation written for farmers, not agronomists. |
| **Step-by-step prevention** | A numbered checklist from pre-sowing to harvest, with a "Listen to steps" button. |
| **Camera capture** | Take a fresh leaf photo with the device camera instead of browsing for a file. |
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
├── wsgi.py                      # Gunicorn entry point
├── requirements.txt             # Python dependencies
├── requirements-gan.txt         # Optional PyTorch dependencies for inference
├── requirements-server.txt      # App + gunicorn for deployment
├── Dockerfile                   # Container deployment
├── Procfile / render.yaml       # Render / Heroku-style deployment
├── README.md                    # Setup and usage guide
├── .gitignore                   # Files that should not be committed
│
├── model/
│   ├── crop_disease_model.h5   # Trained MobileNetV2 weights
│   └── gan/                    # Optional CycleGAN checkpoints
│       ├── maize/G_AB.pth
│       └── wheat/G_AB.pth
│
├── gan/
│   ├── models.py               # CycleGAN ResNet generator + PatchGAN discriminator
│   ├── dataset.py              # Unpaired dataset and preview grids
│   ├── prepare_dataset.py      # Class folders -> trainA/trainB/testA/testB
│   ├── train_cyclegan.py       # Training loop and checkpoints
│   └── translate.py            # CLI inference (healthy <-> diseased)
│
├── notebooks/
│   └── CropShield_CycleGAN_Training.ipynb   # Colab/Kaggle training notebook
│
├── tests/
│   └── test_gan.py             # Dataset, model, checkpoint and fallback tests
│
├── utils/
│   ├── __init__.py
│   ├── auth.py                  # SQLite users, password hashing, demo seeding
│   ├── assistant.py             # Rule-based multilingual voice intents
│   ├── farmer_guides.py         # Simple reason + step-by-step prevention (EN/HI/KN)
│   ├── gan_translate.py         # Lazy CycleGAN inference for Flask
│   ├── i18n.py                  # Language detection, UI and advisory translations
│   ├── prediction.py            # Preprocessing, CNN inference and Grad-CAM
│   └── recommendation.py        # Agronomic knowledge base
│
├── static/
│   ├── css/style.css            # Responsive UI, auth pages, camera dialog, voice widget, print layout
│   ├── js/main.js               # Upload preview, camera capture, TTS helpers
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

> Use **Python 3.11** on Windows. TensorFlow does not install reliably on Python 3.13/3.14 yet.

### 1. Open the project in VS Code

```powershell
cd "C:\Users\Ratna\OneDrive\Desktop\ML_project\Crop_Disease_Enhanced"
```

If an old `venv` folder exists with a different Python version, remove it first:

```powershell
Remove-Item -Recurse -Force venv
```

### 2. Create and activate a Python 3.11 virtual environment

```powershell
py -3.11 -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt

# Optional: only if you have trained checkpoints in model/gan/<crop>/
pip install -r requirements-gan.txt
```

### 4. Start the app

```powershell
python app.py
```

### 5. Open the browser

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
* The navbar selector submits `/set-language?lang=<code>`; the older `/set-language/<code>` route is still supported.
* A language you pick on the login page is kept after you sign in, even if your saved profile uses another language.
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

### Choosing the speech language

The voice panel has a **Speak in** selector (English / हिन्दी / ಕನ್ನಡ). It is separate from the page language:

* Keep it on **हिन्दी** when you are going to speak Hindi, even if the page is in English.
* Keep it on **ಕನ್ನಡ** when you are going to speak Kannada.
* The choice is remembered in the browser (`localStorage`).
* If a browser rejects a regional tag such as `hi-IN`, the app automatically retries with the base language (`hi`) before showing an error.

Chrome and Edge send speech to an online recognition service, so Hindi/Kannada recognition needs an active internet connection. If recognition still fails, check that the correct microphone is selected in Windows and that the site is opened on `http://127.0.0.1:5000` or `localhost`.

### Browser requirements

| Requirement | Details |
| :--- | :--- |
| Browser | **Google Chrome** or **Microsoft Edge** (recommended). Firefox/Safari support varies. |
| Microphone | A working microphone and permission for the site. |
| Secure URL | `http://127.0.0.1:5000`, `http://localhost:5000`, or HTTPS. Microphone access is blocked on plain HTTP for other hosts. |
| Internet | Needed for Google Fonts / Font Awesome icons, and for some cloud speech voices. |

If voice input is unavailable, the typed/example-chip questions still work, and the audio advisory buttons on the report page can read the report aloud.

---

## 📷 Camera Capture

1. On the upload card, click **Use Camera**.
2. Allow camera permission when the browser asks.
3. Hold the affected leaf in good light, fill the frame, then click **Capture Photo**.
4. The captured photo is placed in the normal upload preview. Check it, then click **Diagnose & Generate In-Depth Advisory**.

Notes:

* Live preview needs `localhost` / `127.0.0.1` or HTTPS, and a browser with `getUserMedia` (Chrome/Edge recommended).
* On phones the **Switch Camera** button toggles between the rear and front camera.
* If live preview is unavailable or permission is denied, the app opens the phone's native camera picker instead, so the feature degrades gracefully.
* The photo is stored in `static/uploads/` only for this diagnosis and Grad-CAM report.

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
  "gradcam_url": "/static/uploads/gradcam_...",
  "gan_url": "/static/uploads/gan_..."
}
```

`gan_url` is `null` when PyTorch or the crop checkpoint is missing.

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

## 🧬 CycleGAN Generative Architecture

CropShield uses **two complementary models**:

| Model | Task | Output |
| :--- | :--- | :--- |
| **MobileNetV2 classifier** | Disease diagnosis from a leaf photo | 7 maize/wheat classes + confidence |
| **CycleGAN (generative)** | Healthy ↔ diseased leaf translation | A synthetic lesion view shown as an extra result card |

The classifier stays responsible for the diagnosis because GANs are image generators, not reliable disease classifiers. The CycleGAN adds the GenAI component: it learns the visual difference between healthy and diseased leaves and can generate a lesion-style view of the uploaded leaf.

### Architecture details

* **Generators:** two ResNet generators, `G_AB` (healthy → diseased) and `G_BA` (diseased → healthy).
* **Discriminators:** two PatchGAN discriminators, `D_A` and `D_B`.
* **Losses:** adversarial (LSGAN), cycle-consistency (L1, ×10) and identity (L1, ×5).
* **Size:** 128×128, 32 base channels, 6 residual blocks — small enough for a free Colab/Kaggle T4 GPU.
* **Checkpoint layout:**

```
model/gan/<crop>/
├── G_AB.pth      # required by the Flask app
├── G_BA.pth
├── D_A.pth
├── D_B.pth
├── config.json   # img_size, base_channels, num_blocks
└── samples/      # training previews (not required)
```

The GAN is **optional and lazy**:

* If PyTorch is missing → the result page simply hides the generative card.
* If no checkpoint exists for the detected crop → the card is hidden.
* Any inference error is swallowed, so diagnosis is never blocked.

### Dataset layout

Unpaired CycleGAN training needs two folders per crop:

```
data/cyclegan/maize/
├── trainA/   # healthy maize leaves
├── trainB/   # diseased maize leaves
├── testA/    # optional
└── testB/    # optional
```

`prepare_dataset` also accepts PlantVillage-style class folders:

```
Corn_(maize)___healthy/          -> maize / healthy
Corn_(maize)___Common_rust_/     -> maize / diseased
Wheat___healthy/                 -> wheat / healthy
Wheat___Yellow_rust/             -> wheat / diseased
```

### Training commands

```powershell
# 1. Convert class folders into trainA/trainB
python -m gan.prepare_dataset --source data/raw --output data/cyclegan --crop all

# 2. Train maize (use --epochs 20 for a quick demo)
python -m gan.train_cyclegan --dataroot data/cyclegan/maize --name maize --img-size 128 --epochs 50 --batch-size 1

# 3. Train wheat
python -m gan.train_cyclegan --dataroot data/cyclegan/wheat --name wheat --img-size 128 --epochs 50 --batch-size 1

# 4. Test a single image
python -m gan.translate --checkpoint model/gan/maize --input static/samples/maize_healthy.jpg --output lesion_preview.jpg
```

Training on this laptop is CPU-only and slow. Use the Colab/Kaggle notebook:

```
notebooks/CropShield_CycleGAN_Training.ipynb
```

It uploads the project and dataset, builds `trainA/trainB`, trains maize and wheat, shows previews, and gives you `checkpoints.zip`. Extract it into `model/gan/` and restart the app.

> **Reality check:** a CycleGAN must be trained before it produces useful images. A newly initialised model outputs noise. There is no universal pretrained crop-lesion CycleGAN that works on any dataset.

---

## 🧪 Tests

```powershell
# GAN dataset, model, checkpoint and fallback tests
python -m unittest discover -s tests -v

# Full CycleGAN training + inference smoke test (1 epoch, CPU, ~1 minute)
python -m gan.smoke_test

# Python syntax check
python -m py_compile app.py wsgi.py utils\*.py gan\*.py

# JavaScript syntax check
node --check static\js\main.js
node --check static\js\voice.js
```

The torch-based tests are skipped automatically if PyTorch is not installed. Install `requirements-gan.txt` to run them.

Expected output:

```
Ran 6 tests
OK (skipped=2)     # without PyTorch
OK                 # with PyTorch
```

---

## 🚀 Deployment

### Option 1 — Render (free tier, fastest)

1. Push the project to GitHub.
2. In Render choose **New → Blueprint** and select the repository. `render.yaml` is detected automatically.
3. Render uses:

```
Build: pip install -r requirements-server.txt
Start: gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 180
```

4. Open the generated URL and log in with the demo account.

Notes:

* Free instances sleep after inactivity, so the first request is slow.
* `users.db` and uploaded images are **ephemeral** on the free tier; they reset on redeploy.
* Only **one worker** is used because TensorFlow loads a large model into memory.

Manual start command (any Linux host):

```bash
pip install -r requirements-server.txt
gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 180
```

### Option 2 — Docker

```bash
docker build -t cropshield-ai .
docker run -p 8000:8000 -e SECRET_KEY=change-me cropshield-ai
```

Open `http://127.0.0.1:8000`.

### GAN checkpoints in production

* Commit `model/gan/<crop>/G_AB.pth` + `config.json`, or copy them into the Docker image.
* Keep checkpoints below GitHub's 100 MB file limit. If a checkpoint is larger, use Git LFS.
* PyTorch is **not** in `requirements.txt`. To enable the generative card in production, install it too:

```bash
pip install -r requirements.txt -r requirements-gan.txt
```

or change the Dockerfile build step to install both files.

---

## 🛠️ Troubleshooting

| Problem | Fix |
| :--- | :--- |
| `ModuleNotFoundError` | Activate the virtual environment and run `pip install -r requirements.txt`. |
| Model file not found | Keep `model/crop_disease_model.h5` in the project. |
| Microphone button does nothing | Use Chrome/Edge, open `localhost`/`127.0.0.1`, and allow microphone permission. |
| Hindi/Kannada speech is not recognised | In the voice panel set **Speak in** to हिन्दी or ಕನ್ನಡ, use Chrome/Edge, and check the internet connection (Chrome uses an online speech service for Indian languages). Then allow microphone permission and try again. |
| No sound in Hindi/Kannada | Install the Hindi/Kannada voice pack in Windows Settings → Time & Language → Speech, or use Chrome which may provide cloud voices. |
| Language does not change | Make sure the enhanced app is the one running on `http://127.0.0.1:5000` (not an older copy on your Desktop), then hard-refresh with `Ctrl+F5`. The app now sends `Cache-Control: no-store` for pages and versioned CSS/JS URLs. |
| Camera preview does not open | Use Chrome/Edge on `localhost`/`127.0.0.1` and allow camera permission. On phones, the native camera picker opens automatically when live preview is unavailable. |
| Login fails | Use `demo@cropshield.ai` / `demo1234`, or register a new account. Delete `users.db` only if you want to reset local accounts (the demo account is re-seeded on startup). |
| Port 5000 already in use | Stop the other process or change the port in `app.py`. |
| Prediction is slow the first time | TensorFlow is loading the model; later predictions are faster. |
| Generative AI card is missing | This is expected without a checkpoint. Install `requirements-gan.txt` and add `model/gan/<crop>/G_AB.pth`, then restart the app. |
| `ModuleNotFoundError: torch` | Run `pip install -r requirements-gan.txt`. The rest of the app works without it. |
| GAN output looks like noise | The checkpoint is untrained or the config/crop does not match. Train it with the Colab notebook or lower `--epochs` risk by training longer. |

---

## 📄 License & Disclaimer

This project is intended for educational and decision-support purposes. Agronomic advice is a recommendation, not a guarantee. Confirm chemical names, doses, and local regulations with your nearest agriculture extension officer before spraying.

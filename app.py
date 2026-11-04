import os
import secrets
import time
from datetime import timedelta
from functools import wraps

from flask import (
    Flask,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.utils import secure_filename

from utils.assistant import build_reply
from utils.auth import (
    authenticate,
    create_user,
    get_user_by_id,
    init_db,
    update_user_language,
)
from utils.i18n import (
    DEFAULT_LANGUAGE,
    LANGUAGES,
    detect_language,
    localize_disease_summaries,
    localize_recommendation,
    normalize_language,
    translate,
)
from utils.prediction import predict_disease
from utils.recommendation import get_all_diseases, get_recommendation

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
SAMPLES_FOLDER = os.path.join(BASE_DIR, "static", "samples")
SECRET_FILE = os.path.join(BASE_DIR, ".secret_key")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

# Bump this when CSS/JS changes so browsers never serve an old cached bundle.
ASSET_VERSION = "2026-11-04-camera"


def _load_secret_key():
    """Use SECRET_KEY from the environment, or a generated local key file."""
    env_key = os.environ.get("SECRET_KEY")
    if env_key:
        return env_key
    if os.path.exists(SECRET_FILE):
        with open(SECRET_FILE, "r", encoding="utf-8") as handle:
            key = handle.read().strip()
            if key:
                return key
    key = secrets.token_hex(32)
    with open(SECRET_FILE, "w", encoding="utf-8") as handle:
        handle.write(key)
    return key


app.secret_key = _load_secret_key()

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SAMPLES_FOLDER, exist_ok=True)
init_db()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.before_request
def load_language_and_user():
    """Detect language on first visit and load the signed-in farmer."""
    language = normalize_language(session.get("lang"))
    if not language:
        language = detect_language(request.headers.get("Accept-Language", ""))
        session["lang"] = language
    g.lang = language

    user_id = session.get("user_id")
    g.user = get_user_by_id(user_id) if user_id else None
    if user_id and not g.user:
        session.pop("user_id", None)


@app.context_processor
def inject_globals():
    lang = getattr(g, "lang", DEFAULT_LANGUAGE)
    user = getattr(g, "user", None)
    endpoint = request.endpoint or ""

    # The diagnosis report is produced by POST /predict, so switching language
    # there should return to the upload page instead of re-posting the form.
    language_next = "/" if endpoint in {"predict", "api_predict"} else request.path

    return {
        "t": lambda key, **kwargs: translate(key, lang, **kwargs),
        "lang": lang,
        "language_meta": LANGUAGES[lang],
        "languages": LANGUAGES,
        "current_user": user,
        "is_authenticated": bool(user),
        "speech_lang": LANGUAGES[lang]["speech"],
        "current_year": 2026,
        "asset_version": ASSET_VERSION,
        "language_next": language_next,
    }


@app.after_request
def _prevent_stale_pages(response):
    """Keep translated HTML out of the browser cache after a language switch."""
    if response.mimetype == "text/html":
        response.headers["Cache-Control"] = "no-store, max-age=0, must-revalidate"
        response.headers["Pragma"] = "no-cache"
    return response


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not getattr(g, "user", None):
            flash(translate("flash_login_required", getattr(g, "lang", DEFAULT_LANGUAGE)), "info")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)

    return wrapped_view


def _safe_next(target, fallback_endpoint="home"):
    """Only allow local redirect targets (prevents open redirects)."""
    if target and target.startswith("/") and not target.startswith("//"):
        return target
    return url_for(fallback_endpoint)


def _localized_info(disease_key):
    info = dict(get_recommendation(disease_key))
    info["key"] = disease_key
    return localize_recommendation(info, g.lang)


def _severity_code(disease, confidence):
    if "Healthy" in disease:
        return "healthy"
    if confidence >= 90:
        return "high"
    if confidence >= 75:
        return "medium"
    return "low"


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if getattr(g, "user", None):
        return redirect(url_for("home"))

    next_url = request.args.get("next", "") or request.form.get("next", "")

    if request.method == "POST":
        identifier = request.form.get("identifier", "")
        password = request.form.get("password", "")
        user = authenticate(identifier, password)

        if user:
            session["user_id"] = user["id"]

            # Keep a language the farmer explicitly picked on the login page.
            # Otherwise restore the language saved in their profile.
            saved_language = normalize_language(user["preferred_language"])
            picked_language = normalize_language(session.get("lang"))
            if session.get("lang_explicit"):
                chosen_language = picked_language or saved_language or g.lang
            else:
                chosen_language = saved_language or picked_language or g.lang
            session["lang"] = chosen_language
            update_user_language(user["id"], chosen_language)

            session.permanent = bool(request.form.get("remember"))
            flash(
                translate("flash_welcome", session["lang"], name=user["name"]),
                "success",
            )
            return redirect(_safe_next(next_url))

        flash(translate("flash_invalid_login", g.lang), "error")

    return render_template("login.html", page="login", next_url=next_url)


@app.route("/register", methods=["GET", "POST"])
def register():
    if getattr(g, "user", None):
        return redirect(url_for("home"))

    if request.method == "POST":
        name = request.form.get("name", "")
        phone = request.form.get("phone", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        preferred_language = normalize_language(request.form.get("language")) or g.lang

        if password != confirm:
            flash(translate("flash_password_mismatch", g.lang), "error")
        else:
            try:
                create_user(name, phone, email, password, preferred_language)
                flash(translate("flash_registered", g.lang), "success")
                return redirect(url_for("login"))
            except ValueError as exc:
                code = str(exc)
                key = {
                    "fill_all": "flash_fill_all",
                    "invalid_phone": "flash_invalid_phone",
                    "invalid_email": "flash_invalid_email",
                    "password_short": "flash_password_short",
                    "user_exists": "flash_user_exists",
                }.get(code, "flash_fill_all")
                flash(translate(key, g.lang), "error")

    return render_template("register.html", page="register")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash(translate("flash_logged_out", g.lang), "info")
    return redirect(url_for("login"))


@app.route("/set-language/<language>")
def set_language(language):
    code = normalize_language(language)
    if not code:
        return redirect(url_for("home") if getattr(g, "user", None) else url_for("login"))

    session["lang"] = code
    session["lang_explicit"] = True
    if getattr(g, "user", None):
        update_user_language(g.user["id"], code)

    next_url = request.args.get("next", "")
    fallback = "home" if getattr(g, "user", None) else "login"
    return redirect(_safe_next(next_url, fallback_endpoint=fallback))


@app.route("/set-language")
def set_language_query():
    """No-JavaScript fallback used by the navigation language form."""
    return set_language(request.args.get("lang", ""))


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
@app.route("/")
@login_required
def home():
    diseases = localize_disease_summaries(get_all_diseases(), g.lang)
    return render_template("index.html", diseases=diseases, page="home")


@app.route("/predict", methods=["POST"])
@login_required
def predict():
    # Handle direct sample test click or file upload
    sample_name = request.form.get("sample_name")
    filepath = None
    web_image_path = None
    web_gradcam_path = None

    if sample_name:
        sample_file = os.path.join(SAMPLES_FOLDER, os.path.basename(sample_name))
        if os.path.exists(sample_file):
            timestamp = int(time.time())
            target_filename = f"sample_{timestamp}_{os.path.basename(sample_name)}"
            filepath = os.path.join(UPLOAD_FOLDER, target_filename)
            import shutil

            shutil.copyfile(sample_file, filepath)
            web_image_path = f"uploads/{target_filename}"
            web_gradcam_path = f"uploads/gradcam_{target_filename}"

    if not filepath:
        if "image" not in request.files:
            flash(translate("error_no_file", g.lang), "error")
            return redirect(url_for("home"))

        file = request.files["image"]

        if file.filename == "":
            flash(translate("error_no_file", g.lang), "error")
            return redirect(url_for("home"))

        if file and allowed_file(file.filename):
            orig_name = secure_filename(file.filename) or "leaf.jpg"
            timestamp = int(time.time())
            unique_name = f"{timestamp}_{orig_name}"
            filepath = os.path.join(UPLOAD_FOLDER, unique_name)
            file.save(filepath)
            web_image_path = f"uploads/{unique_name}"
            web_gradcam_path = f"uploads/gradcam_{unique_name}"
        else:
            flash(translate("error_invalid_file", g.lang), "error")
            return redirect(url_for("home"))

    # Execute Deep Learning Prediction & XAI
    disease, confidence = predict_disease(filepath)

    # Retrieve Comprehensive Agronomic Advisory (localised for the farmer)
    info = _localized_info(disease)

    # Determine Severity Rating
    severity_code = _severity_code(disease, confidence)
    severity = translate(f"severity_{severity_code}", g.lang)
    severity_class = {
        "healthy": "badge-healthy",
        "high": "badge-high",
        "medium": "badge-medium",
        "low": "badge-low",
    }[severity_code]

    # Check if Grad-CAM file was generated
    full_gradcam_path = os.path.join(UPLOAD_FOLDER, f"gradcam_{os.path.basename(filepath)}")
    has_gradcam = os.path.exists(full_gradcam_path)

    return render_template(
        "result.html",
        page="result",
        disease_key=disease,
        disease=disease,
        confidence=confidence,
        severity=severity,
        severity_code=severity_code,
        severity_class=severity_class,
        # Exact fields from user's original template
        cause=info.get("cause", ""),
        symptoms=info.get("symptoms", ""),
        treatment=info.get("treatment", ""),
        prevention=info.get("prevention", ""),
        image_path=web_image_path,
        # Extended in-depth fields
        info=info,
        why_it_happened=info.get("why_it_happened", ""),
        causes=info.get("causes", ""),
        farmer_reason=info.get("farmer_reason", ""),
        prevention_steps=info.get("prevention_steps", []),
        pathogen=info.get("pathogen", ""),
        crop=info.get("crop", ""),
        display_name=info.get("display_name", disease),
        affected_area=info.get("affected_area_estimate", "N/A"),
        treatment_details=info.get("treatment_details", {}),
        prevention_details=info.get("prevention_details", {}),
        has_gradcam=has_gradcam,
        gradcam_path=web_gradcam_path if has_gradcam else None,
        voice_en=info.get("voice_en", ""),
        voice_hi=info.get("voice_hi", ""),
        voice_kn=info.get("voice_kn", ""),
        voice_script=info.get("voice", ""),
    )


# ---------------------------------------------------------------------------
# JSON API
# ---------------------------------------------------------------------------
@app.route("/api/predict", methods=["POST"])
@login_required
def api_predict():
    """REST API endpoint for mobile/IoT integration."""
    if "image" not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400

    file = request.files["image"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid image format"}), 400

    orig_name = secure_filename(file.filename) or "leaf.jpg"
    timestamp = int(time.time())
    unique_name = f"api_{timestamp}_{orig_name}"
    filepath = os.path.join(UPLOAD_FOLDER, unique_name)
    file.save(filepath)

    disease, confidence = predict_disease(filepath)
    info = _localized_info(disease)
    severity_code = _severity_code(disease, confidence)

    return jsonify(
        {
            "status": "success",
            "language": g.lang,
            "disease": disease,
            "display_name": info.get("display_name"),
            "crop": info.get("crop"),
            "pathogen": info.get("pathogen"),
            "confidence": confidence,
            "severity": translate(f"severity_{severity_code}", g.lang),
            "why_it_happened": info.get("why_it_happened"),
            "causes": info.get("causes"),
            "farmer_reason": info.get("farmer_reason"),
            "prevention_steps": info.get("prevention_steps", []),
            "symptoms": info.get("symptoms"),
            "treatment": info.get("treatment"),
            "treatment_details": info.get("treatment_details"),
            "prevention": info.get("prevention"),
            "prevention_details": info.get("prevention_details"),
            "voice": info.get("voice", ""),
            "image_url": f"/static/uploads/{unique_name}",
            "gradcam_url": f"/static/uploads/gradcam_{unique_name}",
        }
    )


@app.route("/api/diseases", methods=["GET"])
def api_diseases():
    return jsonify(localize_disease_summaries(get_all_diseases(), g.lang))


@app.route("/api/assistant", methods=["POST"])
def api_assistant():
    """Answer a recognised voice command in the farmer's language."""
    payload = request.get_json(silent=True) or {}
    text = payload.get("text", "")
    language = normalize_language(payload.get("lang")) or g.lang
    page = payload.get("page", "home")
    disease_key = payload.get("disease") or None
    confidence = payload.get("confidence")

    try:
        confidence = float(confidence) if confidence not in (None, "") else None
    except (TypeError, ValueError):
        confidence = None

    try:
        reply = build_reply(
            text=text,
            lang=language,
            page=page,
            disease_key=disease_key,
            confidence=confidence,
            is_authenticated=bool(getattr(g, "user", None)),
        )
    except Exception as exc:  # keep the voice assistant resilient
        app.logger.exception("Assistant error: %s", exc)
        reply = {
            "reply": translate("assistant_error", language),
            "action": None,
            "target": None,
            "speak": True,
            "language": language,
        }

    return jsonify(reply)


@app.errorhandler(413)
def file_too_large(_error):
    flash(translate("error_generic", getattr(g, "lang", DEFAULT_LANGUAGE)), "error")
    return redirect(url_for("home"))


if __name__ == "__main__":
    print("=" * 66)
    print("  Smart Crop Disease Detection & Agronomic Advisory System")
    print("  Languages: English | Hindi | Kannada")
    print("  Voice assistant: Web Speech API (Chrome / Edge recommended)")
    print("  Running on: http://127.0.0.1:5000")
    print("  Demo login: demo@cropshield.ai / demo1234")
    print("=" * 66)
    app.run(debug=True, port=5000)

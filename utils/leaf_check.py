"""Lightweight check that an uploaded image looks like a crop leaf.

This is intentionally heuristic: it prevents obvious mistakes (selfies, human
photos, screenshots, documents) without adding a second heavy neural network.
It never blocks valid diagnoses if the check itself fails.

Returns a tuple ``(ok, reason)`` where ``reason`` is ``"human"``,
``"not_leaf"`` or an empty string.
"""

import os

import cv2
import numpy as np

_face_cascade = None
_face_cascade_loaded = False


def _get_face_cascade():
    """Load the bundled OpenCV frontal-face detector once."""
    global _face_cascade, _face_cascade_loaded
    if _face_cascade_loaded:
        return _face_cascade

    _face_cascade_loaded = True
    try:
        path = os.path.join(
            cv2.data.haarcascades, "haarcascade_frontalface_default.xml"
        )
        cascade = cv2.CascadeClassifier(path)
        _face_cascade = None if cascade.empty() else cascade
    except Exception:
        _face_cascade = None
    return _face_cascade


def _detect_faces(img_rgb):
    cascade = _get_face_cascade()
    if cascade is None:
        return 0

    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    gray = cv2.equalizeHist(gray)
    height, width = gray.shape[:2]
    if max(height, width) > 480:
        scale = 480.0 / max(height, width)
        gray = cv2.resize(gray, (int(width * scale), int(height * scale)))
        height, width = gray.shape[:2]

    min_size = max(30, int(min(height, width) * 0.18))
    try:
        faces = cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=6,
            minSize=(min_size, min_size),
            maxSize=(int(width * 0.9), int(height * 0.9)),
        )
    except Exception:
        return 0
    return 0 if faces is None else len(faces)


def _color_metrics(img_rgb):
    hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
    hue, sat, val = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]

    green = (hue >= 30) & (hue <= 95) & (sat >= 35) & (val >= 30)
    plant = (hue >= 8) & (hue <= 38) & (sat >= 40) & (val >= 35)

    ycrcb = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2YCrCb)
    cr, cb = ycrcb[:, :, 1], ycrcb[:, :, 2]

    red = img_rgb[:, :, 0].astype(np.int16)
    grn = img_rgb[:, :, 1].astype(np.int16)
    blu = img_rgb[:, :, 2].astype(np.int16)

    skin_rgb = (
        (red > 95)
        & (grn > 40)
        & (blu > 20)
        & ((red - grn) > 15)
        & ((red - blu) > 15)
        & (np.abs(red - grn) > 10)
    )
    skin_ycc = (cr >= 135) & (cr <= 180) & (cb >= 80) & (cb <= 135)
    skin = skin_rgb & skin_ycc

    height, width = img_rgb.shape[:2]
    center = np.zeros((height, width), dtype=bool)
    center[height // 4 : (height * 3) // 4, width // 4 : (width * 3) // 4] = True

    total = float(height * width) or 1.0
    return {
        "green": float(np.count_nonzero(green)) / total,
        "plant": float(np.count_nonzero(plant | green)) / total,
        "skin": float(np.count_nonzero(skin)) / total,
        "mean_sat": float(np.mean(sat)),
        "center_green": float(np.count_nonzero(green & center)) / max(1, np.count_nonzero(center)),
        "border_green": float(np.count_nonzero(green & ~center)) / max(1, np.count_nonzero(~center)),
        "center_skin": float(np.count_nonzero(skin & center)) / max(1, np.count_nonzero(center)),
    }


def check_leaf_image(image_path):
    """Return ``(True, "")`` for a likely leaf photo, else a rejection reason."""
    try:
        img_bgr = cv2.imread(image_path)
        if img_bgr is None:
            from PIL import Image

            pil_image = Image.open(image_path).convert("RGB")
            img_bgr = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        if img_bgr is None or img_bgr.size == 0:
            return True, ""

        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        height, width = img_rgb.shape[:2]
        if max(height, width) > 640:
            scale = 640.0 / max(height, width)
            img_rgb = cv2.resize(
                img_rgb, (int(width * scale), int(height * scale)),
                interpolation=cv2.INTER_AREA,
            )

        if _detect_faces(img_rgb) > 0:
            return False, "human"

        metrics = _color_metrics(img_rgb)

        # A person standing in front of grass/trees: green background, but the
        # centre of the frame is skin/clothing rather than a leaf.
        if (
            metrics["center_green"] < 0.12
            and (metrics["border_green"] - metrics["center_green"]) >= 0.18
            and metrics["center_skin"] >= 0.12
        ):
            return False, "human"

        # Clear vegetation, including yellow/brown diseased leaves.
        if metrics["green"] >= 0.10:
            return True, ""
        if metrics["plant"] >= 0.30 and metrics["green"] >= 0.03:
            return True, ""

        # Large areas of skin with almost no vegetation.
        if metrics["skin"] >= 0.28:
            return False, "human"

        # Screenshots, documents, night photos, grayscale images.
        if metrics["green"] < 0.04 and metrics["mean_sat"] < 25:
            return False, "not_leaf"
        if metrics["plant"] < 0.15:
            return False, "not_leaf"

        return True, ""
    except Exception:
        # Never let the validator block the real diagnosis.
        return True, ""

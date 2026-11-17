"""Tests for the non-leaf / human-photo upload guard."""

import io
import os
import sys
import tempfile
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PIL import Image  # noqa: E402

from utils.leaf_check import check_leaf_image  # noqa: E402


def _save_image(path, color, size=(320, 320)):
    Image.new("RGB", size, color).save(path)
    return path


class LeafCheckTests(unittest.TestCase):
    def test_benchmark_samples_are_accepted(self):
        samples = os.path.join(PROJECT_ROOT, "static", "samples")
        for name in sorted(os.listdir(samples)):
            if not name.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            with self.subTest(sample=name):
                ok, reason = check_leaf_image(os.path.join(samples, name))
                self.assertTrue(ok, f"{name} was rejected as {reason}")

    def test_skin_tone_image_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = _save_image(os.path.join(tmp, "face.png"), (224, 172, 105))
            ok, reason = check_leaf_image(path)
            self.assertFalse(ok)
            self.assertEqual(reason, "human")

    def test_gray_image_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = _save_image(os.path.join(tmp, "gray.png"), (128, 128, 128))
            ok, reason = check_leaf_image(path)
            self.assertFalse(ok)
            self.assertEqual(reason, "not_leaf")

    def test_missing_file_does_not_block_diagnosis(self):
        ok, reason = check_leaf_image(os.path.join(PROJECT_ROOT, "does_not_exist.jpg"))
        self.assertTrue(ok)
        self.assertEqual(reason, "")

    def test_flask_rejects_human_upload(self):
        try:
            from app import app
        except Exception as exc:  # TensorFlow not installed
            self.skipTest(f"Flask app unavailable: {exc}")

        app.config.update(TESTING=True)
        client = app.test_client()
        client.post(
            "/login",
            data={"identifier": "demo@cropshield.ai", "password": "demo1234"},
        )
        client.get("/set-language?lang=en&next=/")

        buffer = io.BytesIO()
        Image.new("RGB", (320, 320), (224, 172, 105)).save(buffer, format="PNG")
        buffer.seek(0)

        response = client.post(
            "/predict",
            data={"image": (buffer, "person.png")},
            content_type="multipart/form-data",
            follow_redirects=True,
        )
        body = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("does not look like a maize or wheat leaf", body)

    def test_api_rejects_human_upload(self):
        try:
            from app import app
        except Exception as exc:
            self.skipTest(f"Flask app unavailable: {exc}")

        app.config.update(TESTING=True)
        client = app.test_client()
        client.post(
            "/login",
            data={"identifier": "demo@cropshield.ai", "password": "demo1234"},
        )

        buffer = io.BytesIO()
        Image.new("RGB", (320, 320), (224, 172, 105)).save(buffer, format="PNG")
        buffer.seek(0)

        response = client.post(
            "/api/predict",
            data={"image": (buffer, "person.png")},
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())


if __name__ == "__main__":
    unittest.main(verbosity=2)

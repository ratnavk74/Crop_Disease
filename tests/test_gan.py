"""Tests for the optional CycleGAN pipeline.

Run with::

    python -m unittest discover -s tests -v

The torch-based tests are skipped automatically when PyTorch is not
installed, so the Flask app can still be tested on a light machine.
"""

import json
import os
import sys
import tempfile
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gan import prepare_dataset  # noqa: E402
from utils import gan_translate  # noqa: E402

try:
    import torch  # noqa: F401
    import torchvision  # noqa: F401

    HAS_TORCH = True
except Exception:
    HAS_TORCH = False


def _write_image(path, color=(40, 120, 40), size=(96, 96)):
    from PIL import Image

    os.makedirs(os.path.dirname(path), exist_ok=True)
    Image.new("RGB", size, color).save(path)


class PrepareDatasetTests(unittest.TestCase):
    def test_flat_plantvillage_layout(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = os.path.join(tmp, "raw")
            output = os.path.join(tmp, "out")
            _write_image(os.path.join(source, "Corn_(maize)___healthy", "a.jpg"))
            _write_image(os.path.join(source, "Corn_(maize)___healthy", "b.jpg"))
            _write_image(os.path.join(source, "Corn_(maize)___Common_rust_", "c.jpg"))
            _write_image(os.path.join(source, "Corn_(maize)___Common_rust_", "d.jpg"))
            _write_image(os.path.join(source, "Wheat___healthy", "e.jpg"))
            _write_image(os.path.join(source, "Wheat___Yellow_rust", "f.jpg"))

            original_argv = sys.argv
            try:
                sys.argv = [
                    "prepare_dataset",
                    "--source", source,
                    "--output", output,
                    "--crop", "all",
                    "--test-split", "0",
                ]
                prepare_dataset.main()
            finally:
                sys.argv = original_argv

            maize = os.path.join(output, "maize")
            wheat = os.path.join(output, "wheat")
            self.assertTrue(os.path.isdir(os.path.join(maize, "trainA")))
            self.assertTrue(os.path.isdir(os.path.join(maize, "trainB")))
            self.assertTrue(os.path.isdir(os.path.join(wheat, "trainA")))
            self.assertTrue(os.path.isdir(os.path.join(wheat, "trainB")))
            self.assertEqual(len(os.listdir(os.path.join(maize, "trainA"))), 2)
            self.assertEqual(len(os.listdir(os.path.join(maize, "trainB"))), 2)
            self.assertEqual(len(os.listdir(os.path.join(wheat, "trainA"))), 1)
            self.assertEqual(len(os.listdir(os.path.join(wheat, "trainB"))), 1)

    def test_crop_subfolders_layout(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = os.path.join(tmp, "raw")
            output = os.path.join(tmp, "out")
            _write_image(os.path.join(source, "maize", "Healthy", "a.jpg"))
            _write_image(os.path.join(source, "maize", "Rust", "b.jpg"))

            original_argv = sys.argv
            try:
                sys.argv = [
                    "prepare_dataset",
                    "--source", source,
                    "--output", output,
                    "--crop", "maize",
                    "--test-split", "0",
                ]
                prepare_dataset.main()
            finally:
                sys.argv = original_argv

            self.assertTrue(os.path.isdir(os.path.join(output, "maize", "trainA")))
            self.assertTrue(os.path.isdir(os.path.join(output, "maize", "trainB")))


class GanAvailabilityTests(unittest.TestCase):
    def test_crop_detection(self):
        self.assertEqual(gan_translate.crop_from_disease("Maize_CommonRust"), "maize")
        self.assertEqual(gan_translate.crop_from_disease("Wheat_YellowRust"), "wheat")
        self.assertEqual(gan_translate.crop_from_disease("Unknown"), "")
        self.assertEqual(gan_translate.normalize_crop("Corn"), "maize")

    def test_missing_checkpoint_is_safe(self):
        gan_translate.reset_cache()
        self.assertFalse(gan_translate.gan_available("maize"))
        self.assertFalse(gan_translate.gan_available(""))
        self.assertFalse(
            gan_translate.translate_leaf(os.path.join(PROJECT_ROOT, "missing.jpg"), "maize", "out.jpg")
        )


@unittest.skipUnless(HAS_TORCH, "PyTorch is not installed")
class CycleGanModelTests(unittest.TestCase):
    def test_generator_and_discriminator_shapes(self):
        import torch
        from gan.models import build_discriminator, build_generator

        generator = build_generator(base_channels=8, num_blocks=2).eval()
        discriminator = build_discriminator(base_channels=8, n_layers=2).eval()

        with torch.no_grad():
            image = torch.randn(1, 3, 64, 64)
            output = generator(image)
            patch = discriminator(image)

        self.assertEqual(tuple(output.shape), (1, 3, 64, 64))
        self.assertEqual(patch.shape[0], 1)
        self.assertEqual(patch.shape[1], 1)

    def test_checkpoint_round_trip_and_inference(self):
        from gan.models import build_generator
        from gan.translate import load_generator, translate_image

        with tempfile.TemporaryDirectory() as tmp:
            checkpoint = os.path.join(tmp, "maize")
            os.makedirs(checkpoint, exist_ok=True)
            with open(os.path.join(checkpoint, "config.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {"img_size": 64, "base_channels": 8, "num_blocks": 2}, handle
                )

            model = build_generator(base_channels=8, num_blocks=2)
            import torch

            torch.save(model.state_dict(), os.path.join(checkpoint, "G_AB.pth"))

            generator, size = load_generator(checkpoint, direction="ab")
            self.assertEqual(size, 64)

            source = os.path.join(tmp, "leaf.jpg")
            _write_image(source)
            output = os.path.join(tmp, "lesion.jpg")
            translate_image(generator, size, source, output)
            self.assertTrue(os.path.exists(output))
            self.assertGreater(os.path.getsize(output), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)

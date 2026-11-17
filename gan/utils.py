"""Small dependency-free helpers shared by the GAN scripts.

Keeping these separate means ``gan.prepare_dataset`` works without PyTorch
installed, which is important for the Flask app and the test suite.
"""

import os

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def is_image_file(filename):
    return os.path.splitext(filename)[1].lower() in IMAGE_EXTENSIONS

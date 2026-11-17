"""End-to-end CPU smoke test for the CycleGAN pipeline.

It builds a tiny dataset from ``static/samples``, trains for one epoch at
64×64 with a small network, then runs inference.  This does **not** produce a
useful model — it only proves that the training and inference code work.

Run::

    python -m gan.smoke_test

Requires PyTorch (``pip install -r requirements-gan.txt``).
"""

import os
import shutil
import sys
import tempfile

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gan.utils import is_image_file  # noqa: E402


def build_sample_dataset(root):
    samples = os.path.join(PROJECT_ROOT, "static", "samples")
    train_a = os.path.join(root, "trainA")
    train_b = os.path.join(root, "trainB")
    os.makedirs(train_a, exist_ok=True)
    os.makedirs(train_b, exist_ok=True)

    copied_a = copied_b = 0
    for name in sorted(os.listdir(samples)):
        if not is_image_file(name):
            continue
        source = os.path.join(samples, name)
        if "healthy" in name.lower():
            shutil.copyfile(source, os.path.join(train_a, name))
            copied_a += 1
        else:
            shutil.copyfile(source, os.path.join(train_b, name))
            copied_b += 1

    if not copied_a or not copied_b:
        raise SystemExit("Not enough sample images (need healthy and diseased leaves).")
    print(f"[smoke] Dataset: {copied_a} healthy, {copied_b} diseased")
    return train_a, train_b


def main():
    try:
        import torch
    except Exception:
        raise SystemExit("PyTorch is not installed. Run: pip install -r requirements-gan.txt")

    with tempfile.TemporaryDirectory() as tmp:
        dataset = os.path.join(tmp, "dataset")
        build_sample_dataset(dataset)

        checkpoint_root = os.path.join(tmp, "checkpoints")
        command = [
            sys.executable, "-m", "gan.train_cyclegan",
            "--dataroot", dataset,
            "--name", "smoke",
            "--save-dir", checkpoint_root,
            "--img-size", "64",
            "--base-channels", "8",
            "--num-blocks", "2",
            "--n-layers", "2",
            "--epochs", "1",
            "--decay-epoch", "1",
            "--sample-every", "1",
            "--num-workers", "0",
        ]
        print("[smoke] Training:", " ".join(command))
        import subprocess

        subprocess.run(command, check=True, cwd=PROJECT_ROOT)

        checkpoint = os.path.join(checkpoint_root, "smoke")
        for required in ("G_AB.pth", "G_BA.pth", "config.json"):
            if not os.path.exists(os.path.join(checkpoint, required)):
                raise SystemExit(f"Missing checkpoint file: {required}")

        from gan.translate import load_generator, translate_image

        generator, size = load_generator(checkpoint)
        source = os.path.join(dataset, "trainA")
        images = sorted(os.listdir(source))
        output = os.path.join(tmp, "lesion.jpg")
        translate_image(generator, size, os.path.join(source, images[0]), output)

        if not os.path.exists(output) or os.path.getsize(output) == 0:
            raise SystemExit("Inference did not write an output image")

        print(f"[smoke] Inference OK: {output} ({os.path.getsize(output)} bytes)")
        print("[smoke] CycleGAN pipeline works. Train a real model in Colab/Kaggle.")


if __name__ == "__main__":
    main()

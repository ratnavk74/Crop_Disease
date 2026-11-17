"""Prepare an unpaired CycleGAN dataset from class folders.

Expected input, option 1 (crop folders)**::

    raw/
        maize/
            Maize_Healthy/          -> domain A (healthy)
            Maize_Common_Rust/      -> domain B (diseased)
            Maize_Blight/           -> domain B
        wheat/
            Wheat_Healthy/          -> domain A
            Wheat_Yellow_Rust/      -> domain B
            ...

Option 2 (flat PlantVillage-style class folders)**::

    raw/
        Corn_(maize)___healthy/             -> maize, domain A
        Corn_(maize)___Common_rust_/        -> maize, domain B
        Wheat___healthy/                    -> wheat, domain A
        Wheat___Yellow_rust/                -> wheat, domain B
        ...

Usage::

    python -m gan.prepare_dataset --source data/raw --output data/cyclegan --crop maize
    python -m gan.prepare_dataset --source data/raw --output data/cyclegan --crop wheat
    python -m gan.prepare_dataset --source data/raw --output data/cyclegan --crop all

You can also point ``--source`` directly at one crop folder without a crop
subdirectory.
"""

import argparse
import os
import random
import shutil

from gan.utils import is_image_file

CROP_ALIASES = {
    "maize": ("maize", "corn"),
    "wheat": ("wheat",),
}


def parse_args():
    parser = argparse.ArgumentParser(description="Build trainA/trainB folders for CycleGAN")
    parser.add_argument("--source", required=True, help="Folder with class subfolders")
    parser.add_argument("--output", default="data/cyclegan", help="Destination root")
    parser.add_argument("--crop", choices=["maize", "wheat", "all"], default="all")
    parser.add_argument("--test-split", type=float, default=0.15)
    parser.add_argument("--max-per-class", type=int, default=0, help="0 = use every image")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def detect_crop(name):
    """Infer the crop from a folder name such as ``Corn_(maize)___healthy``."""
    lowered = name.lower()
    for crop, aliases in CROP_ALIASES.items():
        if any(alias in lowered for alias in aliases):
            return crop
    return ""


def collect_class_images(root, crop=None, max_per_class=0):
    """Return ``(healthy, diseased)`` image paths found in class folders."""
    healthy = []
    diseased = []

    for name in sorted(os.listdir(root)):
        directory = os.path.join(root, name)
        if not os.path.isdir(directory):
            continue

        folder_crop = detect_crop(name)
        if crop and folder_crop and folder_crop != crop:
            continue

        files = [os.path.join(directory, f) for f in sorted(os.listdir(directory)) if is_image_file(f)]
        if not files:
            continue
        if max_per_class > 0:
            files = files[:max_per_class]

        if "healthy" in name.lower():
            healthy.extend(files)
            print(f"  healthy  {name}: {len(files)}")
        else:
            diseased.extend(files)
            print(f"  diseased {name}: {len(files)}")
    return healthy, diseased


def split_files(files, test_split, seed):
    files = list(files)
    random.Random(seed).shuffle(files)
    test_count = int(round(len(files) * test_split))
    if test_split > 0 and len(files) > 1 and test_count == 0:
        test_count = 1
    return files[test_count:], files[:test_count]


def copy_files(files, destination):
    os.makedirs(destination, exist_ok=True)
    for index, source in enumerate(files):
        extension = os.path.splitext(source)[1].lower()
        target = os.path.join(destination, f"{index:05d}{extension}")
        shutil.copyfile(source, target)
    return len(files)


def prepare_crop(source, output, crop, test_split, max_per_class, seed):
    print(f"\n[prepare] Crop: {crop}")
    print(f"[prepare] Source: {source}")
    healthy, diseased = collect_class_images(source, crop, max_per_class)

    if not healthy:
        raise SystemExit(f"No healthy {crop} images found under {source}")
    if not diseased:
        raise SystemExit(f"No diseased {crop} images found under {source}")

    train_a, test_a = split_files(healthy, test_split, seed)
    train_b, test_b = split_files(diseased, test_split, seed + 1)

    crop_out = os.path.join(output, crop)
    counts = {
        "trainA": copy_files(train_a, os.path.join(crop_out, "trainA")),
        "testA": copy_files(test_a, os.path.join(crop_out, "testA")),
        "trainB": copy_files(train_b, os.path.join(crop_out, "trainB")),
        "testB": copy_files(test_b, os.path.join(crop_out, "testB")),
    }
    print(f"[prepare] {counts}")
    print(f"[prepare] Dataset ready: {crop_out}")
    print("[prepare] Train with:")
    print(f"  python -m gan.train_cyclegan --dataroot {crop_out} --name {crop} --img-size 128 --epochs 50")


def find_crop_subfolders(source, crop):
    """Return crop subfolders when the dataset is grouped by crop."""
    candidate = os.path.join(source, crop)
    return candidate if os.path.isdir(candidate) else None


def main():
    args = parse_args()
    source = os.path.abspath(args.source)
    output = os.path.abspath(args.output)

    if not os.path.isdir(source):
        raise SystemExit(f"Source folder not found: {source}")

    if args.crop == "all":
        crops = ["maize", "wheat"]
    else:
        crops = [args.crop]

    prepared = 0
    for crop in crops:
        crop_source = find_crop_subfolders(source, crop) or source
        if not os.path.isdir(crop_source):
            print(f"[prepare] Skipping {crop}: folder not found")
            continue

        healthy, diseased = collect_class_images(crop_source, crop, args.max_per_class)
        if not healthy or not diseased:
            print(
                f"[prepare] Skipping {crop}: found healthy={len(healthy)} diseased={len(diseased)}. "
                "Class folder names must contain 'healthy' or the crop name."
            )
            continue

        prepare_crop(crop_source, output, crop, args.test_split, args.max_per_class, args.seed)
        prepared += 1

    if not prepared:
        raise SystemExit(
            "No usable crop datasets found. Expected folders such as "
            "maize/ and wheat/, or PlantVillage class names like "
            "'Corn_(maize)___healthy' and 'Wheat___Yellow_rust'."
        )


if __name__ == "__main__":
    main()

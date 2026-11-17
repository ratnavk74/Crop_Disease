"""Optional CycleGAN inference for the Flask app.

The heavy PyTorch imports are lazy: if ``torch`` is not installed, or no
checkpoint exists, the rest of CropShield keeps working normally.

Checkpoint layout::

    model/gan/<crop>/G_AB.pth
    model/gan/<crop>/config.json
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAN_ROOT = os.path.join(BASE_DIR, "model", "gan")

_generator_cache = {}


def _load_deps():
    try:
        import torch
        from torchvision import transforms
    except Exception:
        return None
    return torch, transforms


def normalize_crop(crop):
    value = (crop or "").strip().lower()
    if value.startswith("maize") or value.startswith("corn"):
        return "maize"
    if value.startswith("wheat"):
        return "wheat"
    return value


def crop_from_disease(disease_key):
    """Map a disease key such as ``Wheat_YellowRust`` to ``wheat``."""
    key = (disease_key or "").lower()
    if key.startswith("maize") or key.startswith("corn"):
        return "maize"
    if key.startswith("wheat"):
        return "wheat"
    return ""


def checkpoint_dir(crop):
    return os.path.join(GAN_ROOT, normalize_crop(crop))


def gan_available(crop):
    """True when torch and a trained checkpoint for this crop are present."""
    crop = normalize_crop(crop)
    if not crop or _load_deps() is None:
        return False
    directory = checkpoint_dir(crop)
    return os.path.exists(os.path.join(directory, "G_AB.pth"))


def _load_generator(crop):
    deps = _load_deps()
    if deps is None:
        return None

    import sys

    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)

    from gan.models import build_generator

    torch, _transforms = deps
    directory = checkpoint_dir(crop)
    weights_path = os.path.join(directory, "G_AB.pth")
    config_path = os.path.join(directory, "config.json")

    if not os.path.exists(weights_path):
        return None

    config = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as handle:
                config = json.load(handle)
        except (OSError, ValueError):
            config = {}

    model = build_generator(
        base_channels=int(config.get("base_channels", 32)),
        num_blocks=int(config.get("num_blocks", 6)),
    )
    state = torch.load(weights_path, map_location="cpu")
    if isinstance(state, dict) and "state_dict" in state:
        state = state["state_dict"]
    model.load_state_dict(state)
    model.eval()
    return {
        "model": model,
        "img_size": int(config.get("img_size", 128)),
    }


def _cached_generator(crop):
    crop = normalize_crop(crop)
    if crop in _generator_cache:
        return _generator_cache[crop]
    loaded = _load_generator(crop)
    if loaded is not None:
        _generator_cache[crop] = loaded
    return loaded


def translate_leaf(image_path, crop, output_path):
    """Generate a diseased-looking version of a healthy leaf.

    Returns ``True`` when the output image was written.  Any failure is
    swallowed so a missing/broken GAN never breaks the diagnosis flow.
    """
    crop = normalize_crop(crop)
    if not crop or not os.path.exists(image_path):
        return False

    loaded = _cached_generator(crop)
    if loaded is None:
        return False

    deps = _load_deps()
    if deps is None:
        return False
    _torch, transforms = deps

    try:
        from PIL import Image

        image = Image.open(image_path).convert("RGB")
        size = loaded["img_size"]
        transform = transforms.Compose([
            transforms.Resize((size, size), Image.BICUBIC),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        ])
        tensor = transform(image).unsqueeze(0)

        with _torch.no_grad():
            output = loaded["model"](tensor).squeeze(0).clamp(-1, 1)

        output = (output + 1.0) / 2.0
        result = transforms.ToPILImage()(output.cpu())

        directory = os.path.dirname(os.path.abspath(output_path))
        if directory:
            os.makedirs(directory, exist_ok=True)
        result.save(output_path, quality=92)
        return True
    except Exception:
        return False


def reset_cache():
    """Clear loaded generators (useful for tests)."""
    _generator_cache.clear()

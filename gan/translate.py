"""Run a trained CycleGAN generator on leaf images.

Examples::

    # single image: healthy -> diseased
    python -m gan.translate --checkpoint model/gan/maize --input leaf.jpg --output lesion.jpg

    # a whole folder
    python -m gan.translate --checkpoint model/gan/wheat --input photos/ --output translated/

The checkpoint directory must contain ``G_AB.pth`` and ``config.json`` as
written by ``gan.train_cyclegan``.
"""

import argparse
import json
import os
import sys

from PIL import Image
from torchvision import transforms

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gan.utils import is_image_file  # noqa: E402
from gan.models import build_generator  # noqa: E402


def parse_args():
    parser = argparse.ArgumentParser(description="Translate leaf images with a trained CycleGAN")
    parser.add_argument("--checkpoint", required=True, help="Directory containing G_AB.pth and config.json")
    parser.add_argument("--input", required=True, help="Image file or directory")
    parser.add_argument("--output", required=True, help="Output image file or directory")
    parser.add_argument("--img-size", type=int, default=None, help="Override config image size")
    parser.add_argument("--direction", choices=["ab", "ba"], default="ab",
                        help="ab = healthy -> diseased, ba = diseased -> healthy")
    return parser.parse_args()


def load_generator(checkpoint_dir, img_size=None, direction="ab"):
    import torch

    config_path = os.path.join(checkpoint_dir, "config.json")
    config = {}
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as handle:
            config = json.load(handle)

    size = img_size or int(config.get("img_size", 128))
    generator = build_generator(
        base_channels=int(config.get("base_channels", 32)),
        num_blocks=int(config.get("num_blocks", 6)),
    )
    weights_name = "G_AB.pth" if direction == "ab" else "G_BA.pth"
    weights_path = os.path.join(checkpoint_dir, weights_name)
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"Checkpoint not found: {weights_path}")

    state = torch.load(weights_path, map_location="cpu")
    if isinstance(state, dict) and "state_dict" in state:
        state = state["state_dict"]
    generator.load_state_dict(state)
    generator.eval()
    return generator, size


def translate_image(generator, img_size, image_path, output_path):
    import torch

    image = Image.open(image_path).convert("RGB")
    transform = transforms.Compose([
        transforms.Resize((img_size, img_size), Image.BICUBIC),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ])
    tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = generator(tensor).squeeze(0).clamp(-1, 1)

    output = (output + 1.0) / 2.0
    result = transforms.ToPILImage()(output.cpu())
    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
    result.save(output_path, quality=92)
    return output_path


def main():
    args = parse_args()
    generator, img_size = load_generator(args.checkpoint, args.img_size, args.direction)

    if os.path.isdir(args.input):
        os.makedirs(args.output, exist_ok=True)
        files = [name for name in sorted(os.listdir(args.input)) if is_image_file(name)]
        if not files:
            raise SystemExit(f"No images found in {args.input}")
        for name in files:
            source = os.path.join(args.input, name)
            target = os.path.join(args.output, name)
            translate_image(generator, img_size, source, target)
            print(f"[CycleGAN] {source} -> {target}")
        print(f"[CycleGAN] Done. {len(files)} image(s) written to {args.output}")
    else:
        translate_image(generator, img_size, args.input, args.output)
        print(f"[CycleGAN] {args.input} -> {args.output}")


if __name__ == "__main__":
    main()

"""Train a CycleGAN for healthy <-> diseased leaf translation.

Example (Colab / local GPU)::

    python -m gan.train_cyclegan \
        --dataroot data/cyclegan/maize \
        --name maize_cyclegan \
        --img-size 128 \
        --epochs 50 \
        --batch-size 1

The script writes checkpoints and a ``config.json`` to::

    model/gan/<name>/
        G_AB.pth      # healthy -> diseased generator
        G_BA.pth      # diseased -> healthy generator
        D_A.pth
        D_B.pth
        config.json
        samples/      # visual previews

For the Flask app, name the run ``maize`` or ``wheat`` so
``utils/gan_translate.py`` finds it automatically.
"""

import argparse
import json
import os
import random
import sys
import time

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision.utils import save_image

# Allow running as ``python gan/train_cyclegan.py`` as well as ``-m``.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gan.dataset import UnalignedDataset, make_sample_grid  # noqa: E402
from gan.models import build_discriminator, build_generator, weights_init  # noqa: E402


def parse_args():
    parser = argparse.ArgumentParser(description="Train a CycleGAN for leaf lesion translation")
    parser.add_argument("--dataroot", required=True, help="Folder containing trainA/trainB")
    parser.add_argument("--name", default="cyclegan", help="Experiment name (use maize or wheat for the app)")
    parser.add_argument("--save-dir", default=os.path.join(PROJECT_ROOT, "model", "gan"))
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--decay-epoch", type=int, default=25)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--img-size", type=int, default=128)
    parser.add_argument("--base-channels", type=int, default=32)
    parser.add_argument("--num-blocks", type=int, default=6)
    parser.add_argument("--n-layers", type=int, default=3)
    parser.add_argument("--lr", type=float, default=0.0002)
    parser.add_argument("--lambda-cycle", type=float, default=10.0)
    parser.add_argument("--lambda-identity", type=float, default=5.0)
    parser.add_argument("--sample-every", type=int, default=5)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoints in save-dir/name")
    return parser.parse_args()


def set_seed(seed):
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def lr_lambda_factory(epochs, decay_epoch):
    def lr_lambda(epoch):
        if epoch < decay_epoch:
            return 1.0
        remaining = max(1, epochs - decay_epoch)
        return max(0.0, 1.0 - (epoch - decay_epoch) / remaining)

    return lr_lambda


def save_checkpoint(directory, name, model):
    torch.save(model.state_dict(), os.path.join(directory, f"{name}.pth"))


def load_checkpoint(directory, name, model, device):
    path = os.path.join(directory, f"{name}.pth")
    if not os.path.exists(path):
        return False
    model.load_state_dict(torch.load(path, map_location=device))
    return True


def main():
    args = parse_args()
    set_seed(args.seed)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    out_dir = os.path.join(args.save_dir, args.name)
    sample_dir = os.path.join(out_dir, "samples")
    os.makedirs(sample_dir, exist_ok=True)

    print(f"[CycleGAN] Device: {device}")
    print(f"[CycleGAN] Dataset: {args.dataroot}")
    print(f"[CycleGAN] Output:  {out_dir}")

    dataset = UnalignedDataset(args.dataroot, phase="train", img_size=args.img_size, augment=True)
    loader = DataLoader(
        dataset,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=args.num_workers,
        drop_last=False,
    )
    print(f"[CycleGAN] Images: A={len(dataset.files_A)}  B={len(dataset.files_B)}")

    G_AB = build_generator(args.base_channels, args.num_blocks).to(device)
    G_BA = build_generator(args.base_channels, args.num_blocks).to(device)
    D_A = build_discriminator(args.base_channels, args.n_layers).to(device)
    D_B = build_discriminator(args.base_channels, args.n_layers).to(device)

    G_AB.apply(weights_init)
    G_BA.apply(weights_init)
    D_A.apply(weights_init)
    D_B.apply(weights_init)

    criterion_gan = nn.MSELoss()
    criterion_cycle = nn.L1Loss()
    criterion_identity = nn.L1Loss()

    optimizer_G = torch.optim.Adam(
        list(G_AB.parameters()) + list(G_BA.parameters()),
        lr=args.lr,
        betas=(0.5, 0.999),
    )
    optimizer_D_A = torch.optim.Adam(D_A.parameters(), lr=args.lr, betas=(0.5, 0.999))
    optimizer_D_B = torch.optim.Adam(D_B.parameters(), lr=args.lr, betas=(0.5, 0.999))

    lr_lambda = lr_lambda_factory(args.epochs, args.decay_epoch)
    scheduler_G = torch.optim.lr_scheduler.LambdaLR(optimizer_G, lr_lambda=lr_lambda)
    scheduler_D_A = torch.optim.lr_scheduler.LambdaLR(optimizer_D_A, lr_lambda=lr_lambda)
    scheduler_D_B = torch.optim.lr_scheduler.LambdaLR(optimizer_D_B, lr_lambda=lr_lambda)

    config = {
        "img_size": args.img_size,
        "base_channels": args.base_channels,
        "num_blocks": args.num_blocks,
        "n_layers": args.n_layers,
        "domain_a": "healthy",
        "domain_b": "diseased",
        "generator": "cyclegan_resnet",
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    with open(os.path.join(out_dir, "config.json"), "w", encoding="utf-8") as handle:
        json.dump(config, handle, indent=2)

    if args.resume:
        loaded = [
            load_checkpoint(out_dir, "G_AB", G_AB, device),
            load_checkpoint(out_dir, "G_BA", G_BA, device),
            load_checkpoint(out_dir, "D_A", D_A, device),
            load_checkpoint(out_dir, "D_B", D_B, device),
        ]
        print(f"[CycleGAN] Resumed checkpoints: {sum(loaded)}/4")

    start = time.time()
    for epoch in range(1, args.epochs + 1):
        G_AB.train()
        G_BA.train()
        D_A.train()
        D_B.train()

        running = {"g": 0.0, "d": 0.0, "cycle": 0.0, "identity": 0.0}
        steps = 0

        for batch in loader:
            real_A = batch["A"].to(device)
            real_B = batch["B"].to(device)
            steps += 1

            # ------------------ Generators ------------------
            optimizer_G.zero_grad(set_to_none=True)

            fake_B = G_AB(real_A)
            rec_A = G_BA(fake_B)
            fake_A = G_BA(real_B)
            rec_B = G_AB(fake_A)

            loss_identity_A = criterion_identity(G_BA(real_A), real_A) * args.lambda_identity
            loss_identity_B = criterion_identity(G_AB(real_B), real_B) * args.lambda_identity
            loss_identity = (loss_identity_A + loss_identity_B) * 0.5

            loss_gan_AB = criterion_gan(D_B(fake_B), torch.ones_like(D_B(fake_B)))
            loss_gan_BA = criterion_gan(D_A(fake_A), torch.ones_like(D_A(fake_A)))
            loss_gan = (loss_gan_AB + loss_gan_BA) * 0.5

            loss_cycle_A = criterion_cycle(rec_A, real_A) * args.lambda_cycle
            loss_cycle_B = criterion_cycle(rec_B, real_B) * args.lambda_cycle
            loss_cycle = (loss_cycle_A + loss_cycle_B) * 0.5

            loss_G = loss_gan + loss_cycle + loss_identity
            loss_G.backward()
            optimizer_G.step()

            # ------------------ Discriminator A ------------------
            optimizer_D_A.zero_grad(set_to_none=True)
            pred_real_A = D_A(real_A)
            pred_fake_A = D_A(fake_A.detach())
            loss_D_A = 0.5 * (
                criterion_gan(pred_real_A, torch.ones_like(pred_real_A))
                + criterion_gan(pred_fake_A, torch.zeros_like(pred_fake_A))
            )
            loss_D_A.backward()
            optimizer_D_A.step()

            # ------------------ Discriminator B ------------------
            optimizer_D_B.zero_grad(set_to_none=True)
            pred_real_B = D_B(real_B)
            pred_fake_B = D_B(fake_B.detach())
            loss_D_B = 0.5 * (
                criterion_gan(pred_real_B, torch.ones_like(pred_real_B))
                + criterion_gan(pred_fake_B, torch.zeros_like(pred_fake_B))
            )
            loss_D_B.backward()
            optimizer_D_B.step()

            running["g"] += float(loss_G.item())
            running["d"] += float((loss_D_A.item() + loss_D_B.item()) * 0.5)
            running["cycle"] += float(loss_cycle.item())
            running["identity"] += float(loss_identity.item())

        scheduler_G.step()
        scheduler_D_A.step()
        scheduler_D_B.step()

        save_checkpoint(out_dir, "G_AB", G_AB)
        save_checkpoint(out_dir, "G_BA", G_BA)
        save_checkpoint(out_dir, "D_A", D_A)
        save_checkpoint(out_dir, "D_B", D_B)

        if epoch % args.sample_every == 0 or epoch == args.epochs or epoch == 1:
            with torch.no_grad():
                sample = next(iter(loader))
                real_A = sample["A"].to(device)
                real_B = sample["B"].to(device)
                fake_B = G_AB(real_A)
                rec_A = G_BA(fake_B)
                fake_A = G_BA(real_B)
                rec_B = G_AB(fake_A)
                grid = make_sample_grid(real_A[0], fake_B[0], rec_A[0], real_B[0], fake_A[0], rec_B[0])
                save_image(grid, os.path.join(sample_dir, f"epoch_{epoch:04d}.png"))

        elapsed = time.time() - start
        print(
            f"[CycleGAN] epoch {epoch:03d}/{args.epochs} | "
            f"G {running['g'] / max(1, steps):.4f} | "
            f"D {running['d'] / max(1, steps):.4f} | "
            f"cycle {running['cycle'] / max(1, steps):.4f} | "
            f"identity {running['identity'] / max(1, steps):.4f} | "
            f"{elapsed:.1f}s"
        )

    print("[CycleGAN] Training complete.")
    print(f"[CycleGAN] Checkpoints: {out_dir}")
    print("[CycleGAN] Copy this folder to model/gan/ in the Flask project, then run:")
    print(f"  python -m gan.translate --checkpoint {out_dir} --input leaf.jpg --output out.jpg")


if __name__ == "__main__":
    main()

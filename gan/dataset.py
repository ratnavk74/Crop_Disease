"""Dataset helpers for unpaired CycleGAN training.

Expected layout::

    <root>/
        trainA/   # healthy leaves
        trainB/   # diseased leaves
        testA/    # optional
        testB/    # optional

``A`` is the source domain (usually healthy) and ``B`` is the target domain
(usually diseased).  ``G_AB`` translates healthy -> diseased.
"""

import os
import random

from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms

from gan.utils import IMAGE_EXTENSIONS, is_image_file  # noqa: F401


def list_images(directory):
    if not os.path.isdir(directory):
        return []
    return [
        os.path.join(directory, name)
        for name in sorted(os.listdir(directory))
        if is_image_file(name)
    ]


class UnalignedDataset(Dataset):
    """Random unpaired samples from two image domains."""

    def __init__(self, root, phase="train", img_size=128, augment=True):
        self.dir_A = os.path.join(root, f"{phase}A")
        self.dir_B = os.path.join(root, f"{phase}B")
        self.files_A = list_images(self.dir_A)
        self.files_B = list_images(self.dir_B)

        if not self.files_A:
            raise FileNotFoundError(f"No images found in {self.dir_A}")
        if not self.files_B:
            raise FileNotFoundError(f"No images found in {self.dir_B}")

        if phase == "train" and augment:
            transform = [
                transforms.Resize((img_size, img_size), Image.BICUBIC),
                transforms.RandomHorizontalFlip(),
                transforms.ColorJitter(brightness=0.08, contrast=0.08, saturation=0.08),
            ]
        else:
            transform = [transforms.Resize((img_size, img_size), Image.BICUBIC)]

        transform += [
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        ]
        self.transform = transforms.Compose(transform)

    def __len__(self):
        return max(len(self.files_A), len(self.files_B))

    def __getitem__(self, index):
        image_A = Image.open(self.files_A[index % len(self.files_A)]).convert("RGB")
        image_B = Image.open(self.files_B[random.randint(0, len(self.files_B) - 1)]).convert("RGB")
        return {"A": self.transform(image_A), "B": self.transform(image_B)}


def make_sample_grid(tensor_a, fake_b, rec_a, tensor_b, fake_a, rec_b):
    """Return a single image grid: A, G(A), F(G(A)), B, G(B), F(G(B))."""
    from torchvision.utils import make_grid

    row = [tensor_a.detach().cpu(), fake_b.detach().cpu(), rec_a.detach().cpu()]
    row2 = [tensor_b.detach().cpu(), fake_a.detach().cpu(), rec_b.detach().cpu()]
    grid = make_grid(row + row2, nrow=3, normalize=True, value_range=(-1, 1))
    return grid

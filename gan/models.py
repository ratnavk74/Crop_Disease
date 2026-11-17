"""CycleGAN generator and discriminator networks.

These are compact versions of the original CycleGAN architecture, sized so a
small Colab/Kaggle GPU session can train them on leaf images in a reasonable
time.  The same definitions are used for training and Flask inference, so a
checkpoint saved here is directly loadable by ``utils.gan_translate``.
"""

import torch.nn as nn


class ResnetBlock(nn.Module):
    """Residual block with reflection padding (CycleGAN style)."""

    def __init__(self, dim):
        super().__init__()
        self.block = nn.Sequential(
            nn.ReflectionPad2d(1),
            nn.Conv2d(dim, dim, kernel_size=3, bias=False),
            nn.InstanceNorm2d(dim),
            nn.ReLU(inplace=True),
            nn.ReflectionPad2d(1),
            nn.Conv2d(dim, dim, kernel_size=3, bias=False),
            nn.InstanceNorm2d(dim),
        )

    def forward(self, x):
        return x + self.block(x)


class Generator(nn.Module):
    """ResNet generator: 3 input channels -> 3 output channels in [-1, 1]."""

    def __init__(self, base_channels=32, num_blocks=6):
        super().__init__()
        layers = [
            nn.ReflectionPad2d(3),
            nn.Conv2d(3, base_channels, kernel_size=7, bias=False),
            nn.InstanceNorm2d(base_channels),
            nn.ReLU(inplace=True),
        ]

        channels = base_channels
        for _ in range(2):
            out_channels = channels * 2
            layers += [
                nn.Conv2d(channels, out_channels, kernel_size=3, stride=2, padding=1, bias=False),
                nn.InstanceNorm2d(out_channels),
                nn.ReLU(inplace=True),
            ]
            channels = out_channels

        layers += [ResnetBlock(channels) for _ in range(num_blocks)]

        for _ in range(2):
            out_channels = channels // 2
            layers += [
                nn.ConvTranspose2d(
                    channels,
                    out_channels,
                    kernel_size=3,
                    stride=2,
                    padding=1,
                    output_padding=1,
                    bias=False,
                ),
                nn.InstanceNorm2d(out_channels),
                nn.ReLU(inplace=True),
            ]
            channels = out_channels

        layers += [
            nn.ReflectionPad2d(3),
            nn.Conv2d(channels, 3, kernel_size=7),
            nn.Tanh(),
        ]
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        return self.model(x)


class Discriminator(nn.Module):
    """PatchGAN discriminator used by CycleGAN."""

    def __init__(self, base_channels=32, n_layers=3):
        super().__init__()
        layers = [
            nn.Conv2d(3, base_channels, kernel_size=4, stride=2, padding=1),
            nn.LeakyReLU(0.2, inplace=True),
        ]

        channels = base_channels
        for _ in range(1, n_layers):
            out_channels = min(channels * 2, 512)
            layers += [
                nn.Conv2d(channels, out_channels, kernel_size=4, stride=2, padding=1, bias=False),
                nn.InstanceNorm2d(out_channels),
                nn.LeakyReLU(0.2, inplace=True),
            ]
            channels = out_channels

        layers += [
            nn.Conv2d(channels, min(channels * 2, 512), kernel_size=4, stride=1, padding=1, bias=False),
            nn.InstanceNorm2d(min(channels * 2, 512)),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(min(channels * 2, 512), 1, kernel_size=4, stride=1, padding=1),
        ]
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        return self.model(x)


def build_generator(base_channels=32, num_blocks=6):
    return Generator(base_channels=base_channels, num_blocks=num_blocks)


def build_discriminator(base_channels=32, n_layers=3):
    return Discriminator(base_channels=base_channels, n_layers=n_layers)


def weights_init(module):
    """Initialise convolutions the way the original CycleGAN does."""
    import torch.nn as nn

    classname = module.__class__.__name__
    if classname.find("Conv") != -1:
        nn.init.normal_(module.weight.data, 0.0, 0.02)
    elif classname.find("InstanceNorm") != -1:
        if module.weight is not None:
            nn.init.normal_(module.weight.data, 1.0, 0.02)
        if module.bias is not None:
            nn.init.constant_(module.bias.data, 0.0)

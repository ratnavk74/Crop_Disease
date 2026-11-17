"""CycleGAN package for CropShield AI.

The package stays import-safe without PyTorch: training/inference modules are
loaded lazily, while dataset preparation only needs Pillow.
"""

__all__ = [
    "Generator",
    "Discriminator",
    "build_generator",
    "build_discriminator",
]


def __getattr__(name):
    if name in __all__:
        from . import models

        return getattr(models, name)
    raise AttributeError(name)

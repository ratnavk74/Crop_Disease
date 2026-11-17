# CycleGAN checkpoints

Trained CycleGAN checkpoints live here, one folder per crop:

```
model/gan/
├── maize/
│   ├── G_AB.pth      # required: healthy -> diseased generator
│   ├── G_BA.pth
│   ├── D_A.pth
│   ├── D_B.pth
│   ├── config.json   # required: img_size, base_channels, num_blocks
│   └── samples/      # optional preview grid
└── wheat/
    └── ...
```

`G_AB.pth` and `config.json` are enough for the Flask "Generative AI view" card.

Train them with `notebooks/CropShield_CycleGAN_Training.ipynb` (Colab/Kaggle GPU)
or locally:

```powershell
python -m gan.prepare_dataset --source data/raw --output data/cyclegan --crop maize
python -m gan.train_cyclegan --dataroot data/cyclegan/maize --name maize --img-size 128 --epochs 50
```

Without checkpoints the app still works normally; the generative card is hidden.

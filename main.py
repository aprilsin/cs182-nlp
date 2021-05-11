import itertools
from argparse import Namespace

import pytorch_lightning as pl
import torch
from pytorch_lightning.callbacks import ModelCheckpoint

import data
import models

for use_bert, use_vader in itertools.product([True, False], repeat=2):
    print(f"{use_bert, use_vader=}")

    try:
        args = Namespace(
            batch_size=240,
            epochs=10,
            max_len=128,
            max_len_vader=128,
            use_bert=use_bert,
            use_cnn=True,
            use_vader=use_vader,
        )

        model = models.LanguageModel(args)
        datamodule = data.YelpDataModule(args)
        trainer = pl.Trainer(
            # TODO re-enable GPU
            # gpus=torch.cuda.device_count(),
            gpus=0,
            # overfit_batches=1,
            # track_grad_norm=2,
            weights_summary="full",
            progress_bar_refresh_rate=1,
            check_val_every_n_epoch=1,
            callbacks=[ModelCheckpoint(monitor="val_loss", every_n_train_steps=100)],
        )
        trainer.fit(model, datamodule=datamodule)
        trainer.validate(model, datamodule=datamodule)
    except:
        continue

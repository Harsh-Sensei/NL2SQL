import torch
import pytorch_lightning

import os

from torch import nn
from pytorch_lightning import LightningModule, Trainer, seed_everything
from torch.nn import functional as F
from torch.utils.data import DataLoader, random_split
from torchvision import transforms
from torchmetrics import Accuracy
from torchvision.datasets import MNIST
from pytorch_lightning.callbacks import ModelCheckpoint

seed_everything(73, workers=True)

PATH_DATASETS = os.environ.get("PATH_DATASETS")
AVAIL_GPUS = min(1, torch.cuda.device_count())
BATCH_SIZE = 64 if AVAIL_GPUS else 32
MODEL_PATH = os.environ.get("MODEL_PATH")
NUM_EPOCHS = 3

print(torch.__version__)
print(pytorch_lightning.__version__)
print("Number of GPUs: ", torch.cuda.device_count())


class LitMNIST(LightningModule):
    def __init__(self, data_dir=PATH_DATASETS, hidden_size=64, lr=1e-4) -> None:
        super().__init__()

        self.data_dir = data_dir
        self.hidden_size = hidden_size
        self.lr = lr

        self.num_classes = 10
        self.dims = (1, 28, 28)
        c, w ,h = self.dims
        self.transform = transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Normalize((0.1307), (0.3081))
            ]
        )

        self.model = nn.Sequential(
            nn.Flatten(),
            nn.Linear(c*w*h, self.hidden_size),
            nn.ReLU(),
            nn.Dropout(p=0.1),
            nn.Linear(hidden_size, self.hidden_size),
            nn.ReLU(),
            nn.Dropout(p=0.1),
            nn.Linear(hidden_size, self.num_classes)
        )

        self.accuracy = Accuracy()

    def forward(self, x):
        x = self.model(x)
        return F.log_softmax(x, dim=1)
    
    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.nll_loss(logits, y) 
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.nll_loss(logits, y)
        preds = torch.argmax(logits, dim=1)
        self.accuracy(preds, y)

        self.log("val_loss", loss, prog_bar=True)
        self.log("val_acc", self.accuracy, prog_bar=True)

        return loss
    
    def test_step(self, batch, batch_idx):
        return self.validation_step(batch, batch_idx)
    
    def prepare_data(self):
        MNIST(self.data_dir, train=True, download=True)
        MNIST(self.data_dir, train=False, download=True)
        return 
    
    def setup(self, stage=None):
        
        if stage=='fit' or stage is None:
            self.mnist_full = MNIST(self.data_dir, train=True, transform=self.transform)
            self.mnist_train, self.mnist_test = random_split(self.mnist_full, [55000, 5000])
        
        if stage=="Test" or stage is None:
            self.mnist_test = MNIST(self.data_dir, train=False, transform=self.transform)
    
    def train_dataloader(self):
        return DataLoader(self.mnist_train, batch_size=BATCH_SIZE)

    def test_dataloader(self):
        return DataLoader(self.mnist_test, batch_size=BATCH_SIZE)

    def val_dataloader(self):
        return DataLoader(self.mnist_test, batch_size=BATCH_SIZE)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.lr)

if __name__=="__main__":
    checkpoint_callback = ModelCheckpoint(
        monitor="val_loss",
        dirpath=MODEL_PATH,
        filename="sample-mnist-{epoch:02d}-{val_loss:.2f}",
        save_top_k=2,
        mode="min",
        every_n_epochs=1
    )

    model = LitMNIST()
    trainer = Trainer(
        gpus=AVAIL_GPUS,
        max_epochs=NUM_EPOCHS,
        progress_bar_refresh_rate=20,
        callbacks=[checkpoint_callback]
    )

    trainer.fit(model)
    trainer.test(model)


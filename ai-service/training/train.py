import torch
from torch.utils.data import DataLoader
from transformers import AutoModel
from torch import nn

from dataset import EmotionDataset


MODEL_NAME = "dbmdz/bert-base-turkish-cased"


# Dataset
dataset = EmotionDataset("../data/emotions.csv")

loader = DataLoader(
    dataset,
    batch_size=2,
    shuffle=True
)


# BERT
bert = AutoModel.from_pretrained(MODEL_NAME)


# Duygu sınıflandırıcı
class EmotionClassifier(nn.Module):

    def __init__(self):
        super().__init__()

        self.bert = bert

        self.classifier = nn.Linear(
            768,
            10
        )


    def forward(self, input_ids, attention_mask):

        output = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        pooled = output.last_hidden_state[:,0]

        logits = self.classifier(pooled)

        return logits



model = EmotionClassifier()


# Loss
criterion = nn.BCEWithLogitsLoss()


# Optimizer
optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=1e-5
)


# Eğitim
epochs = 10


for epoch in range(epochs):

    total_loss = 0

    for batch in loader:

        optimizer.zero_grad()


        outputs = model(
            batch["input_ids"],
            batch["attention_mask"]
        )


        loss = criterion(
            outputs,
            batch["labels"]
        )


        loss.backward()

        optimizer.step()


        total_loss += loss.item()


    print(
        f"Epoch {epoch+1} Loss:",
        total_loss
    )


# Kaydet
torch.save(
    model.state_dict(),
    "../model/emotion_model.pt"
)


print("✅ Model kaydedildi")
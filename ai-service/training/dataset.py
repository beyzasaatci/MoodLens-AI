import torch
import pandas as pd
from torch.utils.data import Dataset
from transformers import AutoTokenizer


MODEL_NAME = "dbmdz/bert-base-turkish-cased"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


class EmotionDataset(Dataset):

    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)

        self.texts = self.data["text"].tolist()

        self.labels = self.data[
            [
                "sadness",
                "anxiety",
                "loneliness",
                "anger",
                "happiness",
                "stress",
                "fear",
                "disappointment",
                "calm",
                "confidence"
            ]
        ].values


    def __len__(self):
        return len(self.texts)


    def __getitem__(self, index):

        text = self.texts[index]

        label = self.labels[index]

        encoded = tokenizer(
            text,
            padding="max_length",
            truncation=True,
            max_length=128,
            return_tensors="pt"
        )

        return {
            "input_ids": encoded["input_ids"].squeeze(),
            "attention_mask": encoded["attention_mask"].squeeze(),
            "labels": torch.tensor(label, dtype=torch.float)  
        }
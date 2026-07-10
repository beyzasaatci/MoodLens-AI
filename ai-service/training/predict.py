import torch
from torch import nn
from transformers import AutoTokenizer, AutoModel


MODEL_NAME = "dbmdz/bert-base-turkish-cased"


tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


bert = AutoModel.from_pretrained(MODEL_NAME)


class EmotionClassifier(nn.Module):

    def __init__(self):
        super().__init__()

        self.bert = bert

        self.classifier = nn.Linear(
            768,
            5
        )


    def forward(self, input_ids, attention_mask):

        output = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        pooled = output.last_hidden_state[:,0]

        return self.classifier(pooled)



model = EmotionClassifier()


model.load_state_dict(
    torch.load("../model/emotion_model.pt")
)


model.eval()


text = "Bugün kendimi çok yalnız ve üzgün hissediyorum."


inputs = tokenizer(
    text,
    return_tensors="pt",
    padding=True,
    truncation=True
)


with torch.no_grad():

    outputs = model(
        inputs["input_ids"],
        inputs["attention_mask"]
    )


scores = torch.sigmoid(outputs)


emotions = [
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


for emotion, score in zip(emotions, scores[0]):

    print(
        emotion,
        round(score.item(), 2)
    )
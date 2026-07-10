from ollama import chat
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel

import torch
from torch import nn
from transformers import AutoTokenizer, AutoModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme için
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MODEL_NAME = "dbmdz/bert-base-turkish-cased"


tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

bert = AutoModel.from_pretrained(MODEL_NAME)



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

        pooled = output.last_hidden_state[:, 0]

        return self.classifier(pooled)



model = EmotionClassifier()


model.load_state_dict(
    torch.load(
        "model/emotion_model.pt",
        map_location="cpu"
    )
)


model.eval()



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



class TextRequest(BaseModel):
    text: str



@app.get("/")
def home():

    return {
        "message": "AI Mood Companion API is running"
    }



@app.post("/predict")
def predict(request: TextRequest):

    inputs = tokenizer(
        request.text,
        return_tensors="pt",
        padding=True,
        truncation=True
    )


    with torch.no_grad():

        outputs = model(
            inputs["input_ids"],
            inputs["attention_mask"]
        )


    scores = torch.sigmoid(outputs)[0]


    emotion_scores = {}


    for emotion, score in zip(emotions, scores):

        emotion_scores[emotion] = round(
            score.item(),
            3
        )



    main_emotion = max(
        emotion_scores,
        key=emotion_scores.get
    )
    print("QWEN BASLIYOR")
    ai = chat(
        model="qwen3:1.7b",
        messages=[
            {
                "role": "system",
                "content": """
Sen Türkçe konuşan empatik bir AI duygu destek asistanısın.

Kurallar:
Sen MoodLens AI'sın.

Türkçe konuş.
Doğal ve arkadaşça cevap ver.
2-3 kısa cümle yaz.
Yargılama.
Tanı koyma.
Tıbbi öneri verme.
"""
            },
            {
                "role": "user",
                "content": f"""
Kullanıcının mesajı:
{request.text}

Algılanan ana duygu:
{main_emotion}
"""
            }
        ]
    )
    confidence = emotion_scores[main_emotion]

    print("QWEN BITTI") 

    sorted_emotions = sorted(
        emotion_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )


    top_emotions = []


    for emotion, score in sorted_emotions[:3]:

        top_emotions.append(
            {
                "name": emotion,
                "score": round(score * 100, 1)
            }
        )



    insights = {

        "sadness":
        "Yazında üzgünlük ifadeleri öne çıkıyor.",

        "anxiety":
        "Yazında kaygı ve endişe ifadeleri öne çıkıyor.",

        "loneliness":
        "Yazında yalnızlık ve bağlantı ihtiyacı hissi öne çıkıyor.",

        "anger":
        "Yazında öfke veya tepki ifadeleri öne çıkıyor.",

        "happiness":
        "Yazında olumlu ve mutlu ifadeler öne çıkıyor.",

        "stress":
        "Yazında yoğun baskı veya stres belirtileri öne çıkıyor.",

        "fear":
        "Yazında korku veya endişe ifadeleri öne çıkıyor.",

        "disappointment":
        "Yazında beklenti karşılanmaması veya hayal kırıklığı ifadeleri öne çıkıyor.",

        "calm":
        "Yazında sakinlik ve huzur ifadeleri öne çıkıyor.",

        "confidence":
        "Yazında kendine güven ve güçlü hissetme ifadeleri öne çıkıyor."

    }



    return {

        "text": request.text,

        "main_emotion": main_emotion,

        "confidence": round(
            confidence,
            3
        ),

        "top_emotions": top_emotions,

        "emotions": emotion_scores,

        "insight": insights[main_emotion],

        "ai_response": ai.message.content

    }


# Yeni sohbet endpoint'i
@app.post("/chat")
def chat_with_ai(request: TextRequest):

    ai = chat(
        model="qwen3:1.7b",
        messages=[
            {
                "role": "system",
                "content": """
Sen MoodLens AI adlı doğal konuşan bir duygu destek asistanısın.

Kurallar:
- Her zaman Türkçe cevap ver.
- Kullanıcıyla doğal ve sıcak konuş.
- Robotik cevap verme.
- Kısa ama anlamlı cevaplar ver.
- Kullanıcıyı yargılama.
- Tanı koyma.
- Tıbbi öneri verme.
- Sohbet ediyormuş gibi cevap ver.
"""
            },
            {
                "role": "user",
                "content": request.text
            }
        ]
    )

    return {
        "response": ai.message.content
    }
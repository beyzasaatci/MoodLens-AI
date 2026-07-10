from transformers import AutoTokenizer, AutoModel

MODEL_NAME = "dbmdz/bert-base-turkish-cased"

print("Model indiriliyor...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModel.from_pretrained(MODEL_NAME)

print("✅ Model başarıyla yüklendi!")

text = "Bugün kendimi çok yalnız hissediyorum."

inputs = tokenizer(
    text,
    return_tensors="pt"
)

outputs = model(**inputs)

print(outputs.last_hidden_state.shape)
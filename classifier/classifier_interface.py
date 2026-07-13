
"""
SecurePrompt Classifier — Interface Module
Load this and call classify_prompt(text) to get a classification.
 
Usage (in Person B's notebook):
    from classifier_interface import classify_prompt
    result = classify_prompt("some text here")
    # result = {"label": "safe"|"suspicious", "confidence": 0.0-1.0}
"""
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
 
MODEL_PATH = "/content/drive/MyDrive/secureprompt_model"  # shared Drive folder — make sure it's shared with your teammate's Google account
 
_model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
_tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
_model.eval()
 
_device = "cuda" if torch.cuda.is_available() else "cpu"
_model.to(_device)
 
 
def classify_prompt(text: str) -> dict:
    inputs = _tokenizer(text, truncation=True, padding="max_length",
                         max_length=128, return_tensors="pt").to(_device)
    with torch.no_grad():
        outputs = _model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1)[0]
    predicted_class = torch.argmax(probs).item()
    confidence = probs[predicted_class].item()
    label = "safe" if predicted_class == 0 else "suspicious"
    return {"label": label, "confidence": round(confidence, 4)}

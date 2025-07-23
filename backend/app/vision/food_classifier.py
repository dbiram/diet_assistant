import torch
from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from PIL import Image


device = "cuda" if torch.cuda.is_available() else "cpu"

# Load Food-101 fine-tuned model
model_id = "nateraw/vit-base-food101"
extractor = AutoFeatureExtractor.from_pretrained(model_id)
model = AutoModelForImageClassification.from_pretrained(model_id).to(device)
model.eval()

# Load Food-101 class labels
id2label = model.config.id2label

def classify_food(image_file) -> str:
    image = Image.open(image_file).convert("RGB")
    inputs = extractor(images=image, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        predicted_idx = outputs.logits.argmax(-1).item()

    return id2label[predicted_idx].replace("_", " ")

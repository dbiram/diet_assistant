import torch
from torchvision import models
import json
from app.vision.utils import load_and_preprocess_image
import requests

# Load model (MobileNetV2, pretrained on ImageNet)
device = "cuda" if torch.cuda.is_available() else "cpu"
model = models.mobilenet_v2(pretrained=True).to(device)
model.eval()

# Load class labels from ImageNet
response = requests.get("https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt")
imagenet_labels = response.text.strip().splitlines()

def classify_food(image_file) -> str:
    input_tensor = load_and_preprocess_image(image_file).to(device)
    with torch.no_grad():
        outputs = model(input_tensor)
    _, predicted_idx = torch.max(outputs, 1)
    return imagenet_labels[predicted_idx.item()]

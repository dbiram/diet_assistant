from torchvision import transforms
from PIL import Image

# Define image transforms compatible with MobileNetV2
image_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],  # Imagenet mean
        std=[0.229, 0.224, 0.225]    # Imagenet std
    )
])

def load_and_preprocess_image(image_file):
    image = Image.open(image_file).convert("RGB")
    return image_transforms(image).unsqueeze(0)  # Add batch dimension

import json
from pathlib import Path

# Load nutrition table once
nutrition_path = Path(__file__).resolve().parents[3] / "data" / "nutrition_lookup.json"
with open(nutrition_path, "r") as f:
    NUTRITION_TABLE = json.load(f)

def get_nutrition(label: str):
    label_lower = label.lower()
    return NUTRITION_TABLE.get(label_lower, {
        "calories": "unknown",
        "protein": "unknown",
        "fat": "unknown"
    })

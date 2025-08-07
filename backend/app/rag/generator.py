import os
import requests


MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL = "mistral-small-latest"


def generate_text(prompt: str, max_length=512):
    mistral_api_key = os.environ.get("MISTRAL_API_KEY", None)
    if not mistral_api_key:
        raise EnvironmentError("Missing MISTRAL_API_KEY environment variable.")
    headers = {
        "Authorization": f"Bearer {mistral_api_key}"
    }

    payload = {
        "model": MISTRAL_MODEL,
        "messages": [
            {"role": "system", "content": (
                "You are a concise and expert diet assistant. "
                "Always provide direct answers without repeating the user’s question, "
                "without mentioning the user's profile explicitly. "
                "Do not say 'based on the information provided' or similar phrases. "
                "Avoid unnecessary introductions or summaries. "
                "Keep your answer helpful but brief (1–3 sentences)."
            )},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": max_length
    }

    response = requests.post(MISTRAL_API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"Mistral API error {response.status_code}: {response.text}")

    data = response.json()
    return data["choices"][0]["message"]["content"]
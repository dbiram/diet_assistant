import os
import requests
import time
from sqlalchemy.orm import Session
from app.database import get_db, LLMLog

from app.obs.metrics import (
    llm_requests_total, llm_errors_total,
    llm_tokens_in_total, llm_tokens_out_total,
    llm_latency_seconds
)

MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL = "mistral-small-latest"


def generate_text(prompt: str, user_id: int = None, db: Session = None, max_length=512):
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
    llm_requests_total.inc()
    start_time = time.time()
    try:
        response = requests.post(MISTRAL_API_URL, headers=headers, json=payload)
        latency = time.time() - start_time
        llm_latency_seconds.observe(latency)

        if response.status_code != 200:
            status = "error"
            tokens_in = tokens_out = 0
            answer = f"Error: {response.text}"
            llm_errors_total.inc()
        else:
            data = response.json()
            if "choices" not in data or len(data["choices"]) == 0:
                raise ValueError("Invalid response format from Mistral API.")
            answer = data["choices"][0]["message"]["content"]
            tokens_in = data.get("usage", {}).get("prompt_tokens", 0)
            tokens_out = data.get("usage", {}).get("completion_tokens", 0)
            status = "success"
            llm_tokens_in_total.inc(tokens_in)
            llm_tokens_out_total.inc(tokens_out)
        # Log to DB
        if db:
            llm_log = LLMLog(
                user_id=user_id,
                prompt=prompt,
                response=answer,
                tokens_in=tokens_in,
                tokens_out=tokens_out,
                latency_seconds=latency,
                model=MISTRAL_MODEL,
                status=status
            )
            db.add(llm_log)
            db.commit()
            db.refresh(llm_log)
        return answer
    except Exception as e:
        llm_errors_total.inc()
        if db:
            llm_log = LLMLog(
                user_id=user_id,
                prompt=prompt,
                response=str(e),
                tokens_in=0,
                tokens_out=0,
                latency_seconds=time.time() - start_time,
                model=MISTRAL_MODEL,
                status="error"
            )
            db.add(llm_log)
            db.commit()
            db.refresh(llm_log)
        raise e 
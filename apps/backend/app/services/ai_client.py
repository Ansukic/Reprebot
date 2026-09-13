import httpx
from fastapi import HTTPException

from app.core.config import get_settings


def chat(
    messages: list[dict], model: str | None = None, temperature: float = 0.2
) -> str:
    s = get_settings()
    body = {
        "model": model or s.groq_chat_model,
        "messages": messages,
        "temperature": temperature,
    }
    try:
        r = httpx.post(
            f"{s.groq_base_url}/chat/completions",
            headers={"Authorization": f"Bearer {s.groq_api_key}"},
            json=body,
            timeout=120,
        )
    except httpx.HTTPError as e:
        raise HTTPException(502, f"no hubo conexión con groq: {e}") from e
    if r.status_code != 200:
        raise HTTPException(502, f"groq respondió {r.status_code}: {r.text[:300]}")
    return r.json()["choices"][0]["message"]["content"]

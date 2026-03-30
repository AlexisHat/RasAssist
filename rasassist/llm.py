import os

from openai import OpenAI

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# System-Prompt: kurze Antworten, da Output direkt zu TTS geht
_SYSTEM_PROMPT = (
    "Du bist ein hilfreicher Sprachassistent. "
    "Antworte immer auf Deutsch, präzise und in ein bis zwei Sätzen. "
    "Vermeide Aufzählungszeichen und Markdown-Formatierung."
)


class LLMClient:
    """Sendet Text-Anfragen über OpenRouter und gibt die Antwort zurück."""

    def __init__(self, model: str = "meta-llama/llama-3.3-70b-instruct:free"):
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY nicht gesetzt. "
                "Bitte eine .env Datei anlegen (siehe .env.example)."
            )
        self._client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)
        self._model = model

    def ask(self, prompt: str) -> str:
        """Schickt einen Prompt und gibt die Text-Antwort zurück."""
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content.strip()

# backend/ai/client.py
from groq import Groq

from backend.config import GROQ_API_KEY

# One shared Groq client for the whole backend (teacher, detector, translator,
# lesson generator). The timeout stops a stuck request from hanging forever.
client = Groq(api_key=GROQ_API_KEY, timeout=90.0, max_retries=2) if GROQ_API_KEY else None


def require_client():
    if client is None:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to your .env file and restart the server."
        )
    return client


if __name__ == "__main__":
    require_client()
    print("Groq client created successfully")
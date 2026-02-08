import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_API_KEY)

logging.basicConfig(level=logging.INFO)

MODEL_NAME = "models/gemini-2.5-flash-lite"


def generate_gemini_explanation(reference_answer: str, student_answer: str) -> str:
    """
    Generates a structured comparative explanation using Gemini.
    Output format is STRICTLY controlled for safe parsing.
    """

    prompt = f"""
You are an academic evaluator.

Compare the STUDENT ANSWER with the TEACHER ANSWER.
Respond STRICTLY in the format below.
Do NOT add extra text or headings.

1. What parts of the student answer are correct:
- Bullet points only.

2. What important points are missing or incorrect:
- Bullet points only.

3. How the answer can be improved:
- Clear, actionable suggestions.

TEACHER ANSWER:
{reference_answer}

STUDENT ANSWER:
{student_answer}
"""

    try:
        response = genai.generate(
            model=MODEL_NAME,
            prompt=prompt
        )

        # ✅ Robust text extraction
        text = None

        if hasattr(response, "candidates") and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, "content") and hasattr(candidate.content, "parts"):
                text = candidate.content.parts[0].text

        if not text and hasattr(response, "text"):
            text = response.text

        if not text:
            text = str(response)

        return text.strip()

    except ResourceExhausted:
        return (
            "1. What parts of the student answer are correct:\n"
            "- AI explanation unavailable due to rate limits.\n\n"
            "2. What important points are missing or incorrect:\n"
            "- AI explanation unavailable due to rate limits.\n\n"
            "3. How the answer can be improved:\n"
            "- Please refer to the rule-based explanation."
        )

    except Exception as e:
        logging.error(f"Gemini error: {e}")
        return (
            "1. What parts of the student answer are correct:\n"
            "- AI explanation unavailable.\n\n"
            "2. What important points are missing or incorrect:\n"
            "- AI explanation unavailable.\n\n"
            "3. How the answer can be improved:\n"
            "- Please refer to the rule-based explanation."
        )

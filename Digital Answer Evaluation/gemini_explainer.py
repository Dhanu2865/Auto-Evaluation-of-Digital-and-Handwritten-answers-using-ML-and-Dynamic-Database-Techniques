import os
import time
import google.generativeai as genai
from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("models/gemini-2.5-flash")


def generate_gemini_explanation(reference_answer: str, student_answer: str) -> str:
    """
    Generates comparative explanation using Gemini.
    Falls back safely if quota is exceeded.
    """

    prompt = f"""
You are an academic evaluator.

Correct Answer:
{reference_answer}

Student Answer:
{student_answer}

Explain:
1. What parts of the student answer are correct
2. What important points are missing or incorrect
3. How the answer can be improved

Keep the explanation concise and educational.
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()

    except ResourceExhausted:
        return (
            "AI explanation temporarily unavailable due to API rate limits. "
            "Rule-based explanation has been provided."
        )

    except Exception:
        return (
            "AI explanation could not be generated at this time. "
            "Rule-based explanation has been provided."
        )
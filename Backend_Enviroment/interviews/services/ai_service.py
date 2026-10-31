import json
import re

from django.conf import settings
from google import genai
from google.genai import types

QUESTION_MODEL = "gemini-2.5-flash"
EVALUATION_MODEL = "gemini-2.5-flash"

# ponytail: thinking off - it dominates latency here and these prompts don't
# need it. Raise the budget if question/feedback quality drops.
NO_THINKING = types.GenerateContentConfig(
    thinking_config=types.ThinkingConfig(thinking_budget=0)
)

_client = None


def get_client():
    """Build the Gemini client on first use, not at import time."""
    global _client
    if _client is None:
        if not settings.GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY is not set")
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


def generate_interview_questions(role, difficulty, count=5):
    prompt = f"""
    You are a senior technical interviewer.

    Generate {count} {difficulty} interview questions for a {role}.
    Questions should test real-world understanding.
    Return each question on a new line.
    """

    response = get_client().models.generate_content(
        model=QUESTION_MODEL,
        contents=prompt,
        config=NO_THINKING,
    )

    text = response.text or ""

    questions = [
        q.strip("-•1234567890. ").strip()
        for q in text.split("\n")
        if q.strip()
    ]

    return questions[:count]


def parse_evaluation(text):
    """Pull {"score", "feedback"} out of a model reply.

    The model wraps JSON in markdown fences and sometimes adds prose, so
    strip the fences and isolate the first object before decoding.
    """
    text = re.sub(r"^```(?:json)?\s*", "", text or "", flags=re.MULTILINE)
    text = re.sub(r"\s*```$", "", text, flags=re.MULTILINE)

    json_match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not json_match:
        return {"score": None, "feedback": None}

    try:
        data = json.loads(json_match.group(0))
    except json.JSONDecodeError:
        return {"score": None, "feedback": None}

    score = data.get("score")
    try:
        score = None if score is None else max(0.0, min(10.0, float(score)))
    except (TypeError, ValueError):
        score = None

    return {"score": score, "feedback": data.get("feedback")}


def evaluate_answer(question_text, answer_text):
    prompt = f"""
    Evaluate this interview answer.

    Question: {question_text}
    Answer: {answer_text}

    Return JSON:
    {{
      "score": <number between 0-10>,
      "feedback": "<short feedback>"
    }}
    """

    response = get_client().models.generate_content(
        model=EVALUATION_MODEL,
        contents=prompt,
        config=NO_THINKING,
    )
    return parse_evaluation(response.text or "")

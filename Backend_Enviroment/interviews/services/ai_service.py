from django.conf import settings
from google import genai

# Create Gemini client
client = genai.Client()


def generate_interview_questions(role, difficulty, count=5):
    prompt = f"""
    You are a senior technical interviewer.

    Generate {count} {difficulty} interview questions for a {role}.
    Questions should test real-world understanding.
    Return each question on a new line.
    """

    response = client.models.generate_content(
        model= "gemini-3-flash-preview",
        contents=prompt
    )

    text = response.text or ""

    questions = [
        q.strip("-•1234567890. ").strip()
        for q in text.split("\n")
        if q.strip()
    ]

    return questions[:count]


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

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )
    text = response.text or ""
    print("RAW GEMINI RESPONSE:", text)

    # strip markdown fences that some AI responses include
    # e.g. ```json {...}```
    import re, json
    # remove starting ```json or ```
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.MULTILINE)
    # remove trailing ```
    text = re.sub(r"\s*```$", "", text, flags=re.MULTILINE)

    # try to isolate JSON object from any surrounding explanation
    json_match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if json_match:
        text = json_match.group(0)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # fallback: log and return a default structure so callers can handle it
        print("Failed to decode AI evaluation JSON, returning empty result")
        return {"score": None, "feedback": None}


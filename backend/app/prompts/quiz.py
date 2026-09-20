def quiz_prompt(
    topic: str,
    difficulty: int = 1,
    qtype: str = "multiple_choice",
) -> str:
    return f"""
Create exactly ONE educational quiz question.

Topic: {topic}
Difficulty: {difficulty}/5
Question type: {qtype}

Return ONLY valid JSON with this structure:

{{
  "question": "the question",
  "qtype": "{qtype}",
  "options": ["option A", "option B", "option C", "option D"],
  "correct_answer": "the exact correct option",
  "explanation": "short explanation of why it is correct",
  "difficulty": {difficulty}
}}

Rules:
- Test understanding, not random trivia.
- Make exactly one answer correct.
- Keep the question appropriate for the requested difficulty.
- Do not reveal the answer in the question.
- Return valid JSON only.
""".strip()
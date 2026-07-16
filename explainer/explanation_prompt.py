
PROMPT_TEMPLATE = """You are a security analyst explaining why a text input was flagged by an automated classifier.

Input text: "{original_text}"
Classifier verdict: {label} (confidence: {confidence})

Do not question or override the verdict — your only job is to explain it.

Respond in EXACTLY this structure, nothing else:
Key phrase: <the specific word or phrase from the input that most likely drove this verdict, quoted exactly>
Reason: <1-2 sentences explaining why that phrase indicates {label}, specific to this input>

Rules:
- The "Key phrase" must be copied exactly from the input text, not paraphrased.
- If verdict is "safe", Key phrase can be "none" and Reason should explain why the text is benign despite any surface similarity to attack patterns.
- Do not mention the confidence score.
- Do not write a generic explanation that could apply to unrelated flagged texts."""


PROMPT_TEMPLATE = """You are a security analyst explaining why a text input was flagged by an automated classifier.

Input text: "{original_text}"
Classifier verdict: {label} (confidence: {confidence})

Do not question or override the verdict — your job is only to explain it.

In 2-3 sentences, explain in plain language:
1. What specific phrase(s) from the input text likely triggered this verdict — quote them directly.
2. Why that phrase is associated with prompt injection / jailbreak risk (if suspicious), or why the text appears benign despite surface similarity to attacks (if safe).

Do not repeat the confidence score in your explanation. Be concrete and specific to this input — do not write a generic explanation that could apply to any flagged text."""

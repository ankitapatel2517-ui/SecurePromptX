
from groq import Groq
from explanation_prompt import PROMPT_TEMPLATE
import os

client = Groq(api_key=os.environ["GROQ_API_KEY"])

def explain(original_text, classifier_output):
    prompt = PROMPT_TEMPLATE.format(
        original_text=original_text,
        label=classifier_output["label"],
        confidence=classifier_output["confidence"]
    )
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    return response.choices[0].message.content

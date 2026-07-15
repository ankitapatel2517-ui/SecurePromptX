
from google import genai
from explanation_prompt import PROMPT_TEMPLATE
import os

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def explain(original_text, classifier_output):
    prompt = PROMPT_TEMPLATE.format(
        original_text=original_text,
        label=classifier_output["label"],
        confidence=classifier_output["confidence"]
    )
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )
    return response.text

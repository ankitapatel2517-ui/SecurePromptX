
import gradio as gr
import sys

sys.path.append("/content/SecurePromptX/classifier")
from classifier_interface import classify_prompt
from explain import explain


def analyze(prompt):
    """
    Runs the classifier + explanation layer and returns:
    - Prediction
    - Confidence
    - Real explanation
    """
    if not prompt or not prompt.strip():
        return "—", "—", "Please enter a prompt."

    result = classify_prompt(prompt)
    label = result["label"]
    confidence = result["confidence"]

    if label.lower() == "safe":
        prediction = "🟢 SAFE"
    else:
        prediction = "🔴 SUSPICIOUS"

    confidence_text = f"{confidence*100:.2f}%"

    try:
        explanation = explain(prompt, result)
    except Exception as e:
        explanation = f"Explanation generation failed: {str(e)[:200]}"

    return prediction, confidence_text, explanation


with gr.Blocks(title="SecurePrompt") as demo:

    gr.Markdown(
        """
        # 🔐 SecurePrompt

        ### Prompt Injection Detection System
        Enter any prompt below and the classifier will determine
        whether it is **SAFE** or **SUSPICIOUS**, with an explanation.
        """
    )

    prompt_input = gr.Textbox(
        label="Enter Prompt",
        placeholder="Type your prompt here...",
        lines=6,
    )

    analyze_button = gr.Button("Analyze", variant="primary")

    with gr.Row():
        prediction_output = gr.Textbox(label="Prediction", interactive=False)
        confidence_output = gr.Textbox(label="Confidence", interactive=False)

    explanation_output = gr.Textbox(
        label="Explanation",
        lines=8,
        interactive=False
    )

    analyze_button.click(
        fn=analyze,
        inputs=prompt_input,
        outputs=[prediction_output, confidence_output, explanation_output]
    )

demo.launch(share=True)

# Classifier Module (Person A)
 
## What this is
A fine-tuned DistilBERT classifier for jailbreak/prompt-injection detection.
Test set performance: see model_comparison.csv in this folder.
 
## How to use it (for Person B / integration)
1. Make sure the model folder at Google Drive path `secureprompt_model/` is
   shared with your account (Person A needs to share the Drive folder, or
   you both work in a shared Drive).
2. In your Colab notebook: `from classifier_interface import classify_prompt`
3. Call it: `result = classify_prompt("some text")`
4. You get back: `{"label": "safe"|"suspicious", "confidence": 0.0-1.0}`
 
## Files in this folder
- `classifier_interface.py` — the function you actually import and call
- `baseline_results.json`, `distilbert_results.json` — raw eval metrics
- `model_comparison.csv` — baseline vs DistilBERT comparison table
- `distilbert_confusion_matrix.png` — confusion matrix on test set

# SecurePromptX

A pre-LLM safety filter that detects jailbreak and prompt-injection attempts before they reach an LLM, and explains *why* a given input was flagged in plain language.

Built as a 2-person project: a fine-tuned classifier (Track A) paired with an LLM-generated natural-language explanation layer (Track B).

## What it does

Given any text input, SecurePrompt returns:
- A verdict: **safe** or **suspicious**
- A confidence score
- A natural-language explanation of why, quoting the specific phrase that likely drove the verdict

## Architecture

```
Input text
    │
    ▼
[Classifier: fine-tuned DistilBERT]  →  {label, confidence}
    │
    ▼
[Explanation layer: Groq/Llama-3.3-70B]  →  natural-language reasoning
    │
    ▼
Gradio demo UI
```
## Repo structure

secureprompt/
├── classifier/          Track A — dataset, baseline, DistilBERT fine-tuning, evaluation
│   ├── classifier_interface.py     <- the function other code imports
│   ├── baseline_results.json
│   ├── distilbert_results.json
│   ├── model_comparison.csv
│   ├── distilbert_confusion_matrix.png
│   ├── generalization_results.csv  <- cross-dataset testing
│   ├── error_analysis.json
│   ├── adversarial_evasion_results.csv
│   ├── v3_status.json              <- documents a rejected model iteration (see below)
│   └── README.md
├── explainer/            Track B — explanation prompt, OOD test set, evaluation
│   ├── explain.py
│   ├── explanation_prompt.py
|   |--- edge_case_results.json
│   ├── ood_test_set.csv
│   ├── ood_results.csv
│   └── README.md
├── demo/                 Combined pipeline
│   ├── app.py             <- Gradio demo, both tracks wired together
│   └── edge_case_results.csv  <- joint testing
└── README.md              <- this file

## Results summary

| Model | Test | Accuracy | F1 |
|---|---|---|---|
| TF-IDF + Logistic Regression | In-distribution | see classifier/baseline_results.json | |
| DistilBERT (v1, reported model) | In-distribution (S-Labs test set) | 96.5% | 96.4% |
| DistilBERT (v1) | External: deepset/prompt-injections | 81.0% | 79.3% |
| DistilBERT (v1) | External: jackhhao/jailbreak-classification | 66.4% | 75.6% |
| Explanation layer + classifier (combined) | Hand-written OOD set (16 examples) | 75% | — |

**Reported/deployed model: v1.** A retraining experiment (v3) attempted to fix an over-sensitivity to unusual-but-benign text (numbers, punctuation) but was found to cause a serious regression in non-English attack detection, and was rejected — see `classifier/v3_status.json` and the paper's Discussion section for full details.

## Key findings

1. **In-distribution accuracy (96.5%) does not hold up cross-dataset** (drops to 66-81% on external benchmarks) — consistent with recent literature on evaluation-shortcut concerns.
2. **Two independent evaluation methods** (automated cross-dataset testing, and a teammate-authored hand-written OOD set) **converged on the same failure mechanisms**: over-sensitivity to persona-assignment phrasing ("You are X...", "Pretend to be...") and to common trigger words ("ignore", "disregard") regardless of actual intent.
3. **The classifier is robust to some obfuscation** (leetspeak character substitution: 0/40 evaded) but two tested attack types (zero-width space, alternating case) were found to be invalidated by the tokenizer's own normalization — an important methodological catch, not a real robustness claim.
4. **A targeted fix for OOD-noise false positives (v3) worked for 6/7 cases but caused a serious non-English attack detection regression** (4/5 real attacks in Spanish/Japanese/Hindi misclassified as safe) — demonstrating that shortcut-driven errors are not reliably fixable through small-scale data augmentation alone.

## How to run the demo

1. Clone this repo
2. Get the trained model: shared via Google Drive (`secureprompt_model` folder) — not included in this repo due to size (~268MB)
3. Get a Groq API key from console.groq.com (free) and set `GROQ_API_KEY`
4. Run `demo/app.py` in a Colab notebook with a GPU runtime
5. `demo.launch(share=True)` will print a public link

## Team

- **Ankita Patel(Classifier Track):** dataset, baseline model, DistilBERT fine-tuning, evaluation, cross-dataset generalization, adversarial testing, error analysis
- **Pooja (Explanation & Integration Track):** explanation prompt design, out-of-distribution test set, Gradio demo, integration

## Status

Project complete as of July 20, 2026. Research paper in progress, due July 31, 2026.


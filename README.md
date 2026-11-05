# Meta x Data Club Spring 2026 Semester Project

We were given an anonymous social media dataset and trained a model, **WhispBERT**, to classify posts into five categories: **Self-Harm, Depression, Aggression, Anxiety, and Sexually suggestive**. We then built a quick frontend that mimics a social media feed: type a post, and the app shows how the model classifies it and how risky it looks.

## What's in this repository

- `app.py`, `ui.py`: the Streamlit frontend (mock social media feed)
- `model.py`, `inference.py`, `threat_rules.py`, `config.py`: model loading, risk scoring, and escalation rules
- `WhispBERT/`: the trained model weights and tokenizer (Git LFS)
- `MetaSetFit.ipynb`: the data labeling notebook (SetFit)
- `cleaned_mentalbert_multilabel_pipeline.ipynb`: the WhispBERT training notebook

## Tech stack

- **Model:** [MentalBERT](https://huggingface.co/mental/mental-bert-base-uncased) fine-tuned for multi-label classification, via Hugging Face Transformers and PyTorch
- **Labeling:** SetFit with `sentence-transformers/paraphrase-mpnet-base-v2`
- **Frontend:** Streamlit
- **Training:** Jupyter notebooks (Google Colab)
- **Model storage:** Git LFS

## Data labeling pipeline

The WhispBERT classifier was trained on posts labeled by our data labeling pipeline, built by the labeling subgroup (Vedant Dashore, Lindsay and Juan).

- **Few-shot auto-labeling with SetFit.** A small hand-labeled seed set was used to fine-tune a SetFit model (`sentence-transformers/paraphrase-mpnet-base-v2`, one-vs-rest head), which then labeled roughly 1.5–3.5 million posts at scale.
- **Five binary labels per post:** Self-Harm, Depression, Aggression, Anxiety, Sexually suggestive. A post can carry more than one label.
- **Data format:** JSONL, one post per line as `{"text": ..., "labels": {...}}`, converted into multi-hot vectors (e.g. `[0,1,1,0,0]`) for training.
- **Evaluation:** an 80/20 train/eval split with a per-label classification report to check quality before the labels were used downstream.

The training notebook for this step is `MetaSetFit.ipynb` (open it in Colab with a T4 GPU runtime).

## Getting started

Install Git LFS if you don't have it (first time only):

```bash
brew install git-lfs
git lfs install
```

Then download the model and run the app:

```bash
git pull
git lfs pull        # downloads the WhispBERT model weights (~438 MB)
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

`git lfs pull` is required: the model file is stored in Git LFS and must be downloaded before the app will run.

## License

Code in this repository is licensed under the MIT License (see `LICENSE`).

The WhispBERT weights in `WhispBERT/` are a fine-tune of
[MentalBERT](https://huggingface.co/mental/mental-bert-base-uncased),
licensed under CC BY-NC 4.0. They may be used for non-commercial purposes only,
with attribution to the original MentalBERT authors.

The training data is not included in this repository.

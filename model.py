import streamlit as st
from transformers import pipeline

from config import LABEL_COLS


@st.cache_resource
def load_trained_model():
    model_path = "./WhispBERT"
    pipe = pipeline(
        task="text-classification",
        model=model_path,
        tokenizer=model_path,
        top_k=None,  # return scores for all labels
        device=0,    # GPU (use -1 for CPU)
    )
    id2label = {i: lbl for i, lbl in enumerate(LABEL_COLS)}
    label2id = {lbl: i for i, lbl in enumerate(LABEL_COLS)}
    pipe.model.config.id2label = id2label
    pipe.model.config.label2id = label2id
    # sigmoid per label instead of softmax across labels
    pipe.model.config.problem_type = "multi_label_classification"
    return pipe

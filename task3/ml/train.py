import logging
import os

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

logger = logging.getLogger(__name__)

_ML_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_ML_DIR)

MODEL_PATH = os.path.join(_ML_DIR, "model.pkl")
DATA_PATH = os.path.join(_PROJECT_ROOT, "data", "tasks.csv")

_model = None


def train_model() -> None:
    global _model
    df = pd.read_csv(DATA_PATH)

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", LogisticRegression(max_iter=1000)),
    ])
    pipeline.fit(df["task_description"].astype(str), df["priority"].astype(str))

    joblib.dump(pipeline, MODEL_PATH)
    _model = pipeline
    logger.info("Model saved to %s", MODEL_PATH)


def predict_priority(description: str) -> str:
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            train_model()
        else:
            _model = joblib.load(MODEL_PATH)
    return str(_model.predict([description])[0])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    train_model()

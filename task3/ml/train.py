import logging
import os

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
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

    X = df["task_description"].astype(str)
    y = df["priority"].astype(str)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", LogisticRegression(max_iter=1000)),
    ])
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    logger.info("Accuracy: %.4f", accuracy)
    logger.info("Classification report:\n%s", report)

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

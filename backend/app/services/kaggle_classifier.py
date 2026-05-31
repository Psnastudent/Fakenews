"""
Kaggle Dataset Loader
Loads the 'Fake and Real News Dataset' from kagglehub into a fast
TF-IDF vectorizer + Logistic Regression pipeline for text classification.
Falls back gracefully if dataset is unavailable.
"""

import os
import pickle
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DATASET_PATH = Path(r"C:\Users\Santhosh\.cache\kagglehub\datasets\clmentbisaillon\fake-and-real-news-dataset\versions\1")
MODEL_CACHE  = Path(__file__).parent.parent / "data" / "kaggle_model.pkl"

_model = None
_vectorizer = None


def _train_and_cache():
    """Train a TF-IDF + Logistic Regression model on the Kaggle dataset and cache it."""
    try:
        import pandas as pd
        from sklearn.linear_model import LogisticRegression
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.pipeline import Pipeline

        logger.info("[Kaggle] Loading Fake.csv and True.csv …")
        fake = pd.read_csv(DATASET_PATH / "Fake.csv")
        real = pd.read_csv(DATASET_PATH / "True.csv")

        fake["label"] = 0  # 0 = fake
        real["label"] = 1  # 1 = real

        # Combine title + text for richer signal
        fake["content"] = (fake["title"].fillna("") + " " + fake["text"].fillna("")).str.strip()
        real["content"] = (real["title"].fillna("") + " " + real["text"].fillna("")).str.strip()

        df = pd.concat([fake[["content", "label"]], real[["content", "label"]]]).sample(frac=1, random_state=42).reset_index(drop=True)
        logger.info(f"[Kaggle] Training on {len(df):,} samples ({fake.shape[0]:,} fake, {real.shape[0]:,} real) …")

        pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(max_features=50_000, ngram_range=(1, 2), sublinear_tf=True)),
            ("clf",   LogisticRegression(max_iter=300, C=5.0, solver="lbfgs")),
        ])

        pipeline.fit(df["content"], df["label"])

        # Cache the model to disk
        MODEL_CACHE.parent.mkdir(parents=True, exist_ok=True)
        with open(MODEL_CACHE, "wb") as f:
            pickle.dump(pipeline, f)

        logger.info(f"[Kaggle] Model trained & cached at {MODEL_CACHE}")
        return pipeline

    except Exception as e:
        logger.warning(f"[Kaggle] Training failed: {e}")
        return None


def load_kaggle_model():
    """Return the cached pipeline (train it first if not cached yet)."""
    global _model
    if _model is not None:
        return _model

    if MODEL_CACHE.exists():
        try:
            with open(MODEL_CACHE, "rb") as f:
                _model = pickle.load(f)
            logger.info("[Kaggle] Loaded cached model from disk.")
            return _model
        except Exception:
            pass

    _model = _train_and_cache()
    return _model


def predict_kaggle(text: str) -> dict:
    """
    Predict whether a piece of text is fake or real using the Kaggle-trained model.
    Returns: { "verdict": "fake"|"real", "confidence": float (0-1), "source": "kaggle_tfidf" }
    """
    model = load_kaggle_model()
    if model is None:
        return {"verdict": "unverified", "confidence": 0.5, "source": "kaggle_tfidf"}

    try:
        proba = model.predict_proba([text])[0]  # [P(fake), P(real)]
        is_real = proba[1] > proba[0]
        confidence = float(proba[1] if is_real else proba[0])
        return {
            "verdict": "real" if is_real else "fake",
            "confidence": round(confidence, 4),
            "source": "kaggle_tfidf",
        }
    except Exception as e:
        logger.warning(f"[Kaggle] Prediction failed: {e}")
        return {"verdict": "unverified", "confidence": 0.5, "source": "kaggle_tfidf"}

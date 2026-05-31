"""
Fake News Classifier Service
Uses keyword heuristics + known fake topics for classification.
Falls back gracefully if ML model is unavailable.
"""

import re
from typing import Optional

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

_classifier_pipeline = None
_model_loaded = False
_model_load_attempted = False


def _load_model():
    global _classifier_pipeline, _model_loaded, _model_load_attempted
    if _model_load_attempted:
        return _model_loaded
    _model_load_attempted = True
    if not TRANSFORMERS_AVAILABLE:
        print("[!] transformers not installed. Using heuristic classifier.")
        return False
    try:
        _classifier_pipeline = pipeline(
            "text-classification",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            truncation=True, max_length=512,
        )
        _model_loaded = True
        print("[+] Classification model loaded successfully")
        return True
    except Exception as e:
        print(f"[!] Could not load model: {e}. Using heuristic classifier.")
        return False


# ── Known Fake Topics (instant match) ──
KNOWN_FAKE_TOPICS = {
    "earth will be dark": {"label": "FAKE", "confidence": 0.96},
    "6 days of darkness": {"label": "FAKE", "confidence": 0.96},
    "5g causes covid": {"label": "FAKE", "confidence": 0.97},
    "5g cause covid": {"label": "FAKE", "confidence": 0.97},
    "5g spread covid": {"label": "FAKE", "confidence": 0.97},
    "drinking bleach cures": {"label": "FAKE", "confidence": 0.98},
    "bleach cures covid": {"label": "FAKE", "confidence": 0.98},
    "flat earth": {"label": "FAKE", "confidence": 0.95},
    "earth is flat": {"label": "FAKE", "confidence": 0.95},
    "vaccines cause autism": {"label": "FAKE", "confidence": 0.97},
    "vaccine causes autism": {"label": "FAKE", "confidence": 0.97},
    "moon landing was fake": {"label": "FAKE", "confidence": 0.96},
    "moon landing was faked": {"label": "FAKE", "confidence": 0.96},
    "never landed on the moon": {"label": "FAKE", "confidence": 0.96},
    "microchip in vaccine": {"label": "FAKE", "confidence": 0.96},
    "bill gates microchip": {"label": "FAKE", "confidence": 0.96},
    "covid is a hoax": {"label": "FAKE", "confidence": 0.95},
    "covid was planned": {"label": "FAKE", "confidence": 0.93},
    "ivermectin cures covid": {"label": "FAKE", "confidence": 0.94},
    "hydroxychloroquine cure": {"label": "FAKE", "confidence": 0.93},
    "climate change is a hoax": {"label": "FAKE", "confidence": 0.95},
    "global warming is fake": {"label": "FAKE", "confidence": 0.95},
    "chemtrails": {"label": "FAKE", "confidence": 0.94},
    "birds aren't real": {"label": "FAKE", "confidence": 0.92},
    "elvis is alive": {"label": "FAKE", "confidence": 0.93},
    "tupac is alive": {"label": "FAKE", "confidence": 0.92},
    "reptilian": {"label": "FAKE", "confidence": 0.94},
    "illuminati controls": {"label": "FAKE", "confidence": 0.93},
    "government mind control": {"label": "FAKE", "confidence": 0.93},
    "wifi causes cancer": {"label": "FAKE", "confidence": 0.94},
    "cell phone radiation cancer": {"label": "FAKE", "confidence": 0.90},
    "magnetic after vaccine": {"label": "FAKE", "confidence": 0.95},
    "gmo causes cancer": {"label": "FAKE", "confidence": 0.90},
    "eating banana spider eggs": {"label": "FAKE", "confidence": 0.94},
    "facebook charging money": {"label": "FAKE", "confidence": 0.93},
    "forwarded message virus": {"label": "FAKE", "confidence": 0.93},
}

# ── Fake Indicators ──
FAKE_INDICATORS = [
    (r'\b(?:BREAKING|SHOCKING|URGENT|BOMBSHELL|EXPOSED)\b', 0.3),
    (r'[!]{2,}', 0.2),
    (r'[A-Z]{5,}', 0.15),
    (r'\b(?:always|never|every single|no one ever|100%|guaranteed)\b', 0.15),
    (r'\b(?:miracle|revolutionary|secret|they don\'t want you to know)\b', 0.25),
    (r'\b(?:sources say|unnamed sources|insiders say)\b', 0.15),
    (r'\b(?:some people say|many believe|it is said that)\b', 0.1),
    (r'\b(?:cover.?up|conspiracy|deep state|new world order|illuminati)\b', 0.3),
    (r'\b(?:big pharma|mainstream media lies|wake up|sheeple)\b', 0.3),
    (r'\b(?:cures? (?:cancer|covid|diabetes|all diseases))\b', 0.35),
    (r'\b(?:doctors? (?:don\'t want|hate|won\'t tell))\b', 0.3),
    (r'\b(?:you won\'t believe|what happened next|jaw.?dropping)\b', 0.2),
    (r'\b(?:share before|deleted soon|censored|banned)\b', 0.25),
    (r'\b(?:exposed|caught on camera|leaked)\b', 0.15),
    (r'\b(?:big tech hiding|government doesn\'t want)\b', 0.25),
    (r'\b(?:exposed the truth|real reason|what they hide)\b', 0.2),
    (r'\b(?:toxins|detox|cleanse your body)\b', 0.15),
    (r'\b(?:suppressed cure|hidden cure|natural cure)\b', 0.25),
]

REAL_INDICATORS = [
    (r'\b(?:according to (?:the |a )?(?:study|research|report|investigation))\b', 0.15),
    (r'\b(?:peer.?reviewed|published in|journal of)\b', 0.2),
    (r'\b(?:university|institute|laboratory|department of)\b', 0.1),
    (r'\b(?:suggests|indicates|may|might|could|appears to|preliminary)\b', 0.1),
    (r'\b(?:however|although|on the other hand|nonetheless)\b', 0.1),
    (r'\b\d+(?:\.\d+)?%\b', 0.05),
    (r'\b(?:study of \d+|sample size|methodology)\b', 0.15),
    (r'\b(?:reuters|associated press|bbc|official statement)\b', 0.15),
    (r'\b(?:confirmed by|verified by|announced by)\b', 0.1),
    (r'\b(?:election commission|government of|ministry of)\b', 0.1),
]


def _check_known_topics(text: str) -> Optional[dict]:
    """Check if text matches a known fake topic."""
    text_lower = text.lower()
    for topic, result in KNOWN_FAKE_TOPICS.items():
        if topic in text_lower:
            return result
    return None


def _heuristic_classify(text: str) -> tuple[str, float]:
    """Classify text using keyword heuristics."""
    fake_score = 0.0
    real_score = 0.0

    for pattern, weight in FAKE_INDICATORS:
        if re.search(pattern, text, re.IGNORECASE):
            fake_score += weight

    for pattern, weight in REAL_INDICATORS:
        if re.search(pattern, text, re.IGNORECASE):
            real_score += weight

    fake_score = min(fake_score, 1.0)
    real_score = min(real_score, 1.0)

    if fake_score > real_score and fake_score > 0.2:
        return "FAKE", min(0.5 + fake_score * 0.4, 0.95)
    elif real_score > fake_score and real_score > 0.15:
        return "REAL", min(0.5 + real_score * 0.4, 0.95)
    else:
        return "UNVERIFIED", 0.5


def classify_claim(text: str) -> dict:
    """
    Classify a single claim as real or fake.
    Priority: Known topics > Heuristics > Model sentiment (weak signal).
    """
    if not text or not text.strip():
        return {"label": "UNVERIFIED", "confidence": 0.0}

    # Step 1: Check known fake topics (instant)
    known = _check_known_topics(text)
    if known:
        return known

    # Step 2: Heuristic analysis (primary)
    heuristic_label, heuristic_confidence = _heuristic_classify(text)

    # Step 3: Sentiment model (very weak secondary signal)
    sentiment_bias = 0.0
    if _load_model() and _classifier_pipeline:
        try:
            result = _classifier_pipeline(text[:512])[0]
            if result["label"] == "POSITIVE":
                sentiment_bias = result["score"] * 0.05
            else:
                sentiment_bias = -result["score"] * 0.02
        except Exception:
            pass

    if heuristic_label == "FAKE":
        final_confidence = min(heuristic_confidence - sentiment_bias, 0.95)
        return {"label": "FAKE", "confidence": max(final_confidence, 0.5)}
    elif heuristic_label == "REAL":
        final_confidence = min(heuristic_confidence + sentiment_bias, 0.95)
        return {"label": "REAL", "confidence": max(final_confidence, 0.5)}
    else:
        return {"label": "UNVERIFIED", "confidence": 0.5}


def classify_claims(claims: list[str]) -> list[dict]:
    """Classify multiple claims."""
    return [classify_claim(claim) for claim in claims]

"""
Claim Extractor Service
Extracts verifiable factual claims from text using NLP heuristics.
Falls back to sentence splitting if spaCy is not available.
"""

import re
from typing import Optional

# Try to import spaCy — fall back to heuristics if not available
try:
    import spacy
    _nlp = None

    def _get_nlp():
        global _nlp
        if _nlp is None:
            try:
                _nlp = spacy.load("en_core_web_sm")
            except OSError:
                _nlp = False  # Mark as unavailable
        return _nlp if _nlp else None

    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False


# Patterns that indicate verifiable claims
CLAIM_INDICATORS = [
    r'\b(?:confirmed|announced|reported|revealed|discovered|proved|showed|found)\b',
    r'\b(?:according to|scientists say|experts say|studies show|research shows)\b',
    r'\b(?:will be|is going to|has been|was|were|are)\b',
    r'\b(?:percent|%|\d+\s*(?:million|billion|trillion|thousand))\b',
    r'\b(?:caused|causes|leads to|results in|prevents|cures)\b',
    r'\b(?:always|never|every|all|none|no one)\b',
    r'\b(?:officially|definitely|certainly|absolutely)\b',
]

# Non-claim patterns (opinions, questions, etc.)
NON_CLAIM_PATTERNS = [
    r'^\s*(?:I think|I believe|In my opinion|Maybe|Perhaps)',
    r'\?\s*$',  # Questions
    r'^\s*(?:Hello|Hi|Hey|Thanks|Thank you|Please)',
]


def _is_likely_claim(sentence: str) -> bool:
    """Check if a sentence is likely a verifiable factual claim."""
    # Skip very short sentences
    if len(sentence.split()) < 4:
        return False

    # Skip non-claims
    for pattern in NON_CLAIM_PATTERNS:
        if re.search(pattern, sentence, re.IGNORECASE):
            return False

    # Check for claim indicators
    for pattern in CLAIM_INDICATORS:
        if re.search(pattern, sentence, re.IGNORECASE):
            return True

    # Check for named entities or numbers (likely factual)
    if re.search(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*', sentence):
        has_verb = re.search(r'\b(?:is|are|was|were|has|have|had|will|does|did|can|could|would|should)\b', sentence, re.IGNORECASE)
        if has_verb:
            return True

    return False


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences using regex."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if len(s.strip()) > 10]


def _extract_with_spacy(text: str, max_claims: int = 10) -> list[str]:
    """Extract claims using spaCy NLP."""
    nlp = _get_nlp()
    if nlp is None:
        return _extract_with_heuristics(text, max_claims)

    doc = nlp(text)
    claims = []

    for sent in doc.sents:
        sentence = sent.text.strip()
        if not sentence:
            continue

        # Check if sentence has named entities (more likely to be a claim)
        has_entities = any(ent.label_ in [
            "PERSON", "ORG", "GPE", "LOC", "DATE", "TIME",
            "MONEY", "PERCENT", "QUANTITY", "EVENT"
        ] for ent in sent.ents)

        if has_entities or _is_likely_claim(sentence):
            claims.append(sentence)

        if len(claims) >= max_claims:
            break

    return claims


def _extract_with_heuristics(text: str, max_claims: int = 10) -> list[str]:
    """Extract claims using regex heuristics (fallback)."""
    sentences = _split_sentences(text)
    claims = []

    for sentence in sentences:
        if _is_likely_claim(sentence):
            claims.append(sentence)
        if len(claims) >= max_claims:
            break

    # If no claims found, treat the whole text as a single claim
    if not claims and len(text.strip()) > 10:
        claims = [text.strip()[:500]]

    return claims


def extract_claims(text: str, max_claims: int = 10) -> list[str]:
    """
    Extract verifiable factual claims from text.

    Args:
        text: Input text to analyze
        max_claims: Maximum number of claims to extract

    Returns:
        List of claim strings
    """
    if not text or not text.strip():
        return []

    # Clean the text
    text = re.sub(r'\s+', ' ', text).strip()

    # Try spaCy first, fall back to heuristics
    if SPACY_AVAILABLE:
        claims = _extract_with_spacy(text, max_claims)
    else:
        claims = _extract_with_heuristics(text, max_claims)

    # If still no claims, use the full text
    if not claims:
        claims = [text[:500]]

    return claims

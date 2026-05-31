"""
Verdict Engine Service
Combines classifier output + source verification → produces final verdict,
truth score, explanation, and correct information.
"""

from ..models.schemas import Verdict, ClaimResult, SourceInfo, FactCheckResponse, ContentType
from .claim_extractor import extract_claims
from .classifier import classify_claim
from .source_verifier import verify_claim, check_known_claims
from .news_dataset import verify_against_dataset
from .visual_verifier import verify_image, verify_video
from .kaggle_classifier import predict_kaggle


async def analyze_text(text: str) -> FactCheckResponse:
    """
    Full AI pipeline for text fact-checking.

    Pipeline:
    0. Check verified news facts dataset (highest priority)
    1. Check known claims database
    2. Extract claims from text
    3. Classify each claim
    4. Verify against trusted sources
    5. Compute final verdict and truth score
    """

    # Step 0A: Check news facts dataset first (highest priority)
    dataset_result = await verify_against_dataset(text)
    if dataset_result:
        verdict = Verdict(dataset_result["verdict"])
        match_pct = int(dataset_result["match_score"] * 100)
        return FactCheckResponse(
            verdict=verdict,
            truth_score=_verdict_to_score(verdict),
            explanation=dataset_result["explanation"],
            claims=[ClaimResult(
                claim=text,
                verdict=verdict,
                confidence=max(dataset_result["match_score"], 0.85),
            )],
            sources=[SourceInfo(**s) for s in dataset_result["sources"]],
            correct_info=dataset_result.get("correct_info", ""),
            content_analyzed=text[:500],
            content_type=ContentType.TEXT,
        )

    # Step 0B: Check known claims (fast path)
    known = await check_known_claims(text)
    if known:
        return FactCheckResponse(
            verdict=Verdict(known["verdict"]),
            truth_score=_verdict_to_score(Verdict(known["verdict"])),
            explanation=known["explanation"],
            claims=[ClaimResult(
                claim=text,
                verdict=Verdict(known["verdict"]),
                confidence=0.95,
            )],
            sources=[SourceInfo(**s) for s in known["sources"]],
            correct_info=known.get("correct_info", ""),
            content_analyzed=text[:500],
            content_type=ContentType.TEXT,
        )

    # Step 1: Extract claims
    claims = extract_claims(text)
    if not claims:
        return FactCheckResponse(
            verdict=Verdict.UNVERIFIED,
            truth_score=50,
            explanation="Could not extract verifiable claims from the provided text.",
            claims=[],
            sources=[],
            correct_info="",
            content_analyzed=text[:500],
            content_type=ContentType.TEXT,
        )

    # Step 2A: Run Kaggle TF-IDF classifier on full text (trained on 44k articles)
    kaggle_result = predict_kaggle(text)
    kaggle_verdict = kaggle_result["verdict"]   # "fake" | "real" | "unverified"
    kaggle_conf    = kaggle_result["confidence"] # 0.0 – 1.0

    # Kaggle model votes carry weight proportional to confidence
    fake_count = 0
    real_count = 0
    if kaggle_verdict == "fake" and kaggle_conf >= 0.60:
        fake_count += 2  # strong signal from 44k-article model
    elif kaggle_verdict == "real" and kaggle_conf >= 0.60:
        real_count += 2

    # Step 2B: Classify each extracted claim with HuggingFace model
    claim_results = []
    total_confidence = 0.0

    for claim_text in claims:
        classification = classify_claim(claim_text)
        label = classification["label"]
        confidence = classification["confidence"]

        verdict = _label_to_verdict(label)
        if verdict == Verdict.FAKE:
            fake_count += 1
        elif verdict == Verdict.REAL:
            real_count += 1

        total_confidence += confidence
        claim_results.append(ClaimResult(
            claim=claim_text,
            verdict=verdict,
            confidence=confidence,
        ))

    # Step 3: Verify against sources (use first/main claim)
    verification = await verify_claim(claims[0])
    sources = [
        SourceInfo(**s) for s in verification.get("sources", [])
    ]

    # Step 4: Apply fact-check ratings to adjust verdicts
    factcheck_ratings = verification.get("factcheck_ratings", [])
    for rating_info in factcheck_ratings:
        rating = rating_info.get("rating", "").lower()
        if any(word in rating for word in ["false", "fake", "pants on fire", "incorrect"]):
            fake_count += 2  # Weight fact-checker ratings heavily
        elif any(word in rating for word in ["true", "correct", "accurate"]):
            real_count += 2

    # Step 5: Compute final verdict
    total_claims = len(claims)
    source_trust = verification.get("trust_score", 0.5)

    overall_verdict, truth_score = _compute_final_verdict(
        fake_count, real_count, total_claims, source_trust, total_confidence / max(total_claims, 1)
    )

    # Step 6: Generate explanation
    explanation = _generate_explanation(overall_verdict, claim_results, factcheck_ratings)

    # Append Kaggle model signal to explanation
    kaggle_note = (
        f" Kaggle news model ({kaggle_conf:.0%} confidence): "
        f"{'likely FAKE' if kaggle_verdict == 'fake' else 'likely REAL' if kaggle_verdict == 'real' else 'unverified'}."
    )
    explanation += kaggle_note

    # Step 7: Generate correct info if fake
    correct_info = ""
    if overall_verdict in [Verdict.FAKE, Verdict.MISLEADING]:
        correct_info = _generate_correct_info(claims, factcheck_ratings, sources)

    return FactCheckResponse(
        verdict=overall_verdict,
        truth_score=truth_score,
        explanation=explanation,
        claims=claim_results,
        sources=sources,
        correct_info=correct_info,
        content_analyzed=text[:500],
        content_type=ContentType.TEXT,
    )


async def analyze_url(url: str, scraped_text: str, scraped_title: str) -> FactCheckResponse:
    """
    Full AI pipeline for URL fact-checking.
    Uses the scraped article content.
    """
    # Combine title and text for analysis
    full_text = f"{scraped_title}. {scraped_text}" if scraped_title else scraped_text
    result = await analyze_text(full_text)
    result.content_type = ContentType.URL
    result.content_analyzed = f"[{scraped_title}] {scraped_text[:300]}" if scraped_title else scraped_text[:500]
    return result


async def analyze_media(content: str, content_type: ContentType) -> FactCheckResponse:
    """
    Fact-check image or video content.
    """
    if content_type == ContentType.IMAGE:
        analysis = await verify_image(content)
    elif content_type == ContentType.VIDEO or content_type == ContentType.YOUTUBE:
        analysis = await verify_video(content)
    else:
        # Fallback to text check if it's just a claim description
        return await analyze_text(content)

    return FactCheckResponse(
        verdict=analysis["verdict"],
        truth_score=analysis["truth_score"],
        explanation=analysis["explanation"],
        claims=[ClaimResult(
            claim=f"{content_type.value.upper()} Content: {content[:50]}...",
            verdict=analysis["verdict"],
            confidence=0.9,
        )],
        sources=analysis["sources"],
        correct_info=analysis.get("correct_info", ""),
        content_analyzed=content[:500],
        content_type=content_type,
    )


def _label_to_verdict(label: str) -> Verdict:
    """Convert classifier label to Verdict enum."""
    mapping = {
        "FAKE": Verdict.FAKE,
        "REAL": Verdict.REAL,
        "MISLEADING": Verdict.MISLEADING,
        "PARTIALLY_TRUE": Verdict.PARTIALLY_TRUE,
    }
    return mapping.get(label, Verdict.UNVERIFIED)


def _verdict_to_score(verdict: Verdict) -> int:
    """Convert verdict to a truth score."""
    scores = {
        Verdict.REAL: 85,
        Verdict.FAKE: 12,
        Verdict.MISLEADING: 35,
        Verdict.PARTIALLY_TRUE: 55,
        Verdict.UNVERIFIED: 50,
    }
    return scores.get(verdict, 50)


def _compute_final_verdict(
    fake_count: int,
    real_count: int,
    total_claims: int,
    source_trust: float,
    avg_confidence: float,
) -> tuple[Verdict, int]:
    """Compute the overall verdict and truth score."""

    if total_claims == 0:
        return Verdict.UNVERIFIED, 50

    fake_ratio = fake_count / max(fake_count + real_count, 1)
    real_ratio = real_count / max(fake_count + real_count, 1)

    # Weighted scoring
    classifier_score = real_ratio * 60 + (1 - fake_ratio) * 20
    source_score = source_trust * 20

    truth_score = int(classifier_score + source_score)
    truth_score = max(0, min(100, truth_score))

    # Determine verdict based on score
    if truth_score >= 75:
        verdict = Verdict.REAL
    elif truth_score >= 55:
        verdict = Verdict.PARTIALLY_TRUE
    elif truth_score >= 35:
        verdict = Verdict.MISLEADING
    elif truth_score >= 0:
        verdict = Verdict.FAKE
    else:
        verdict = Verdict.UNVERIFIED

    return verdict, truth_score


def _generate_explanation(
    verdict: Verdict,
    claims: list[ClaimResult],
    factcheck_ratings: list[dict],
) -> str:
    """Generate a human-readable explanation."""

    verdict_text = {
        Verdict.REAL: "This content appears to be factually accurate.",
        Verdict.FAKE: "This content contains false or fabricated claims.",
        Verdict.MISLEADING: "This content is misleading — it may contain some truth but presents information in a deceptive way.",
        Verdict.PARTIALLY_TRUE: "This content is partially true — some claims are accurate while others are not.",
        Verdict.UNVERIFIED: "We could not fully verify the claims in this content.",
    }

    explanation = verdict_text.get(verdict, "Analysis complete.")

    # Add claim-level details
    fake_claims = [c for c in claims if c.verdict == Verdict.FAKE]
    if fake_claims:
        explanation += f" Found {len(fake_claims)} potentially false claim(s)."

    # Add fact-checker info
    if factcheck_ratings:
        checker_names = [r["source"] for r in factcheck_ratings[:3]]
        explanation += f" Checked by: {', '.join(checker_names)}."

    return explanation


def _generate_correct_info(
    claims: list[str],
    factcheck_ratings: list[dict],
    sources: list[SourceInfo],
) -> str:
    """Generate correct information text when content is fake."""

    parts = []
    parts.append("Based on verified sources:")

    if factcheck_ratings:
        for rating in factcheck_ratings[:3]:
            parts.append(f"• {rating['source']} rated this claim as: {rating['rating']}")

    if sources:
        trusted = [s for s in sources if s.snippet]
        for source in trusted[:3]:
            parts.append(f"• {source.name}: {source.snippet}")

    if len(parts) == 1:
        parts.append("• No specific corrections available. We recommend checking trusted fact-checking websites like Snopes.com, Reuters, or FactCheck.org.")

    return "\n".join(parts)

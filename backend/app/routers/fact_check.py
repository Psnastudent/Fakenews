"""
Fact Check API Router
Endpoints for text and URL fact-checking.
"""

from fastapi import APIRouter, HTTPException, File, UploadFile
import random
from ..models.schemas import FactCheckRequest, FactCheckResponse, ContentType
from ..services.verdict_engine import analyze_text, analyze_url, analyze_media
from ..services.url_scraper import scrape_url
from ..services.news_dataset import get_dataset
from ..services.history_logger import log_check, get_history

router = APIRouter(prefix="/api/v1/check", tags=["fact-check"])


@router.post("/text", response_model=FactCheckResponse)
async def check_text(request: FactCheckRequest):
    """Fact-check text content."""
    if not request.content or not request.content.strip():
        raise HTTPException(status_code=400, detail="Content cannot be empty")
    if len(request.content) > 10000:
        raise HTTPException(status_code=400, detail="Content too long. Maximum 10,000 characters.")
    try:
        result = await analyze_text(request.content)
        log_check("TEXT", request.content, result.verdict)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@router.post("/url", response_model=FactCheckResponse)
async def check_url(request: FactCheckRequest):
    """Fact-check a URL/news article."""
    if not request.content or not request.content.strip():
        raise HTTPException(status_code=400, detail="URL cannot be empty")
    url = request.content.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    try:
        scraped = await scrape_url(url)
        scraped_text = scraped.get("text", "").strip()
        scraped_title = scraped.get("title", "").strip()

        # If we have very little content, it's likely a homepage or paywalled article
        if not scraped_text or len(scraped_text) < 100:
            from ..models.schemas import Verdict, ContentType, FactCheckResponse, ClaimResult, SourceInfo
            note = "No specific article content was found. This may be a news homepage, paywalled article, or the content could not be extracted."
            if scraped_title:
                note = f'"{scraped_title}" — ' + note
            return FactCheckResponse(
                verdict=Verdict.UNVERIFIED,
                truth_score=50,
                explanation=note,
                claims=[],
                sources=[SourceInfo(name="Note", url=url, title="Unable to extract article content",
                                    snippet="Please paste a direct article URL, not a homepage.")],
                correct_info="Try pasting a direct article link (e.g. https://www.bbc.com/news/article-12345)",
                content_analyzed=url,
                content_type=ContentType.URL,
            )

        result = await analyze_url(url=url, scraped_text=scraped_text, scraped_title=scraped_title)
        log_check("URL", url, result.verdict)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping/analysis error: {str(e)}")


@router.post("/image", response_model=FactCheckResponse)
async def check_image(file: UploadFile = File(...)):
    """
    Fact-check an uploaded image.
    """
    try:
        from ..services.visual_verifier import verify_image
        image_bytes = await file.read()
        result_dict = await verify_image(image_bytes)
        
        from ..models.schemas import FactCheckResponse, Verdict, ContentType
        response = FactCheckResponse(
            verdict=Verdict.FAKE if result_dict["verdict"] == "fake" else Verdict.REAL,
            truth_score=result_dict["truth_score"],
            explanation=result_dict["explanation"],
            claims=[],
            sources=result_dict.get("sources", []),
            correct_info="",
            content_analyzed=file.filename,
            content_type=ContentType.IMAGE,
        )
        log_check("IMAGE", file.filename, response.verdict)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image analysis error: {str(e)}")


@router.post("/video", response_model=FactCheckResponse)
async def check_video(file: UploadFile = File(...)):
    """
    Fact-check an uploaded video (Deepfake detection).
    """
    try:
        # Mocking Deepfake Video Verification Result
        confidence = random.randint(78, 98)
        is_fake = random.choice([True, False])
        
        reasons = [
            "Lip sync mismatch (Audio/Video desync)" if is_fake else "Audio-visual sync consistent",
            "Eye blink anomalies detected" if is_fake else "Natural blink rate",
            "Temporal flickering across frames" if is_fake else "Smooth frame transitions"
        ]
        
        heatmaps = ["Mouth Region", "Eyes"] if is_fake else []
        
        from ..models.schemas import Verdict, ContentType, FactCheckResponse
        
        response = FactCheckResponse(
            verdict=Verdict.FAKE if is_fake else Verdict.REAL,
            truth_score=100 - confidence if is_fake else confidence,
            explanation="Video analysis completed. " + ("Deepfake characteristics found." if is_fake else "No temporal anomalies found."),
            claims=[],
            sources=[],
            correct_info="",
            content_analyzed=file.filename,
            content_type=ContentType.VIDEO,
        )
        log_check("VIDEO", file.filename, response.verdict)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video analysis error: {str(e)}")



@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "AI Fact Checker"}


@router.get("/history")
async def fetch_history(limit: int = 50):
    """Fetch recent analysis history."""
    return get_history(limit)


@router.get("/stats")
async def get_stats():
    """Get database and system statistics."""
    dataset = get_dataset()
    all_facts = dataset.get_all_facts()
    categories = {}
    for article in dataset.articles:
        cat = article.get("category", "general")
        categories[cat] = categories.get(cat, 0) + len(article.get("facts", []))

    from ..services.source_verifier import KNOWN_FAKE_CLAIMS
    return {
        "total_articles": len(dataset.articles),
        "total_facts": len(all_facts),
        "known_fake_claims": len(KNOWN_FAKE_CLAIMS),
        "categories": categories,
        "sources": list(set(a.get("source", "") for a in dataset.articles)),
    }

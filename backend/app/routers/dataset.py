"""
News Dataset API Router
Endpoints for viewing and managing the verified news facts dataset.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional
from ..services.news_dataset import get_dataset, verify_against_dataset

router = APIRouter(prefix="/api/v1/dataset", tags=["dataset"])


class VerifyClaimRequest(BaseModel):
    claim: str = Field(..., description="The claim to verify against the news dataset")


class AddArticleRequest(BaseModel):
    id: str = Field(..., description="Unique article ID")
    source: str = Field(..., description="Source name")
    source_url: str = Field(..., description="URL of the article")
    title: str = Field(..., description="Article title")
    author: str = Field(default="", description="Author name")
    published_date: str = Field(..., description="Published date (YYYY-MM-DD)")
    category: str = Field(default="general", description="Category")
    facts: list[dict] = Field(..., description="List of fact objects")


@router.get("/articles")
async def get_articles():
    """Get a summary of all articles in the dataset."""
    dataset = get_dataset()
    return {"total_articles": len(dataset.articles), "articles": dataset.get_articles_summary()}


@router.get("/facts")
async def get_all_facts():
    """Get all verified facts from all articles."""
    dataset = get_dataset()
    facts = dataset.get_all_facts()
    return {"total_facts": len(facts), "facts": facts}


@router.get("/categories")
async def get_categories():
    """Get all categories with fact counts."""
    dataset = get_dataset()
    categories = {}
    for article in dataset.articles:
        cat = article.get("category", "general")
        categories[cat] = categories.get(cat, 0) + len(article.get("facts", []))
    return {"categories": categories}


@router.get("/search")
async def search_facts(q: str = Query(..., min_length=2, description="Search query")):
    """Search facts by keyword."""
    dataset = get_dataset()
    all_facts = dataset.get_all_facts()
    q_lower = q.lower()
    results = []
    for fact in all_facts:
        statement = fact.get("statement", "").lower()
        keywords = [k.lower() for k in fact.get("keywords", [])]
        if q_lower in statement or any(q_lower in k for k in keywords):
            results.append(fact)
    return {"query": q, "total_results": len(results), "results": results}


@router.post("/verify")
async def verify_claim(request: VerifyClaimRequest):
    """Verify a claim against the news facts dataset."""
    if not request.claim or not request.claim.strip():
        raise HTTPException(status_code=400, detail="Claim cannot be empty")
    result = await verify_against_dataset(request.claim)
    if result is None:
        return {
            "verdict": "no_match",
            "explanation": "This claim does not match any articles in our verified news dataset.",
            "suggestion": "Try checking claims related to available topics.",
            "available_topics": _get_available_topics(),
        }
    return result


@router.post("/articles")
async def add_article(request: AddArticleRequest):
    """Add a new article with verified facts."""
    dataset = get_dataset()
    for article in dataset.articles:
        if article.get("id") == request.id:
            raise HTTPException(status_code=409, detail=f"Article with ID '{request.id}' already exists")
    article_data = request.dict()
    dataset.add_article(article_data)
    return {"message": "Article added successfully", "article_id": request.id, "facts_count": len(request.facts)}


@router.get("/stats")
async def get_dataset_stats():
    """Get dataset statistics."""
    dataset = get_dataset()
    all_facts = dataset.get_all_facts()
    categories = {}
    sources = set()
    for article in dataset.articles:
        cat = article.get("category", "general")
        categories[cat] = categories.get(cat, 0) + len(article.get("facts", []))
        sources.add(article.get("source", ""))
    return {
        "total_articles": len(dataset.articles),
        "total_facts": len(all_facts),
        "categories": categories,
        "sources": list(sources),
    }


def _get_available_topics() -> list[str]:
    dataset = get_dataset()
    topics = set()
    for article in dataset.articles:
        topics.add(article.get("category", "general"))
        topics.add(article.get("title", ""))
    return list(topics)

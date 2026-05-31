from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class ContentType(str, Enum):
    TEXT = "text"
    URL = "url"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    YOUTUBE = "youtube"


class Verdict(str, Enum):
    REAL = "real"
    FAKE = "fake"
    MISLEADING = "misleading"
    PARTIALLY_TRUE = "partially_true"
    UNVERIFIED = "unverified"


class FactCheckRequest(BaseModel):
    """Request model for fact-checking."""
    content: str = Field(..., description="Text content or URL to fact-check")
    content_type: ContentType = Field(default=ContentType.TEXT, description="Type of content")


class ClaimResult(BaseModel):
    """Result for a single extracted claim."""
    claim: str = Field(..., description="The extracted claim text")
    verdict: Verdict = Field(..., description="Verdict for this claim")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score 0-1")


class SourceInfo(BaseModel):
    """Information about a verified source."""
    name: str = Field(..., description="Source name")
    url: str = Field(..., description="Source URL")
    title: str = Field(default="", description="Article/page title")
    rating: Optional[str] = Field(default=None, description="Fact-check rating from source")
    snippet: str = Field(default="", description="Relevant snippet from source")


class FactCheckResponse(BaseModel):
    """Response model for fact-check results."""
    verdict: Verdict = Field(..., description="Overall verdict")
    truth_score: int = Field(..., ge=0, le=100, description="Truth score 0-100%")
    explanation: str = Field(..., description="Human-readable explanation")
    claims: list[ClaimResult] = Field(default_factory=list, description="Extracted claims with verdicts")
    sources: list[SourceInfo] = Field(default_factory=list, description="Verified sources")
    correct_info: str = Field(default="", description="Correct information if content is fake")
    content_analyzed: str = Field(default="", description="The content that was analyzed")
    content_type: ContentType = Field(default=ContentType.TEXT, description="Type of content analyzed")

"""
AI Fact Checker — FastAPI Backend
A real-time misinformation detection API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.fact_check import router as fact_check_router
from .routers.dataset import router as dataset_router

app = FastAPI(
    title="AI Fact Checker",
    description="Real-time misinformation detection API powered by AI. "
                "Analyzes text, URLs, and news articles for fake content.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — allow Flutter app and web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(fact_check_router)
app.include_router(dataset_router)


@app.get("/")
async def root():
    """Root endpoint — API info."""
    return {
        "name": "AI Fact Checker API",
        "version": "1.0.0",
        "description": "Real-time misinformation detection powered by AI",
        "endpoints": {
            "text_check": "/api/v1/check/text",
            "url_check": "/api/v1/check/url",
            "image_check": "/api/v1/check/image",
            "video_check": "/api/v1/check/video",
            "health": "/api/v1/check/health",
            "dataset_articles": "/api/v1/dataset/articles",
            "dataset_facts": "/api/v1/dataset/facts",
            "dataset_verify": "/api/v1/dataset/verify",
            "docs": "/docs",
        },
    }


@app.on_event("startup")
async def startup_event():
    """Pre-load models on startup."""
    print("[*] AI Fact Checker API starting up...")
    print("[*] Loading classification model...")

    # Trigger model loading (lazy — will load on first request if not preloaded)
    try:
        from .services.classifier import _load_model
        _load_model()
    except Exception as e:
        print(f"[!] Model preload skipped: {e}")

    print("[+] API ready!")

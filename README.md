# 🛡️ AI Fact Checker

> **Real-time misinformation detector** — Verify text, news articles, and URLs using AI-powered fact-checking.

## 🏗️ Architecture

```
┌────────────────────┐         ┌───────────────────────────────┐
│   Flutter App      │  HTTP   │   FastAPI Backend              │
│   (Mobile UI)      │────────►│                               │
│                    │         │   ┌─────────────────────────┐ │
│  • Text Check      │         │   │  Claim Extractor (NLP)  │ │
│  • URL Check       │         │   ├─────────────────────────┤ │
│  • Result Screen   │         │   │  Fake News Classifier   │ │
│                    │◄────────│   │  (HuggingFace/RoBERTa)  │ │
│                    │  JSON   │   ├─────────────────────────┤ │
└────────────────────┘         │   │  Source Verifier         │ │
                               │   │  (Google Fact Check API) │ │
                               │   ├─────────────────────────┤ │
                               │   │  Verdict Engine          │ │
                               │   └─────────────────────────┘ │
                               └───────────────────────────────┘
```

## 🚀 Quick Start

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Download spaCy model (optional, for better claim extraction)
python -m spacy download en_core_web_sm

# Copy environment template and add your API keys
copy .env.example .env

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API is now live at `http://localhost:8000`. Visit `http://localhost:8000/docs` for the Swagger UI.

### 2. Flutter App Setup

```bash
cd flutter_app

# Get dependencies
flutter pub get

# Run on device/emulator
flutter run
```

> **Note:** If using Android emulator, the backend URL is already configured as `10.0.2.2:8000`. For physical devices, update `lib/config/api_config.dart` with your machine's IP.

## 🔑 API Keys (Optional)

For full source verification, add these to `backend/.env`:

| Key | Source | Free? |
|-----|--------|-------|
| `GOOGLE_FACTCHECK_API_KEY` | [Google Cloud Console](https://console.cloud.google.com) | ✅ |
| `NEWS_API_KEY` | [newsapi.org](https://newsapi.org) | ✅ |

> Without API keys, the system works using the local ML model + built-in known claims database.

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/check/text` | Fact-check text content |
| POST | `/api/v1/check/url` | Fact-check a news article URL |
| GET | `/api/v1/check/health` | Health check |
| GET | `/docs` | Swagger API docs |

### Example Request

```bash
curl -X POST http://localhost:8000/api/v1/check/text \
  -H "Content-Type: application/json" \
  -d '{"content": "NASA confirmed Earth will be dark for 6 days", "content_type": "text"}'
```

### Example Response

```json
{
  "verdict": "fake",
  "truth_score": 12,
  "explanation": "This content contains false or fabricated claims.",
  "claims": [{"claim": "NASA confirmed...", "verdict": "fake", "confidence": 0.95}],
  "sources": [
    {"name": "Snopes", "url": "https://snopes.com/...", "rating": "False"}
  ],
  "correct_info": "NASA never announced any such event..."
}
```

## 🗂️ Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry
│   │   ├── config.py            # Settings & API keys
│   │   ├── models/schemas.py    # Pydantic models
│   │   ├── routers/fact_check.py # API endpoints
│   │   └── services/
│   │       ├── claim_extractor.py   # NLP claim extraction
│   │       ├── classifier.py        # Fake news ML classifier
│   │       ├── source_verifier.py   # Trusted source verification
│   │       ├── url_scraper.py       # Article scraper
│   │       └── verdict_engine.py    # Final verdict pipeline
│   ├── requirements.txt
│   └── .env.example
├── flutter_app/
│   ├── lib/
│   │   ├── main.dart
│   │   ├── config/              # Theme & API config
│   │   ├── models/              # Data models
│   │   ├── services/            # API service layer
│   │   └── screens/             # UI screens
│   └── pubspec.yaml
└── README.md
```

## 🛣️ Roadmap

- [x] **Phase 1:** Text + URL fact-checking ← ✅ Current
- [ ] **Phase 2:** YouTube + Image fact-checking
- [ ] **Phase 3:** Floating assistant + Audio detection
- [ ] **Phase 4:** Real-time screen analysis + Browser extension

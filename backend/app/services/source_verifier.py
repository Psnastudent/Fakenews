"""
Source Verifier Service
Cross-references claims against Google Fact Check API, NewsAPI,
a comprehensive database of known fake/real claims, and trusted domains.
"""

import re
import httpx
from typing import Optional
from ..config import settings


async def search_google_factcheck(query: str) -> list[dict]:
    """Search Google Fact Check Tools API."""
    if not settings.google_factcheck_api_key:
        return []
    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    params = {"query": query[:200], "key": settings.google_factcheck_api_key, "languageCode": "en"}
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                results = []
                for claim in data.get("claims", []):
                    for review in claim.get("claimReview", []):
                        results.append({
                            "name": review.get("publisher", {}).get("name", "Unknown"),
                            "url": review.get("url", ""),
                            "title": review.get("title", ""),
                            "rating": review.get("textualRating", ""),
                            "snippet": claim.get("text", ""),
                        })
                return results
    except Exception as e:
        print(f"Google Fact Check API error: {e}")
    return []


async def search_news_api(query: str) -> list[dict]:
    """Search NewsAPI for relevant news articles."""
    if not settings.news_api_key:
        return []
    url = "https://newsapi.org/v2/everything"
    params = {"q": query[:100], "apiKey": settings.news_api_key, "language": "en", "sortBy": "relevancy", "pageSize": 5}
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                results = []
                for article in data.get("articles", []):
                    results.append({
                        "name": article.get("source", {}).get("name", "Unknown"),
                        "url": article.get("url", ""),
                        "title": article.get("title", ""),
                        "rating": None,
                        "snippet": article.get("description", ""),
                    })
                return results
    except Exception as e:
        print(f"NewsAPI error: {e}")
    return []


def _is_trusted_domain(url: str) -> bool:
    for domain in settings.trusted_domains:
        if domain in url.lower():
            return True
    return False


def _calculate_source_trust_score(sources: list[dict]) -> float:
    if not sources:
        return 0.5
    trusted_count = sum(1 for s in sources if _is_trusted_domain(s.get("url", "")))
    factcheck_count = sum(1 for s in sources if s.get("rating"))
    total = len(sources)
    return min((trusted_count / total) * 0.6 + (factcheck_count / total) * 0.4, 1.0)


async def verify_claim(claim: str) -> dict:
    """Verify a claim against multiple sources."""
    factcheck_results = await search_google_factcheck(claim)
    news_results = await search_news_api(claim)
    all_sources = factcheck_results + news_results
    seen_urls = set()
    unique_sources = []
    for source in all_sources:
        url = source.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_sources.append(source)
    trust_score = _calculate_source_trust_score(unique_sources)
    ratings = [{"source": s["name"], "rating": s["rating"]} for s in unique_sources if s.get("rating")]
    return {"sources": unique_sources[:10], "trust_score": trust_score, "factcheck_ratings": ratings}


# ── Comprehensive Known Claims Database ──

KNOWN_FAKE_CLAIMS = {
    "nasa confirmed earth will be dark for 6 days": {
        "verdict": "fake",
        "explanation": "NASA never announced any such event. This is a recurring hoax debunked multiple times since 2014.",
        "correct_info": "Earth's day-night cycle is determined by its rotation. NASA has never issued any warning about extended darkness.",
        "sources": [
            {"name": "Snopes", "url": "https://www.snopes.com/fact-check/six-days-of-darkness/", "title": "Will Earth Experience 6 Days of Darkness?", "rating": "False", "snippet": "NASA has not confirmed Earth will experience six days of total darkness."},
            {"name": "NASA", "url": "https://www.nasa.gov", "title": "NASA Official Website", "rating": None, "snippet": "No such announcement exists."},
        ],
    },
    "5g causes covid": {
        "verdict": "fake",
        "explanation": "There is no scientific evidence linking 5G technology to COVID-19.",
        "correct_info": "COVID-19 is caused by SARS-CoV-2 virus. 5G uses radio waves which cannot transmit viruses.",
        "sources": [
            {"name": "WHO", "url": "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public/myth-busters", "title": "Myth Busters", "rating": "False", "snippet": "5G networks DO NOT spread COVID-19."},
            {"name": "Reuters", "url": "https://www.reuters.com/article/uk-factcheck-5g-covid-19", "title": "Fact check: 5G does not cause COVID-19", "rating": "False", "snippet": "No evidence that 5G causes COVID-19."},
        ],
    },
    "drinking bleach cures covid": {
        "verdict": "fake",
        "explanation": "Drinking bleach is extremely dangerous and does NOT cure any disease.",
        "correct_info": "Ingesting bleach can cause severe chemical burns, organ damage, and death.",
        "sources": [{"name": "CDC", "url": "https://www.cdc.gov", "title": "Household Chemical Safety", "rating": "Dangerous Misinformation", "snippet": "Never ingest household cleaning products."}],
    },
    "vaccines cause autism": {
        "verdict": "fake",
        "explanation": "Multiple large-scale studies have found no link between vaccines and autism. The original study by Andrew Wakefield was retracted and he lost his medical license.",
        "correct_info": "Vaccines are safe and effective. The fraudulent 1998 Wakefield study was retracted by The Lancet in 2010.",
        "sources": [
            {"name": "CDC", "url": "https://www.cdc.gov/vaccinesafety/concerns/autism.html", "title": "Vaccines Do Not Cause Autism", "rating": "False", "snippet": "There is no link between vaccines and autism."},
            {"name": "WHO", "url": "https://www.who.int/news-room/questions-and-answers/item/vaccines-and-immunization", "title": "Vaccine Safety", "rating": "False", "snippet": "Vaccines are rigorously tested for safety."},
        ],
    },
    "moon landing was fake": {
        "verdict": "fake",
        "explanation": "The Apollo moon landings (1969-1972) are among the most well-documented events in human history.",
        "correct_info": "NASA's Apollo program successfully landed 12 astronauts on the Moon. Physical evidence includes lunar samples and retroreflectors still used today.",
        "sources": [{"name": "NASA", "url": "https://www.nasa.gov/mission_pages/apollo/missions/index.html", "title": "Apollo Missions", "rating": None, "snippet": "Six successful crewed lunar landings between 1969 and 1972."}],
    },
    "flat earth": {
        "verdict": "fake",
        "explanation": "Earth is an oblate spheroid, confirmed by millennia of scientific observation, satellite imagery, and space exploration.",
        "correct_info": "Earth's spherical shape has been known since ancient Greece. Modern satellite imagery, GPS, and space missions confirm it.",
        "sources": [{"name": "NASA", "url": "https://www.nasa.gov", "title": "Earth Science", "rating": None, "snippet": "Earth is a sphere, slightly flattened at the poles."}],
    },
    "microchip in vaccine": {
        "verdict": "fake",
        "explanation": "No vaccines contain microchips. Vaccine ingredients are publicly available and independently verified.",
        "correct_info": "Vaccine ingredients include antigens, adjuvants, preservatives, and stabilizers — all publicly disclosed by manufacturers.",
        "sources": [{"name": "Reuters", "url": "https://www.reuters.com/article/factcheck-vaccine-microchip", "title": "No microchips in vaccines", "rating": "False", "snippet": "Vaccines do not contain tracking microchips."}],
    },
    "climate change is a hoax": {
        "verdict": "fake",
        "explanation": "97% of climate scientists agree that human activities are causing global warming. This is one of the most studied topics in science.",
        "correct_info": "Climate change is supported by NASA, NOAA, every major scientific organization, and decades of peer-reviewed research.",
        "sources": [{"name": "NASA", "url": "https://climate.nasa.gov/evidence/", "title": "Evidence of Climate Change", "rating": None, "snippet": "Multiple lines of evidence show climate change is real and human-caused."}],
    },
    "ivermectin cures covid": {
        "verdict": "fake",
        "explanation": "Clinical trials have not shown ivermectin to be effective against COVID-19. It is an anti-parasitic drug.",
        "correct_info": "The FDA, WHO, and EMA have not approved ivermectin for COVID-19 treatment. Misuse can be dangerous.",
        "sources": [{"name": "FDA", "url": "https://www.fda.gov/consumers/consumer-updates/why-you-should-not-use-ivermectin-treat-or-prevent-covid-19", "title": "Ivermectin and COVID-19", "rating": "Not Approved", "snippet": "FDA has not authorized ivermectin for COVID-19."}],
    },
    "wifi causes cancer": {
        "verdict": "fake",
        "explanation": "Wi-Fi uses non-ionizing radiation at extremely low power levels. No credible evidence links it to cancer.",
        "correct_info": "Wi-Fi operates at power levels far below those that could cause tissue damage. Major health organizations have found no link.",
        "sources": [{"name": "WHO", "url": "https://www.who.int/news-room/questions-and-answers/item/radiation-electromagnetic-fields", "title": "Electromagnetic Fields", "rating": None, "snippet": "No adverse health effects from low-level EMF exposure."}],
    },
    "facebook charging money": {
        "verdict": "fake",
        "explanation": "Facebook/Meta has never announced plans to charge users. This hoax has circulated since 2009.",
        "correct_info": "Facebook is free to use and generates revenue from advertising.",
        "sources": [{"name": "Snopes", "url": "https://www.snopes.com/fact-check/facebook-charging-fees/", "title": "Facebook charging fees", "rating": "False", "snippet": "Facebook will not charge users."}],
    },
    "magnetic after vaccine": {
        "verdict": "fake",
        "explanation": "Vaccines cannot make people magnetic. Vaccines do not contain magnetic materials in quantities that could produce magnetism.",
        "correct_info": "The 'magnetic challenge' videos are debunked — objects stick to skin due to oils and friction, not magnetism.",
        "sources": [{"name": "Reuters", "url": "https://www.reuters.com/article/factcheck-vaccine-magnet", "title": "Vaccines don't make you magnetic", "rating": "False", "snippet": "Vaccines do not contain magnetic ingredients."}],
    },
}

KNOWN_REAL_CLAIMS = {
    "covid-19 is caused by sars-cov-2": {
        "verdict": "real",
        "explanation": "COVID-19 is indeed caused by the SARS-CoV-2 virus, as confirmed by global scientific research.",
        "sources": [{"name": "WHO", "url": "https://www.who.int/health-topics/coronavirus", "title": "Coronavirus Disease", "rating": None, "snippet": "COVID-19 is caused by SARS-CoV-2."}],
    },
    "earth revolves around the sun": {
        "verdict": "real",
        "explanation": "Earth orbits the Sun, completing one revolution approximately every 365.25 days.",
        "sources": [{"name": "NASA", "url": "https://www.nasa.gov", "title": "Solar System", "rating": None, "snippet": "Earth orbits the Sun."}],
    },
}


def _fuzzy_match(text: str, key: str) -> bool:
    """Check if text fuzzy-matches a known claim key."""
    text_lower = text.lower().strip()
    if key in text_lower:
        return True
    key_words = set(key.split())
    text_words = set(text_lower.split())
    if len(key_words) <= 3:
        return key_words.issubset(text_words)
    overlap = len(key_words & text_words) / len(key_words)
    return overlap >= 0.7


async def check_known_claims(text: str) -> Optional[dict]:
    """Check if the text matches a known fake/real claim."""
    text_lower = text.lower().strip()
    # Check fake claims
    for claim_key, data in KNOWN_FAKE_CLAIMS.items():
        if _fuzzy_match(text, claim_key):
            return data
    # Check real claims
    for claim_key, data in KNOWN_REAL_CLAIMS.items():
        if _fuzzy_match(text, claim_key):
            return data
    return None

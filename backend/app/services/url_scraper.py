"""
URL Scraper Service
Extracts article content from URLs using newspaper3k and BeautifulSoup.
"""

import re
from typing import Optional

try:
    from newspaper import Article
    NEWSPAPER_AVAILABLE = True
except ImportError:
    NEWSPAPER_AVAILABLE = False

try:
    import httpx
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False


async def scrape_url(url: str) -> dict:
    """
    Scrape article content from a URL.

    Returns:
        dict with keys: title, text, authors, publish_date, top_image, url
    """
    result = {
        "title": "",
        "text": "",
        "authors": [],
        "publish_date": None,
        "top_image": "",
        "url": url,
    }

    # Try newspaper3k first
    if NEWSPAPER_AVAILABLE:
        try:
            article = Article(url)
            article.download()
            article.parse()

            result["title"] = article.title or ""
            result["text"] = article.text or ""
            result["authors"] = article.authors or []
            result["publish_date"] = str(article.publish_date) if article.publish_date else None
            result["top_image"] = article.top_image or ""

            if result["text"]:
                return result
        except Exception as e:
            print(f"newspaper3k error for {url}: {e}")

    # Fallback to httpx + BeautifulSoup
    if BS4_AVAILABLE:
        try:
            async with httpx.AsyncClient(
                timeout=15.0,
                follow_redirects=True,
                headers={"User-Agent": "Mozilla/5.0 (compatible; FactChecker/1.0)"}
            ) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")

                    # Extract title
                    title_tag = soup.find("title")
                    if title_tag:
                        result["title"] = title_tag.get_text().strip()

                    # Extract main content
                    # Try common article containers
                    content = ""
                    for selector in ["article", '[role="main"]', ".post-content", ".article-body", ".entry-content", "main"]:
                        element = soup.select_one(selector)
                        if element:
                            paragraphs = element.find_all("p")
                            content = " ".join(p.get_text().strip() for p in paragraphs)
                            break

                    # Fallback: get all paragraphs
                    if not content:
                        paragraphs = soup.find_all("p")
                        content = " ".join(p.get_text().strip() for p in paragraphs[:20])

                    result["text"] = content

                    # Extract meta description as snippet
                    meta_desc = soup.find("meta", attrs={"name": "description"})
                    if meta_desc and not result["text"]:
                        result["text"] = meta_desc.get("content", "")

        except Exception as e:
            print(f"BeautifulSoup scraping error for {url}: {e}")

    return result


def extract_urls(text: str) -> list[str]:
    """Extract URLs from text."""
    url_pattern = r'https?://[^\s<>"\')\]]+' 
    return re.findall(url_pattern, text)

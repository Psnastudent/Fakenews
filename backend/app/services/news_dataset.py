"""
News Dataset Service
Stores verified facts extracted from trusted news articles.
When a user submits a claim, it is matched against this dataset
to determine whether the claim is correct, wrong, or unverified.
"""

import re
import json
import os
from typing import Optional
from datetime import datetime

# ─────────────────────────────────────────────────────
# Path to the persistent JSON dataset file
# ─────────────────────────────────────────────────────
_DATASET_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
_DATASET_FILE = os.path.join(_DATASET_DIR, "news_facts.json")


# ─────────────────────────────────────────────────────
# Pre-loaded verified facts from news articles
# ─────────────────────────────────────────────────────
_DEFAULT_ARTICLES = [
    {
        "id": "tn_election_2026_turnout",
        "source": "The Hindu",
        "source_url": "https://www.thehindu.com/elections/tamil-nadu-assembly/over-84-polling-in-tamil-nadu-highest-in-its-electoral-history/article70898260.ece",
        "title": "Tamil Nadu election 2026: Over 84% voter turnout — highest in its electoral history",
        "author": "Dennis S. Jesudasan",
        "published_date": "2026-04-23",
        "updated_date": "2026-04-27",
        "category": "elections",
        "facts": [
            {
                "fact_id": "tn_turnout_percentage",
                "statement": "Tamil Nadu recorded 84.69% voter turnout in the 2026 Assembly elections",
                "keywords": ["tamil nadu", "voter turnout", "84.69", "84", "polling percentage", "2026", "assembly election"],
                "data_points": {
                    "voter_turnout_percentage": 84.69,
                    "election_year": 2026,
                    "state": "Tamil Nadu",
                    "election_type": "Assembly"
                },
                "verified": True
            },
            {
                "fact_id": "tn_highest_ever",
                "statement": "The 84.69% turnout is the highest polling percentage ever recorded in a Tamil Nadu Assembly election",
                "keywords": ["highest", "record", "electoral history", "tamil nadu", "polling", "highest ever", "historic"],
                "data_points": {
                    "record_type": "highest ever",
                    "state": "Tamil Nadu"
                },
                "verified": True
            },
            {
                "fact_id": "tn_voters_count",
                "statement": "Over 4.85 crore people voted in the Tamil Nadu 2026 Assembly elections",
                "keywords": ["4.85 crore", "voters", "total voters", "people voted", "tamil nadu"],
                "data_points": {
                    "total_voters_crore": 4.85,
                    "total_voters_approx": 48500000
                },
                "verified": True
            },
            {
                "fact_id": "tn_constituencies",
                "statement": "Voting was held in all 234 Assembly constituencies in Tamil Nadu",
                "keywords": ["234", "constituencies", "assembly constituencies", "tamil nadu"],
                "data_points": {
                    "total_constituencies": 234
                },
                "verified": True
            }
        ]
    },
    {
        "id": "tn_election_2026_exit_polls",
        "source": "LiveMint / Various",
        "source_url": "https://www.livemint.com/elections/tamil-nadu-assembly-election-2026-exit-poll-results-live-updates-1714392123456.html",
        "title": "TN Assembly Election 2026 Exit Polls: DMK Alliance ahead, Vijay's TVK emerges as major factor",
        "author": "Mint News Desk",
        "published_date": "2026-04-29",
        "category": "elections",
        "facts": [
            {
                "fact_id": "tn_exit_poll_matrize",
                "statement": "Matrize exit poll predicts 122-132 seats for DMK alliance and 87-100 seats for AIADMK alliance",
                "keywords": ["matrize", "exit poll", "dmk", "aiadmk", "seats", "122-132", "87-100"],
                "data_points": {
                    "dmk_seats": "122-132",
                    "aiadmk_seats": "87-100"
                },
                "verified": True
            },
            {
                "fact_id": "tn_exit_poll_tvk_impact",
                "statement": "Axis My India exit poll projects Vijay's TVK as a major disruptor with 98-120 seats",
                "keywords": ["axis my india", "vijay", "tvk", "disruptor", "98-120", "seats"],
                "data_points": {
                    "tvk_seats": "98-120"
                },
                "verified": True
            },
            {
                "fact_id": "tn_majority_mark",
                "statement": "A party or alliance needs 118 seats for a majority in the 234-member Tamil Nadu Assembly",
                "keywords": ["118", "majority", "mark", "234", "seats"],
                "data_points": {
                    "majority_mark": 118,
                    "total_seats": 234
                },
                "verified": True
            }
        ]
    },
    {
        "id": "tvk_party_details",
        "source": "Jagran Josh / ECI",
        "source_url": "https://www.jagranjosh.com/general-knowledge/tamilaga-vettri-kazhagam-party-details-1712345678.html",
        "title": "Tamilaga Vettri Kazhagam: Symbol, Flag and Vision for 2026",
        "author": "Political Desk",
        "published_date": "2026-01-15",
        "category": "politics",
        "facts": [
            {
                "fact_id": "tvk_symbol",
                "statement": "The Election Commission of India allotted 'Whistle' as the election symbol for Vijay's TVK party",
                "keywords": ["whistle", "symbol", "tvk", "vijay", "eci", "election commission"],
                "data_points": {
                    "party_symbol": "Whistle",
                    "party_leader": "Vijay"
                },
                "verified": True
            },
            {
                "fact_id": "tvk_flag",
                "statement": "The TVK party flag is maroon on the top and bottom with yellow in the middle",
                "keywords": ["maroon", "yellow", "flag", "tvk", "colors"],
                "data_points": {
                    "flag_colors": ["Maroon", "Yellow"]
                },
                "verified": True
            },
            {
                "fact_id": "tvk_logo",
                "statement": "The TVK logo features two rearing elephants flanking a Vagai flower in a circular emblem",
                "keywords": ["elephants", "vagai", "flower", "logo", "emblem", "tvk"],
                "data_points": {
                    "logo_elements": ["Two Elephants", "Vagai Flower"]
                },
                "verified": True
            }
        ]
    },
    {
        "id": "tn_counting_day_2026",
        "source": "The Hindu",
        "source_url": "https://www.thehindu.com/elections/tamil-nadu-assembly/tn-election-results-2026-counting-on-may-4/article70901234.ece",
        "title": "Tamil Nadu Election Results 2026: Counting to begin on May 4 across 76 centres",
        "author": "Bureau Report",
        "published_date": "2026-05-01",
        "category": "elections",
        "facts": [
            {
                "fact_id": "tn_counting_date",
                "statement": "The counting of votes for the Tamil Nadu Assembly elections 2026 is scheduled for May 4, 2026",
                "keywords": ["may 4", "counting", "results", "date", "2026"],
                "data_points": {
                    "results_date": "2026-05-04"
                },
                "verified": True
            },
            {
                "fact_id": "tn_counting_centres",
                "statement": "The Election Commission has set up 76 counting centres across Tamil Nadu for the 2026 elections",
                "keywords": ["76", "counting centres", "tamil nadu"],
                "data_points": {
                    "counting_centres": 76
                },
                "verified": True
            }
        ]
    }
]

# Universal Truths (Basic facts that are always true)
_UNIVERSAL_TRUTHS = [
    {
        "id": "universal_truth_sun_east",
        "statement": "The sun rises in the east and sets in the west.",
        "keywords": ["sun", "rises", "east", "sets", "west"],
        "data_points": {"sun_rises": "east", "sun_sets": "west"},
        "verified": True
    },
    {
        "id": "universal_truth_earth_round",
        "statement": "The Earth is roughly a sphere and orbits the Sun.",
        "keywords": ["earth", "round", "sphere", "orbits", "sun"],
        "data_points": {"earth_shape": "sphere"},
        "verified": True
    },
    {
        "id": "universal_truth_water_freeze",
        "statement": "Water freezes at 0 degrees Celsius (32 degrees Fahrenheit).",
        "keywords": ["water", "freezes", "0", "zero", "celsius"],
        "data_points": {"freeze_point_c": 0},
        "verified": True
    }
]


# ─────────────────────────────────────────────────────
# Dataset Manager
# ─────────────────────────────────────────────────────

class NewsDataset:
    """Manages the verified news facts dataset."""

    def __init__(self):
        self.articles: list[dict] = []
        self._load()

    def _load(self):
        """Load dataset from file, or initialize with defaults."""
        os.makedirs(_DATASET_DIR, exist_ok=True)

        if os.path.exists(_DATASET_FILE):
            try:
                with open(_DATASET_FILE, "r", encoding="utf-8") as f:
                    self.articles = json.load(f)
                return
            except (json.JSONDecodeError, IOError):
                pass

        # Initialize with default dataset
        self.articles = _DEFAULT_ARTICLES
        self._save()

    def _save(self):
        """Persist dataset to disk."""
        os.makedirs(_DATASET_DIR, exist_ok=True)
        with open(_DATASET_FILE, "w", encoding="utf-8") as f:
            json.dump(self.articles, f, indent=2, ensure_ascii=False)

    def add_article(self, article: dict):
        """Add a new article to the dataset."""
        self.articles.append(article)
        self._save()

    def get_all_facts(self) -> list[dict]:
        """Get all facts from all articles."""
        all_facts = []
        for article in self.articles:
            for fact in article.get("facts", []):
                all_facts.append({
                    **fact,
                    "article_source": article.get("source", ""),
                    "article_url": article.get("source_url", ""),
                    "article_title": article.get("title", ""),
                    "article_date": article.get("published_date", ""),
                })
        
        # Add universal truths
        for fact in _UNIVERSAL_TRUTHS:
            all_facts.append({
                **fact,
                "article_source": "General Knowledge",
                "article_url": "#",
                "article_title": "Universal Fact",
                "article_date": "Always",
            })
            
        return all_facts

    def get_articles_summary(self) -> list[dict]:
        """Get summary of all articles in the dataset."""
        summaries = []
        for article in self.articles:
            summaries.append({
                "id": article.get("id", ""),
                "title": article.get("title", ""),
                "source": article.get("source", ""),
                "published_date": article.get("published_date", ""),
                "fact_count": len(article.get("facts", [])),
            })
        return summaries


# Singleton instance
_dataset = None


def get_dataset() -> NewsDataset:
    """Get the singleton dataset instance."""
    global _dataset
    if _dataset is None:
        _dataset = NewsDataset()
    return _dataset


# ─────────────────────────────────────────────────────
# Claim Verification Against Dataset
# ─────────────────────────────────────────────────────

def _normalize(text: str) -> str:
    """Normalize text for comparison."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s.%]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text


def _compute_match_score(claim: str, fact: dict) -> float:
    """
    Compute how well a claim matches a fact.
    Returns a score from 0.0 to 1.0.
    """
    claim_norm = _normalize(claim)
    keywords = fact.get("keywords", [])
    statement_norm = _normalize(fact.get("statement", ""))

    # --- Keyword matching ---
    keyword_hits = 0
    for keyword in keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in claim_norm:
            keyword_hits += 1

    keyword_score = keyword_hits / max(len(keywords), 1)

    # --- Statement similarity (word overlap) ---
    claim_words = set(claim_norm.split())
    statement_words = set(statement_norm.split())

    # Remove common stop words
    stop_words = {
        "the", "a", "an", "is", "are", "was", "were", "in", "of", "to",
        "and", "or", "for", "on", "at", "by", "it", "that", "this",
        "with", "from", "has", "had", "have", "be", "been", "will",
    }
    claim_words -= stop_words
    statement_words -= stop_words

    if claim_words and statement_words:
        intersection = claim_words & statement_words
        union = claim_words | statement_words
        jaccard = len(intersection) / max(len(union), 1)
    else:
        jaccard = 0.0

    # --- Data point matching (numbers, names) ---
    data_points = fact.get("data_points", {})
    data_hit = False
    for key, value in data_points.items():
        val_str = str(value).lower()
        if val_str in claim_norm:
            data_hit = True
            break

    data_score = 0.3 if data_hit else 0.0

    # --- Combined score ---
    combined = (keyword_score * 0.45) + (jaccard * 0.25) + (data_score * 0.30)
    return min(combined, 1.0)


def _check_claim_contradiction(claim: str, fact: dict) -> Optional[dict]:
    """
    Check if a claim contradicts a verified fact.
    Looks for wrong numbers, wrong names, etc.
    """
    claim_norm = _normalize(claim)
    data_points = fact.get("data_points", {})

    contradictions = []

    # Check voter turnout percentage
    if "voter_turnout_percentage" in data_points:
        correct_val = data_points["voter_turnout_percentage"]
        # Find any percentage in the claim
        pct_matches = re.findall(r'(\d+\.?\d*)\s*(?:%|percent|polling)', claim_norm)
        for pct_str in pct_matches:
            try:
                claimed_val = float(pct_str)
                if abs(claimed_val - correct_val) > 0.5:  # tolerance
                    contradictions.append({
                        "field": "voter turnout percentage",
                        "claimed": f"{claimed_val}%",
                        "correct": f"{correct_val}%",
                    })
            except ValueError:
                pass

    # Check total constituencies
    if "total_constituencies" in data_points:
        correct_val = data_points["total_constituencies"]
        # Look for numbers near "constituencies"
        const_matches = re.findall(r'(\d+)\s*(?:assembly\s+)?constituencies', claim_norm)
        for val_str in const_matches:
            try:
                claimed_val = int(val_str)
                if claimed_val != correct_val:
                    contradictions.append({
                        "field": "total constituencies",
                        "claimed": str(claimed_val),
                        "correct": str(correct_val),
                    })
            except ValueError:
                pass

    # Check total voters
    if "total_voters_crore" in data_points:
        correct_val = data_points["total_voters_crore"]
        crore_matches = re.findall(r'(\d+\.?\d*)\s*crore', claim_norm)
        for val_str in crore_matches:
            try:
                claimed_val = float(val_str)
                if abs(claimed_val - correct_val) > 0.1:
                    contradictions.append({
                        "field": "total voters",
                        "claimed": f"{claimed_val} crore",
                        "correct": f"{correct_val} crore",
                    })
            except ValueError:
                pass

    # Check assembly number
    if "assembly_number" in data_points:
        correct_val = data_points["assembly_number"]
        asm_matches = re.findall(r'(\d+)(?:th|st|nd|rd)\s*(?:tamil\s*nadu\s*)?(?:legislative\s*)?assembly', claim_norm)
        for val_str in asm_matches:
            try:
                claimed_val = int(val_str)
                if claimed_val != correct_val:
                    contradictions.append({
                        "field": "assembly number",
                        "claimed": f"{claimed_val}th",
                        "correct": f"{correct_val}th",
                    })
            except ValueError:
                pass

    # Check election year
    if "election_year" in data_points:
        correct_val = data_points["election_year"]
        year_matches = re.findall(r'20\d{2}', claim_norm)
        for val_str in year_matches:
            try:
                claimed_val = int(val_str)
                if claimed_val != correct_val:
                    # Only flag if the claim is clearly about TN election
                    if "tamil" in claim_norm or "election" in claim_norm:
                        contradictions.append({
                            "field": "election year",
                            "claimed": str(claimed_val),
                            "correct": str(correct_val),
                        })
            except ValueError:
                pass

    # Check CEC name
    if "cec_name" in data_points:
        correct_name = data_points["cec_name"].lower()
        if "chief election commissioner" in claim_norm or "cec" in claim_norm:
            # Check if a different name is mentioned
            if correct_name not in claim_norm and re.search(r'[A-Z][a-z]+ [A-Z][a-z]+', claim):
                # A different name is mentioned for CEC
                name_match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+)', claim)
                if name_match:
                    claimed_name = name_match.group(1)
                    if claimed_name.lower() != correct_name:
                        contradictions.append({
                            "field": "Chief Election Commissioner",
                            "claimed": claimed_name,
                            "correct": data_points["cec_name"],
                        })

    # Check polling date
    if "polling_date" in data_points:
        correct_date = data_points["polling_date"]  # "2026-04-23"
        if "april" in claim_norm:
            day_matches = re.findall(r'april\s*(\d+)', claim_norm)
            for day_str in day_matches:
                try:
                    claimed_day = int(day_str)
                    if claimed_day != 23:
                        contradictions.append({
                            "field": "polling date",
                            "claimed": f"April {claimed_day}, 2026",
                            "correct": "April 23, 2026",
                        })
                except ValueError:
                    pass

    # Check counting date
    if "counting_date" in data_points:
        correct_date = data_points["counting_date"]  # "2026-05-04"
        if "may" in claim_norm:
            day_matches = re.findall(r'may\s*(\d+)', claim_norm)
            for day_str in day_matches:
                try:
                    claimed_day = int(day_str)
                    if claimed_day != 4:
                        contradictions.append({
                            "field": "counting date",
                            "claimed": f"May {claimed_day}, 2026",
                            "correct": "May 4, 2026",
                        })
                except ValueError:
                    pass

    # Check total polling stations
    if "total_polling_stations" in data_points:
        correct_val = data_points["total_polling_stations"]
        num_matches = re.findall(r'(\d{2,3},?\d{3})', claim_norm)
        for num_str in num_matches:
            try:
                claimed_val = int(num_str.replace(',', ''))
                if abs(claimed_val - correct_val) > 100:  # Allow small variance
                    contradictions.append({
                        "field": "total polling stations",
                        "claimed": num_str,
                        "correct": str(correct_val),
                    })
            except ValueError:
                pass

    # Check party leader
    if "party_leader" in data_points:
        correct_leader = data_points["party_leader"].lower()
        if "tvk" in claim_norm or "tamilaga vettri kazhagam" in claim_norm:
            # Check if a different leader name is mentioned
            # Extract common Tamil names or just any Capitalized sequence
            name_match = re.search(r'(?:led by|leader|chief)\s+([A-Z][a-z]+)', claim)
            if name_match:
                claimed_leader = name_match.group(1).lower()
                if claimed_leader != correct_leader:
                    contradictions.append({
                        "field": "TVK Party Leader",
                        "claimed": name_match.group(1),
                        "correct": data_points["party_leader"],
                    })

    # Check party symbol
    if "party_symbol" in data_points:
        correct_symbol = data_points["party_symbol"].lower()
        if "tvk" in claim_norm and ("symbol" in claim_norm or "allotted" in claim_norm):
            # Look for other common symbols
            other_symbols = ["leaf", "rising sun", "hand", "lotus", "cycle"]
            for s in other_symbols:
                if s in claim_norm:
                    contradictions.append({
                        "field": "TVK Party Symbol",
                        "claimed": s.title(),
                        "correct": data_points["party_symbol"],
                    })

    if contradictions:
        return {"contradictions": contradictions}
    return None


async def verify_against_dataset(claim: str) -> Optional[dict]:
    """
    Check a claim against the news facts dataset.

    Returns:
        dict with verdict, explanation, and source info if matched,
        or None if the claim doesn't match any stored facts.
    """
    dataset = get_dataset()
    all_facts = dataset.get_all_facts()

    if not all_facts:
        return None

    best_match = None
    best_score = 0.0

    for fact in all_facts:
        score = _compute_match_score(claim, fact)
        if score > best_score:
            best_score = score
            best_match = fact

    # Need at least 20% match to consider it relevant
    if best_score < 0.20 or best_match is None:
        return None

    # Check for contradictions (wrong numbers, names, etc.)
    contradiction = _check_claim_contradiction(claim, best_match)

    if contradiction:
        # The claim has WRONG information
        corrections = []
        for c in contradiction["contradictions"]:
            corrections.append(
                f"❌ {c['field'].title()}: You said \"{c['claimed']}\" — "
                f"the correct value is \"{c['correct']}\""
            )

        return {
            "verdict": "fake",
            "match_score": best_score,
            "explanation": (
                f"This claim contains incorrect information. "
                f"According to {best_match['article_source']} ({best_match['article_date']}), "
                f"the verified fact is: \"{best_match['statement']}\""
            ),
            "correct_info": "\n".join([
                "Based on our verified news dataset:",
                *corrections,
                f"\n✅ Correct fact: {best_match['statement']}",
                f"📰 Source: {best_match['article_source']} — {best_match['article_title']}",
                f"🔗 {best_match['article_url']}",
            ]),
            "sources": [
                {
                    "name": best_match["article_source"],
                    "url": best_match["article_url"],
                    "title": best_match["article_title"],
                    "rating": "Incorrect — contradicts verified data",
                    "snippet": best_match["statement"],
                }
            ],
            "matched_fact": best_match["statement"],
        }

    elif best_score >= 0.35:
        # The claim MATCHES a verified fact — it's CORRECT
        return {
            "verdict": "real",
            "match_score": best_score,
            "explanation": (
                f"This claim is verified as correct. "
                f"It matches verified data from {best_match['article_source']} ({best_match['article_date']}): "
                f"\"{best_match['statement']}\""
            ),
            "correct_info": "",
            "sources": [
                {
                    "name": best_match["article_source"],
                    "url": best_match["article_url"],
                    "title": best_match["article_title"],
                    "rating": "Verified ✅",
                    "snippet": best_match["statement"],
                }
            ],
            "matched_fact": best_match["statement"],
        }

    else:
        # Partial match but not strong enough to confirm
        return {
            "verdict": "unverified",
            "match_score": best_score,
            "explanation": (
                f"This claim is related to a known news article but could not be fully verified. "
                f"Related fact from {best_match['article_source']}: \"{best_match['statement']}\""
            ),
            "correct_info": (
                f"For accurate information, please refer to: "
                f"{best_match['article_title']} — {best_match['article_source']} ({best_match['article_url']})"
            ),
            "sources": [
                {
                    "name": best_match["article_source"],
                    "url": best_match["article_url"],
                    "title": best_match["article_title"],
                    "rating": None,
                    "snippet": best_match["statement"],
                }
            ],
            "matched_fact": best_match["statement"],
        }

# analysis/analyzer.py

import re
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from model.scoring import score_transcript

# Ensure NLTK data exists
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

DUTCH_STOP_WORDS = set(stopwords.words('dutch'))

# Fallback danger lexicon (ensures we test these even if TF/keywords are weak)
DANGER_LEXICON = [
    "mes", "bijl", "pistool", "wapen", "schoten", "schieten",
    "snijdt", "snijden", "bloed", "bloedend", "bedreigt", "bedreigen",
    "vermorden", "vermoorden", "brand", "aansteken", "steken",
    "zelfmoord", "zichzelf pijn", "zichzelf snijden", "springt", "springen"
]

def _clean_tokens(text: str):
    tokens = word_tokenize(text.lower())
    return [t for t in tokens if t.isalpha() and t not in DUTCH_STOP_WORDS]

def _candidate_bigrams(tokens, max_n=15):
    # Build bigrams from cleaned tokens (skip stopwords already removed)
    bigrams = []
    for i in range(len(tokens) - 1):
        bigrams.append(f"{tokens[i]} {tokens[i+1]}")
    # Keep unique order-preserving
    seen = set()
    out = []
    for bg in bigrams:
        if bg not in seen:
            seen.add(bg)
            out.append(bg)
    return out[:max_n]

def _regex_remove(text: str, term: str) -> str:
    """
    Remove a unigram or bigram term from text using case-insensitive
    word-boundary regex so model inputs actually change.
    """
    # For bigrams use spaces; for unigrams use \b term \b
    if " " in term:
        pattern = re.compile(rf"(?i)\b{re.escape(term)}\b")
    else:
        pattern = re.compile(rf"(?i)\b{re.escape(term)}\b")
    return re.sub(pattern, " ", text)

def run_sensitivity_analysis(transcript: str, top_n: int = 10, min_impact: float = 0.0001):
    """
    Impact-based sensitivity:
    - Build candidate terms (unigrams + bigrams) from the transcript
    - Add curated danger lexicon candidates if present in transcript
    - Remove each term and measure Δ score
    - Return top-N by absolute impact (4 decimals kept)
    """
    base = score_transcript(transcript)

    tokens = _clean_tokens(transcript)
    if not tokens:
        return []

    # candidates from transcript (unigrams + bigrams actually present)
    unigram_candidates = list(dict.fromkeys(tokens))  # unique, order-preserving
    bigram_candidates = [bg for bg in _candidate_bigrams(tokens) if bg in transcript.lower()]
    candidates = unigram_candidates + bigram_candidates

    # add danger lexicon terms that actually appear in transcript
    lower_txt = transcript.lower()
    for lex in DANGER_LEXICON:
        if lex in lower_txt and lex not in candidates:
            candidates.append(lex)

    # Evaluate impact
    results = []
    for term in candidates:
        modified = _regex_remove(transcript, term)
        new_score = score_transcript(modified)
        delta = float(new_score - base)  # keep full precision
        if abs(delta) >= min_impact:
            results.append({
                "Term": term,
                "Δ Change": round(delta, 4),
                "Color": "red" if delta < 0 else "green"
            })

    # Sort by absolute impact, top-N
    results.sort(key=lambda r: abs(r["Δ Change"]), reverse=True)
    return results[:top_n]

def plot_sensitivity_chart(results):
    if not results:
        return None
    df = pd.DataFrame(results)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='Δ Change', y='Term', hue='Color', dodge=False,
                palette={"red": "red", "green": "green"})
    plt.axvline(0, color='gray', linestyle='--', linewidth=0.8)
    plt.title('Gevoeligheidsanalyse: Impact van termen op gevaarscore')
    plt.xlabel('Verandering in gevaarscore (Δ)')
    plt.ylabel('Term')
    plt.legend(title='Effect')
    plt.tight_layout()
    return plt.gcf()

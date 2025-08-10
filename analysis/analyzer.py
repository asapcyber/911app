# analysis/analyzer.py

import re
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from model.scoring import score_transcript

# --- Stopwords: try NLTK Dutch stopwords, else fallback ---
try:
    import nltk
    from nltk.corpus import stopwords
    try:
        DUTCH_STOP_WORDS = set(stopwords.words('dutch'))
    except Exception:
        # Fallback if stopwords resource not available
        DUTCH_STOP_WORDS = set()
except Exception:
    DUTCH_STOP_WORDS = set()

# Minimal fallback list if above failed or is empty
if not DUTCH_STOP_WORDS:
    DUTCH_STOP_WORDS = {
        'de','het','een','en','of','maar','ik','jij','je','u','hij','zij','ze','wij','we','jullie',
        'mijn','jouw','zijn','haar','ons','onze','hun','dit','dat','die','deze','er','hier','daar',
        'niet','geen','wel','al','ook','nog','dan','als','om','te','van','voor','met','aan','op',
        'in','uit','bij','naar','over','onder','boven','tussen','tegen','tot','door','heen',
        'is','ben','zijn','was','waren','wordt','worden','heb','hebt','heeft','hebben','had','hadden',
        'kan','kunnen','kon','konden','zal','zullen','zou','zouden','moet','moeten'
    }

# Fallback danger lexicon to ensure critical terms are evaluated
DANGER_LEXICON = [
    "mes","bijl","pistool","wapen","schieten","schoten",
    "snijdt","snijden","snede","bloed","bloedend",
    "bedreigt","bedreigen","vermoorden","doden",
    "brand","aansteken","steken",
    "zelfmoord","zichzelf pijn","zichzelf snijden",
    "springen","springt","vluchten","gevlucht","gevaar"
]

# --- Regex-based tokenizer (no NLTK dependency) ---
# Matches words incl. accented letters (Dutch)
_WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+", re.UNICODE)

def _clean_tokens(text: str):
    tokens = _WORD_RE.findall(text.lower())
    return [t for t in tokens if t not in DUTCH_STOP_WORDS]

def _candidate_bigrams(tokens, max_n=20):
    seen = set()
    out = []
    for i in range(len(tokens) - 1):
        bg = f"{tokens[i]} {tokens[i+1]}"
        if bg not in seen:
            seen.add(bg)
            out.append(bg)
            if len(out) >= max_n:
                break
    return out

def _regex_remove(text: str, term: str) -> str:
    """
    Remove unigram/bigram using case-insensitive word-boundary regex.
    """
    pattern = re.compile(rf"(?i)\b{re.escape(term)}\b")
    return re.sub(pattern, " ", text)

def run_sensitivity_analysis(transcript: str, top_n: int = 10, min_impact: float = 0.00005):
    """
    Impact-based sensitivity:
    - Candidates = unigrams + bigrams from transcript
    - Plus danger-lexicon terms that appear in transcript
    - Remove each candidate and measure Δ score
    """
    base = score_transcript(transcript)
    tokens = _clean_tokens(transcript)

    if not tokens:
        return []

    # Build candidates from this transcript
    unigram_candidates = list(dict.fromkeys(tokens))        # unique, keep order
    bigram_candidates  = _candidate_bigrams(tokens)

    # Filter bigrams to those actually present in the text
    lower_txt = transcript.lower()
    bigram_candidates = [bg for bg in bigram_candidates if bg in lower_txt]

    candidates = unigram_candidates + bigram_candidates

    # Add danger lexicon terms present in transcript (avoid dupes)
    for lex in DANGER_LEXICON:
        if lex in lower_txt and lex not in candidates:
            candidates.append(lex)

    results = []
    for term in candidates:
        modified = _regex_remove(transcript, term)
        new_score = score_transcript(modified)
        delta = float(new_score - base)
        if abs(delta) >= min_impact:
            results.append({
                "Term": term,
                "Δ Change": round(delta, 4),
                "Color": "red" if delta < 0 else "green"
            })

    # Sort by absolute impact
    results.sort(key=lambda r: abs(r["Δ Change"]), reverse=True)
    return results[:top_n]

def plot_sensitivity_chart(results):
    if not results:
        return None

    df = pd.DataFrame(results)
    fig = plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='Δ Change', y='Term', hue='Color', dodge=False,
                palette={"red": "red", "green": "green"})
    plt.axvline(0, color='gray', linestyle='--', linewidth=0.8)
    plt.title('Gevoeligheidsanalyse: Impact van termen op gevaarscore')
    plt.xlabel('Verandering in gevaarscore (Δ)')
    plt.ylabel('Term')
    plt.legend(title='Effect')
    plt.tight_layout()
    return fig

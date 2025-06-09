import re
from typing import List, Dict

def danger_score(transcript: str) -> float:
    """
    Computes a risk score based on danger-related keywords.
    """
    score = 0
    features = {
        'knife': 0.2,
        'cutting herself': 0.2,
        'stab': 0.2,
        'flee': 0.15,
        'run': 0.1,
        'police': 0.05,
        'abused': 0.05,
        'crazy': 0.05,
        'dangerous': 0.05
    }
    transcript_lower = transcript.lower()
    for keyword, weight in features.items():
        if keyword in transcript_lower:
            score += weight
    return min(score, 1.0)

def run_sensitivity_analysis(transcript: str) -> List[Dict[str, str]]:
    """
    Simulates modified scenarios by removing or changing certain phrases in the transcript.
    Returns the resulting changes in the danger score.
    """
    base_score = danger_score(transcript)
    variants = [
        ("Remove 'knife'", re.sub(r'knife', '', transcript, flags=re.I)),
        ("Caller does not flee", re.sub(r'run|flee', '', transcript, flags=re.I)),
        ("Remove past police visits", re.sub(r'police.*?times', '', transcript, flags=re.I)),
        ("Remove 'stab me'", re.sub(r'stab.*', '', transcript, flags=re.I)),
        ("Calm tone, no panic", re.sub(r'i have to run.*', '', transcript, flags=re.I)),
        ("Change 'cutting herself' to 'yelling loudly'", re.sub(r'cutting herself', 'yelling loudly', transcript, flags=re.I))
    ]
    results = []
    for label, mod_text in variants:
        score = danger_score(mod_text)
        results.append({
            'Scenario': label,
            'Danger Score': round(score, 2),
            'Δ Change': round(score - base_score, 2)
        })
    return results


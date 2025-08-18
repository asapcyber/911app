def danger_score(transcript: str) -> float:
    """
    Heuristic fallback danger score based on keyword weights.
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

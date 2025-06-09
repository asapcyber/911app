from analysis.analyzer import danger_score
from typing import List

def generate_worst_case_scenario(transcript: str) -> str:
    if 'knife' in transcript.lower() or 'cutting herself' in transcript.lower():
        return (
            "If first responders underestimate the threat or fail to de-escalate, "
            "the subject may brandish the knife, leading to a fatal encounter. "
            "This could result in the subject being shot by police to protect themselves or others. "
            "Key contributing factors: prior violent history, caller has fled, emotional instability, presence of a weapon."
        )
    else:
        return (
            "If response is delayed or poorly coordinated, the subject may harm themselves severely. "
            "Risk increases in absence of mental health professionals or if escalation is ignored."
        )

def generate_branching_scenarios(transcript: str) -> List[str]:
    score = danger_score(transcript)
    base_paths = [
        ("🚔 Police arrive and de-escalate: Subject surrenders.", 0.2),
        ("🧠 Crisis team intervenes: Subject hospitalized.", 0.2),
        ("⚠️ Police enter blindly: Subject charges, force used.", 0.2),
        ("🕰️ Delay: Subject harms self before help arrives.", 0.2),
        ("👩‍👧 Family intervenes: Situation de-escalates or worsens.", 0.2)
    ]
    adjusted = [(desc, round(prob * (1 + score), 2)) for desc, prob in base_paths]
    total = sum(prob for _, prob in adjusted)
    normalized = [(desc, round(prob / total, 2)) for desc, prob in adjusted]
    return [f"{desc} (Est. Prob: {prob})" for desc, prob in normalized]

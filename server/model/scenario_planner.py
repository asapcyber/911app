from model.scoring import score_transcript
from model.fallback import danger_score as fallback_score
from typing import List

def generate_worst_case_scenario(transcript: str) -> str:
    """
    Describes the worst plausible outcome based on ML danger score and known risk cues.
    """
    score = 0.0
    try:
        score = score_transcript(transcript)
    except:
        score = fallback_score(transcript)

    has_weapon = 'knife' in transcript.lower() or 'stab' in transcript.lower()
    has_self_harm = 'cutting herself' in transcript.lower()
    has_history = 'police' in transcript.lower() or 'abused' in transcript.lower()

    if score > 0.7 and has_weapon:
        return (
            "High likelihood of violent escalation. Subject may threaten or attack responders. "
            "Police may be forced to use lethal force if de-escalation fails. "
            "Contributing risk factors: weapon present, fleeing caller, volatile language, past incidents."
        )
    elif has_self_harm:
        return (
            "Subject may continue self-harming or attempt suicide if left alone. "
            "Delays in response or misjudgment of risk could result in severe injury or death. "
            "Mental health crisis team needed urgently."
        )
    else:
        return (
            "Situation may de-escalate, but risk remains due to unstable behavior. "
            "Without immediate intervention, incident could deteriorate rapidly."
        )


def generate_branching_scenarios(transcript: str) -> List[str]:
    """
    Provides alternative outcome paths with estimated probabilities adjusted by danger score.
    """
    try:
        score = score_transcript(transcript)
    except:
        score = fallback_score(transcript)

    base_paths = [
        ("🚔 Police arrive and de-escalate: Subject cooperates peacefully.", 0.2),
        ("🧠 Crisis team intervenes: Subject stabilized and hospitalized.", 0.2),
        ("⚠️ Subject attacks with weapon: Use of force required.", 0.2),
        ("⏳ Delay in response: Subject harms self or others.", 0.2),
        ("👤 Family member intervenes: De-escalation succeeds or escalates.", 0.2),
    ]

    # Danger score adjusts perceived probabilities
    adjusted_paths = [(desc, round(prob * (1 + score), 2)) for desc, prob in base_paths]
    total = sum(prob for _, prob in adjusted_paths)
    normalized = [(desc, round(prob / total, 2)) for desc, prob in adjusted_paths]

    return [f"{desc} (Est. Prob: {prob})" for desc, prob in normalized]


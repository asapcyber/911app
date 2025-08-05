from analysis.analyzer import run_sensitivity_analysis
from model.scoring import score_transcript

def generate_incident_card(transcript: str) -> str:
    # Get danger score and sensitivity analysis
    score = score_transcript(transcript)
    analysis = run_sensitivity_analysis(transcript)

    bullet_points = "".join(
        f"<li>{item['Scenario']}: Δ {item['Δ Change']}</li>"
        for item in analysis
    )

    html = f"""
    <div style='font-family: Arial, sans-serif; padding: 10px; border: 1px solid #ccc;'>
        <h2>📟 Incident Card</h2>
        <p><strong>📞 Transcript:</strong> {transcript}</p>
        <p><strong>🔥 Danger Score:</strong> {score:.2f}</p>
        <p><strong>🔍 Top Risk Factors:</strong></p>
        <ul>
            {bullet_points}
        </ul>
        <p><strong>🚨 Use this card to guide first responder decisions based on ML-derived risk.</strong></p>
    </div>
    """
    return html

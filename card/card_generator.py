# card/card_generator.py

from analysis.analyzer import run_sensitivity_analysis
from model.scoring import score_transcript
from analysis.sentiment_module import sentiment_analysis

def generate_incident_card(transcript: str) -> str:
    score = score_transcript(transcript)
    analysis = run_sensitivity_analysis(transcript)
    sentiment_df, _ = sentiment_analysis(transcript)

    bullet_points = ""
    for item in analysis:
        bullet_points += f"<li>{item['Scenario']}: Δ {item['Δ Change']}</li>"

    sentiment_html = sentiment_df.to_html(index=False)

    html = f"""
    <div style="border:2px solid #444;padding:20px;border-radius:10px;">
        <h2>🧾 Incident Kaart</h2>
        <p><strong>📍 Transcript samenvatting:</strong></p>
        <p style="background-color:#f0f0f0;padding:10px;border-radius:5px;">{transcript}</p>

        <p><strong>🔥 Gevaar Score:</strong> {score:.2f} (0 = Laag, 1 = Hoog)</p>

        <p><strong>🧠 Gevoelige termen:</strong></p>
        <ul>{bullet_points}</ul>

        <p><strong>😊 Sentiment Analyse:</strong></p>
        {sentiment_html}
    </div>
    """
    return html

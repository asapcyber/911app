# card/card_generator.py

from analysis.analyzer import run_sensitivity_analysis
from analysis.sentiment_module import sentiment_analysis
from model.scoring import score_transcript

def generate_incident_card(transcript: str) -> str:
    score = score_transcript(transcript)
    analysis = run_sensitivity_analysis(transcript)
    sentiment_df, _ = sentiment_analysis(transcript)

    bullet_points = ""
    if analysis:
        bullet_points = "".join(
            f"<li>{item['Scenario']}: Δ {item['Δ Change']}</li>"
            for item in analysis
        )

    sentiment_table = ""
    if not sentiment_df.empty:
        sentiment_table = sentiment_df.to_html(index=False)

    html = f"""
    <div style="border:1px solid #ccc; padding:20px; border-radius:10px;">
        <h3>📝 Incidentkaart</h3>
        <p><strong>🔥 Gevaar Score:</strong> {score:.2f} (0 = Laag, 1 = Hoog)</p>

        <p><strong>🧠 Gevoelige termen:</strong></p>
        <ul>{bullet_points}</ul>

        <p><strong>😊 Sentiment Analyse:</strong></p>
        {sentiment_table}
    </div>
    """

    return html

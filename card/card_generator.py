from analysis.analyzer import run_sensitivity_analysis
from model.scenario_planner import generate_worst_case_scenario, generate_branching_scenarios

try:
    from model.scoring import score_transcript
except ImportError:
    from model.fallback import danger_score as score_transcript


def generate_incident_card(transcript: str) -> str:
    score = score_transcript(transcript)
    analysis = run_sensitivity_analysis(transcript)
    scenario = generate_worst_case_scenario(transcript)
    bullet_points = "".join(
        f"<li>{item['Scenario']}: Score = {item['Danger Score']} (Δ {item['Δ Change']})</li>"
        for item in analysis
    )
    branches = generate_branching_scenarios(transcript)
    branch_points = "".join(f"<li>{b}</li>" for b in branches)
    card_html = f"""
    <html><body>
    <h2>🚨 911 Incident Risk Card</h2>
    <p><strong>Danger Score:</strong> {score:.2f} / 1.0</p>
    <h3>📋 Key Risk Indicators (Inferred)</h3>
    <ul>
        <li>ML-based scoring model used</li>
        <li>Dynamic risk sensitivity simulated</li>
        <li>Historical incident trends applied</li>
    </ul>
    <h3>📊 Sensitivity Analysis</h3>
    <ul>{bullet_points}</ul>
    <h3>🚨 Worst-Case Scenario</h3>
    <p>{scenario}</p>
    <h3>🔀 Branching Scenarios</h3>
    <ul>{branch_points}</ul>
    <h3>✅ Recommended Actions</h3>
    <ul>
        <li>Dispatch multiple units</li>
        <li>Send mental health crisis support</li>
        <li>Maintain safe perimeter</li>
        <li>Attempt remote contact</li>
        <li>Coordinate with caller’s family (with caution)</li>
    </ul>
    </body></html>
    """
    return card_html

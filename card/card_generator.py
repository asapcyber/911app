from analysis.analyzer import danger_score, run_sensitivity_analysis
from model.scenario_planner import generate_worst_case_scenario, generate_branching_scenarios

def generate_incident_card(transcript: str) -> str:
    score = danger_score(transcript)
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
    <p><strong>Danger Score:</strong> {score} / 1.0</p>
    <h3>📋 Key Risk Indicators</h3>
    <ul>
        <li>Weapon involved (if reported)</li>
        <li>Self-harm or harm to others</li>
        <li>Emotional volatility</li>
        <li>Caller fled the scene</li>
        <li>History of police contact</li>
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
        <li>Include mental health crisis team</li>
        <li>Attempt de-escalation via remote contact</li>
        <li>Coordinate with any known family member cautiously</li>
        <li>Maintain safe perimeter</li>
    </ul>
    </body></html>
    """
    return card_html


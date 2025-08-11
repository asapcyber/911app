# 911 Analyzer app
Developed to assist law enforecement and first responders in assessing level of danger to be expected in response to a 911 call.

## Structure
The app consists of the following:

- ML Trained Danger Scoring model
- Scoring engine
- MCP server connection to GenAI platform
- reporting outputs

## Key Tech Stack Components
The initial app is built on a lightweight tech stack to allow for quick iterations and demonstrate the concepts.
In order to fully develop the app a more robust tech stack will need to be leveraged and the app will be transitioned to it once approved.
- Node.js
- SQLite
- Python
- Vite/Tailwind
- React UI
- Streamlit Cloud for prototype
- Custom MCP Server for OpenAI

## Intended use
The app is designed to leverage a "dange scoring" model trained with past 911 call data, in order to "score" an incoming call for potential danger to/for first-responders.
With a realtime integration to the OpenAI ChatGPT agent, users can request real-time recommendations on how to handle the 911 incident.

## Features backlog
Once the bseline product is working as designed and the scoring model is considered robust, additional features can be added, like:
- Incident Report Card (for a quick reference to summarize call analysis)
- Sentiment Analysis (to support danger score and provide first-responders with estimate of emotional state of 911 caller)
- Scenario simulator (to simulate possible ways the 911 response could develop and how to avoid worst-case)
- Recommend next best actions (NBA)
- Mental health support requester

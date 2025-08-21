# 112 Analyzer — Emergency Transcript Scoring & MCP Agent

A modern, full-stack application for analyzing **112 emergency transcripts** with:
- ML-based **danger score** (0–1) trained on simulated Dutch 112 calls  
- **Sensitivity analysis** (which terms influence the score, and by how much)  
- **Emotion/Sentiment analysis** + radar visualization  
- **Map view** (default location + user-supplied lat/lon)  
- **Next-Best Actions** (recommended dispatcher responses)  
- **MCP Agent** (OpenAI-powered) for contextual Q&A about the incident  
- **Admin Panel** for live retraining of the ML danger model  

> ⚠️ Disclaimer: This app is a **prototype** and for demonstration purposes only. The danger score and MCP responses are **supportive tools, not authoritative**. Always require human evaluation.

---

## Table of Contents
- [Architecture](#architecture)  
- [Repository Structure](#repository-structure)  
- [Requirements](#requirements)  
- [Quick Start (Local)](#quick-start-local)  
- [Backend (FastAPI)](#backend-fastapi)  
- [Frontend (React + Vite + Tailwind)](#frontend-react--vite--tailwind)  
- [ML Training & Database](#ml-training--database)  
- [MCP Agent](#mcp-agent)  
- [Deployment (Render)](#deployment-render)  
- [API Endpoints](#api-endpoints)  
- [Environment Variables](#environment-variables)  
- [Troubleshooting](#troubleshooting)  
- [Security & Disclaimer](#security--disclaimer)  
- [License](#license)  

---

## Architecture
```text
Frontend (React + Vite + Tailwind)
│ - Transcript analysis (danger score, sensitivity, radar, map)
│ - MCP Agent tab
│ - Admin (retrain model)
│
└──→ Backend (FastAPI)
│ /api/score -> ML danger score
│ /api/sensitivity -> Sensitivity analysis
│ /api/analyze -> Score + sensitivity combined
│ /api/sentiment -> Emotion radar
│ /api/recommend -> Next-best actions
│ /mcp/query, /mcp/reset -> OpenAI MCP Agent
│
└──→ ML model (.pkl joblib, Dutch vectorizer)
```
---

## Repository Structure
```text
.
├─ server/
│ ├─ main.py # FastAPI app (API + MCP Agent)
│ ├─ analysis/
│ │ └─ analyzer.py # Sensitivity analysis + keyword impact
│ ├─ model/
│ │ ├─ scoring.py # Loads ML model, computes danger score
│ │ ├─ training.py # Retraining helpers
│ │ └─ train_pipeline.py # Full training pipeline
│ └─ .nltk_data/ # Pre-bundled NLTK data (punkt, stopwords)
│
├─ frontend/
│ ├─ src/
│ │ ├─ routes/ # TranscriptPage.tsx, McpAgentPage.tsx
│ │ ├─ components/ # GaugeCard, MapCard, SensitivityBar
│ │ ├─ lib/ # API + MCP helpers
│ │ └─ state/ # Zustand store
│ └─ public/ # Logo, favicon
│
├─ requirements.txt # Python dependencies
├─ package.json # Frontend dependencies
└─ README.md # This file
```

---

## Requirements
- **Python** 3.11  
- **Node.js** 20.x  
- **OpenAI API key** (required for MCP Agent)  

---

## Quick Start (Local)

### Backend
```bash
cd server
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r ../requirements.txt

# Configure env vars
cp .env.example .env
# Add your OPENAI_API_KEY

# Run backend
uvicorn main:app --reload --port 8000
# Health check
curl http://localhost:8000/health
```
---

### Frontend
```bash
cd frontend
npm ci
npm run dev

# Environment (frontend/.env.local)
VITE_API_BASE=http://localhost:8000
VITE_MCP_BASE=http://localhost:8000

# Open in browser
http://localhost:5173

```
---

## Backend (FastAPI)
- **NLTK**: packaged with `.nltk_data` so no runtime download needed.  
- **Matplotlib**: used for local sensitivity plots.  
- **CORS**: configured via `FRONTEND_ORIGIN` env var.

---

## Frontend (React + Vite + Tailwind)
- **GaugeCard**: circular gauge with dynamic color (green → red).
- **MapCard**: Leaflet map with default location (Amsterdam) until user enters coordinates.  
- **SensitivityBar**: highlights most impactful keywords.

---

## ML Training & Database
- **Pipeline**: `train_pipeline.py` trains TF-IDF vectorizer + classifier.
- **Danger Score**: computed by `scoring.py`.  
- **Sensitivity**: `analyzer.py` perturbs words, recomputes Δ-score.

---

## MCP Agent
- Endpoints: 
    - `POST /mcp/query` → contextual Q&A with OpenAI.
    - `POST /mcp/reset` → resets session.
- Compatible with **Responses** API and fallback to **Chat Completions API**.  

---

## Deployment (Render)
### Backend (Web Service)
- **Root**: `server/` 
- **Build Command**:  
```bash
pip install -r requirements.txt
```
- **Start Command**:  
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```
- **Env vars**:
    - `OPENAI_API_KEY`
    - `OPENAI_MODEL=gpt-4o-mini`
    - `FRONTEND_ORIGIN=https://<frontend-url>`
    - `PYTHONPATH=/opt/render/project/src/server`

### Frontend (Static Site)
- **Root**: `frontend/` 
- **Build Command**:  
```bash
npm ci && npm run build
```
- **Publish Directory**: `dist/`
- **Env Vars**:
    - `VITE_API_BASE=https://<backend-url>`
    - `VITE_MCP_BASE=https://<backend-url>`

---

## API Endpoints
```bash
GET  /health
POST /api/score           { transcript }
POST /api/sensitivity     { transcript, top_n? }
POST /api/analyze         { transcript, top_n? }
POST /api/sentiment       { transcript }
POST /api/recommend       { transcript, score }
POST /mcp/query           { session_id, query, context? }
POST /mcp/reset           { session_id }

```
## Environment Variables
### Backend (.env)
```bash
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
FRONTEND_ORIGIN=http://localhost:5173
NLTK_DATA=server/.nltk_data
```
### Frontend (.env.local)
```bash
VITE_API_BASE=http://localhost:8000
VITE_MCP_BASE=http://localhost:8000

```
---

## Troubelshooting
- **Frontend “Analyze” does nothing**:
    Check browser console & network tab → API calls should hit `/api/analyze`.
- **ModuleNotFoundError: analysis:**:
    Ensure `analysis/` and `model/` dirs exist under `server/`.
- `'OpenAI' object has no attribute 'responses'`:
    Fixed in MCP agent fallback → ensure openai>=1.0.0.
- **NLTK Errors**:
    Bundle data under `server/.nltk_data`.

---

## Security & Disclaimer
> [!WARNING]
> This project is a **prototype**. Danger scoring, sensitivity, and MCP responses are experimental.
Do not use in production emergency systems. Always require human review.

---

## License
© 2025 — asapcyber
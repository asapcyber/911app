# server/main.py
# server/main.py
from __future__ import annotations

import os
import time
import json
import asyncio
import logging
from collections import defaultdict, deque
from typing import Deque, Tuple, List, Dict, Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ---- Load env early ----
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1")  # Responses-capable model (e.g., gpt-4.1, gpt-4o-mini)

# ---- Logging ----
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---- Third-party clients ----
try:
    from openai import OpenAI
except Exception as e:
    OpenAI = None
    logger.error("OpenAI SDK not available: %s", e)

client = OpenAI(api_key=OPENAI_API_KEY) if (OpenAI and OPENAI_API_KEY) else None

# ---- Local ML imports ----
# These should exist in your repo:
#   model/scoring.py  -> score_transcript(text) -> float in [0,1]
#   analysis/analyzer.py -> run_sensitivity_analysis(text, top_n=10) -> list of dicts ({Term, delta, ...})
try:
    from model.scoring import score_transcript
except Exception as e:
    logger.exception("Failed to import model.scoring.score_transcript: %s", e)
    def score_transcript(text: str) -> float:
        raise RuntimeError("score_transcript import failed; check server logs.")

try:
    from analysis.analyzer import run_sensitivity_analysis
except Exception as e:
    logger.exception("Failed to import analysis.analyzer.run_sensitivity_analysis: %s", e)
    def run_sensitivity_analysis(text: str, top_n: int = 10) -> List[Dict[str, Any]]:
        raise RuntimeError("run_sensitivity_analysis import failed; check server logs.")

# =============================================================================
# FastAPI app
# =============================================================================
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN] if FRONTEND_ORIGIN != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app = FastAPI(title="112 Analyzer API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# Schemas
# =============================================================================
class ScoreRequest(BaseModel):
    transcript: str = Field(..., min_length=3)

class ScoreResponse(BaseModel):
    score: float

class SensitivityRequest(BaseModel):
    transcript: str = Field(..., min_length=3)
    top_n: int = Field(10, ge=1, le=30)

class SensitivityResponse(BaseModel):
    results: List[Dict[str, Any]]

class AnalyzeRequest(BaseModel):
    transcript: str = Field(..., min_length=3)
    top_n: int = Field(10, ge=1, le=30)

class AnalyzeResponse(BaseModel):
    score: float
    results: List[Dict[str, Any]]

# =============================================================================
# Health
# =============================================================================
@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": bool(client), "ml_imports_ok": score_transcript is not None}

# =============================================================================
# ML endpoints
# =============================================================================
@app.post("/api/score", response_model=ScoreResponse)
async def api_score(req: ScoreRequest):
    t0 = time.perf_counter()
    try:
        s = await asyncio.to_thread(score_transcript, req.transcript)
        s = max(0.0, min(1.0, float(s)))
        return {"score": round(s, 4)}
    except Exception as e:
        logger.exception("/api/score failed: %s", e)
        raise HTTPException(status_code=500, detail=f"scoring failed: {e}")
    finally:
        logger.info("/api/score completed in %.1f ms", (time.perf_counter() - t0) * 1000)

@app.post("/api/sensitivity", response_model=SensitivityResponse)
async def api_sensitivity(req: SensitivityRequest):
    t0 = time.perf_counter()
    try:
        top = min(req.top_n, 20)
        rows = await asyncio.to_thread(run_sensitivity_analysis, req.transcript, top)
        # Normalize keys for the frontend
        out = []
        for r in rows or []:
            term = r.get("Term") or r.get("term") or r.get("Scenario") or ""
            delta = r.get("Δ Change", r.get("delta", 0.0))
            try:
                delta = float(delta)
            except Exception:
                delta = 0.0
            out.append({
                "Term": term,
                "delta": round(delta, 6),
                "Δ Change": round(delta, 6),
                "Color": r.get("Color", "green"),
            })
        return {"results": out}
    except Exception as e:
        logger.exception("/api/sensitivity failed: %s", e)
        raise HTTPException(status_code=500, detail=f"sensitivity failed: {e}")
    finally:
        logger.info("/api/sensitivity completed in %.1f ms", (time.perf_counter() - t0) * 1000)

@app.post("/api/analyze", response_model=AnalyzeResponse)
async def api_analyze(req: AnalyzeRequest):
    t0 = time.perf_counter()
    try:
        s = await asyncio.to_thread(score_transcript, req.transcript)
        s = max(0.0, min(1.0, float(s)))
        top = min(req.top_n, 20)
        rows = await asyncio.to_thread(run_sensitivity_analysis, req.transcript, top)
        # normalize result terms
        norm = []
        for r in rows or []:
            term = r.get("Term") or r.get("term") or r.get("Scenario") or ""
            delta = r.get("Δ Change", r.get("delta", 0.0))
            try:
                delta = float(delta)
            except Exception:
                delta = 0.0
            norm.append({"Term": term, "delta": round(delta, 6)})
        return {"score": round(s, 4), "results": norm}
    except Exception as e:
        logger.exception("/api/analyze failed: %s", e)
        raise HTTPException(status_code=500, detail=f"analyze failed: {e}")
    finally:
        logger.info("/api/analyze completed in %.1f ms", (time.perf_counter() - t0) * 1000)

# --- Sentiment & Recommendations (Nederlands) -------------------------------
import re
from typing import Dict, List
from fastapi import HTTPException

class SentimentRequest(BaseModel):
    transcript: str = Field(..., min_length=3)

class SentimentResponse(BaseModel):
    emotions: Dict[str, float]  # bv {"angst":0.7, "boosheid":0.6, ...}

EMO_LEX = {
    "angst": ["bang", "angstig", "vrees", "paniek", "gevaar", "ik moet vluchten", "help", "hulp"],
    "boosheid": ["boos", "woedend", "schreeuwt", "bedreigt", "agressief", "aanvalt", "geweld"],
    "verdriet": ["huilen", "verdriet", "pijn", "gewond", "gewond", "gewond geraakt"],
    "urgentie": ["nu", "meteen", "dringend", "spoed", "snel", "direct"],
    "wanhoop": ["ik kan niet", "het gaat mis", "red me", "wanhopig", "ik ben bang", "ik moet weg"],
}

def _score_emotions_nl(text: str) -> Dict[str, float]:
    t = text.lower()
    out: Dict[str, float] = {}
    total_hits = 0
    raw = {}
    for emo, terms in EMO_LEX.items():
        c = 0
        for kw in terms:
            c += len(re.findall(r"\b" + re.escape(kw) + r"\b", t))
        raw[emo] = c
        total_hits += c
    # normaliseer tot 0..1 (robust)
    denom = max(1, total_hits)
    for emo, c in raw.items():
        out[emo] = round(c / denom, 4)
    return out

@app.post("/api/sentiment", response_model=SentimentResponse)
async def api_sentiment(req: SentimentRequest):
    try:
        emo = await asyncio.to_thread(_score_emotions_nl, req.transcript)
        return {"emotions": emo}
    except Exception as e:
        logger.exception("/api/sentiment failed: %s", e)
        raise HTTPException(status_code=500, detail=f"sentiment failed: {e}")

class RecommendRequest(BaseModel):
    transcript: str = Field(..., min_length=3)
    score: float = Field(..., ge=0.0, le=1.0)

class RecommendResponse(BaseModel):
    actions: List[str]

WEAPON_TERMS = ["mes", "pistool", "geweer", "hamer", "fles", "machete", "bijl"]
SELF_HARM_TERMS = ["snijdt zichzelf", "zelfmoord", "ik doe mezelf pijn", "ik ga mezelf pijn doen", "ik ga mezelf iets aandoen"]

def _recommend_actions(text: str, score: float) -> List[str]:
    t = text.lower()
    has_weapon = any(w in t for w in WEAPON_TERMS)
    self_harm = any(s in t for s in SELF_HARM_TERMS)
    high = score >= 0.7
    med  = 0.4 <= score < 0.7

    actions: List[str] = []
    # Altijd:
    actions.append("Beoordeel veiligheid ter plekke; houd veilige afstand en creëer perimeters.")
    actions.append("Maak contact op afstand (porto/telefoon), spreek rustig en duidelijk.")
    # Score-gedreven:
    if high:
        actions.append("Stuur extra eenheid + ambulance stand-by; informeer ter plaatse over mogelijke escalatie.")
    elif med:
        actions.append("Plan de-escalatie met twee-eenheden-benadering; ambulance op afroep.")
    else:
        actions.append("Voer rustige de-escalatie; monitor laagschalig maar alert.")

    # Wapen aanwezig
    if has_weapon:
        actions.append("Wapenprotocol: geen plotselinge bewegingen; Taser/pepperspray conform richtlijnen gereed.")
        actions.append("Vermijd binnentreden zonder overzicht; gebruik beschutting en licht/geluid aan/uit beleid.")
    # Zelfbeschadiging
    if self_harm:
        actions.append("Schakel crisisdienst/psycholance; focus op verbale de-escalatie en veiligheidsafspraken.")
        actions.append("Verwijder scherpe voorwerpen uit bereik zodra veilig mogelijk.")
    # Check derden
    actions.append("Verifieer aanwezigheid van derden (kinderen/omstanders) en evacueer zo nodig.")
    # Info
    actions.append("Vraag: middelengebruik, eerdere incidenten, medische/psychiatrische voorgeschiedenis, beschermingsmaatregelen.")
    return actions

@app.post("/api/recommend", response_model=RecommendResponse)
async def api_recommend(req: RecommendRequest):
    try:
        acts = await asyncio.to_thread(_recommend_actions, req.transcript, float(req.score))
        return {"actions": acts}
    except Exception as e:
        logger.exception("/api/recommend failed: %s", e)
        raise HTTPException(status_code=500, detail=f"recommend failed: {e}")



# =============================================================================
# MCP Agent (Responses API only, with session memory)
# =============================================================================
# Lightweight in-memory chat store: session_id -> last 20 messages (role, text)
CHAT_SESSIONS: dict[str, Deque[Tuple[str, str]]] = defaultdict(lambda: deque(maxlen=20))

class MCPChatQuery(BaseModel):
    session_id: str = Field(..., min_length=3)
    query: str = Field(..., min_length=2)
    context: str = Field("", description="112-transcript of samenvatting")

class MCPAnswer(BaseModel):
    response: str

SYSTEM_DUTCH = (
    "Je bent een 112-hulpagent voor Nederland. "
    "Geef kort, handelingsgericht advies voor politie en eerstehulpdiensten. "
    "Gebruik bondige bullets, benoem veiligheid eerst, maak aannames expliciet. "
    "Als informatie ontbreekt, geef duidelijke vragen/checks. "
    "Vermijd juridisch bindende claims. Antwoord in het Nederlands."
)

def _prompt_with_history(session_id: str, q: str, ctx: str) -> List[Dict[str, str]]:
    """
    Build a Responses-API style 'input' list with roles.
    We keep a system message and then a single user content that includes short history + context + question.
    """
    hist = CHAT_SESSIONS.get(session_id, deque())
    lines = []
    for role, msg in hist:
        prefix = "Gebruiker" if role == "user" else "Agent"
        lines.append(f"- {prefix}: {msg}")
    hist_block = "\n".join(lines) if lines else "— (geen eerdere berichten) —"

    user_payload = (
        f"GESPREK HISTORIE (laatste {len(hist)}):\n{hist_block}\n\n"
        f"112 CONTEXT:\n{ctx.strip() or '(leeg)'}\n\n"
        f"VRAAG:\n{q.strip()}\n\n"
        f"Geef beknopt, praktisch en veiligheidsgericht advies in bullets."
    )

    return [
        {"role": "system", "content": SYSTEM_DUTCH},
        {"role": "user", "content": user_payload},
    ]

def _extract_responses_text(resp) -> str:
    """
    Robustly extract plain text from Responses API object across SDK/model variations.
    """
    # Preferred helper in newer SDKs
    text = (getattr(resp, "output_text", "") or "").strip()
    if text:
        return text

    # Fallback: walk structured 'output'
    out = getattr(resp, "output", None)
    if out:
        chunks = []
        for item in out:
            content_list = getattr(item, "content", None) or []
            for c in content_list:
                # c may be an object or a dict depending on SDK
                ctype = getattr(c, "type", None) or (isinstance(c, dict) and c.get("type"))
                if ctype in ("text", "output_text"):
                    ctext = getattr(c, "text", None) or (isinstance(c, dict) and c.get("text")) or ""
                    if ctext:
                        chunks.append(ctext)
        if chunks:
            return "\n".join(chunks).strip()

    # Another fallback (some SDKs): top-level 'content'
    top = getattr(resp, "content", None)
    if isinstance(top, list):
        parts = []
        for c in top:
            if isinstance(c, dict) and c.get("type") in ("text", "output_text") and c.get("text"):
                parts.append(c["text"])
        if parts:
            return "\n".join(parts).strip()

    return ""

@app.post("/mcp/query", response_model=MCPAnswer)
async def mcp_query(payload: MCPChatQuery = Body(...)):
    if not client or not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY ontbreekt op de server.")

    # Build Responses-API input (role-based) with compact history
    input_messages = _prompt_with_history(payload.session_id, payload.query, payload.context)

    t0 = time.perf_counter()
    try:
        def _call():
            # Responses API — no `response_format` in your SDK version
            return client.with_options(timeout=20).responses.create(
                model=OPENAI_MODEL,
                input=input_messages,      # role/content list
                max_output_tokens=400,     # correct param for Responses API
            )
        resp = await asyncio.to_thread(_call)

        # Light introspection for debugging shapes
        try:
            logger.info("MCP Responses model: %s", getattr(resp, "model", None))
            if hasattr(resp, "__dict__"):
                logger.info("MCP Responses keys: %s", list(resp.__dict__.keys()))
        except Exception:
            pass

        text = _extract_responses_text(resp)
        if not text:
            # Log a truncated JSON dump if available
            try:
                raw_json = getattr(resp, "model_dump_json", None)
                if callable(raw_json):
                    dumped = raw_json()
                    logger.warning("MCP empty text; raw json (truncated): %s", dumped[:1500])
            except Exception:
                logger.warning("MCP empty text; resp type=%s", type(resp))
            raise HTTPException(status_code=502, detail="MCP agent: leeg antwoord ontvangen van de model-API.")

        # Update session history
        CHAT_SESSIONS[payload.session_id].append(("user", payload.query))
        CHAT_SESSIONS[payload.session_id].append(("assistant", text))

        return {"response": text}

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("MCP query failed")
        raise HTTPException(status_code=500, detail=f"MCP agent: onverwachte fout: {e}")
    finally:
        logger.info("/mcp/query completed in %.1f ms", (time.perf_counter() - t0) * 1000)

class ResetReq(BaseModel):
    session_id: str

@app.post("/mcp/reset")
def mcp_reset(req: ResetReq):
    CHAT_SESSIONS.pop(req.session_id, None)
    return {"ok": True}

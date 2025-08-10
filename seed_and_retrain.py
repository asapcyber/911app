"""
Seed the database with Dutch 112 transcripts (20 high-risk, 20 low-risk)
and retrain the danger-scoring model.

Run:
    python scripts/seed_and_retrain.py
"""

import datetime
import random
import sys

# --- Adjust imports to your project structure ---
try:
    from model.db import SessionLocal
    from model.models import CallRecord
except Exception as e:
    print("❌ Could not import DB models. Are you running from the repo root?")
    print("   Expected: model/db.py and model/models.py to be importable.")
    raise

# Try both training entry points (use whichever your project has)
TRAIN_FN = None
try:
    from model.train_pipeline import train_model_from_db as TRAIN_FN
except Exception:
    try:
        from model.training import retrain_model_from_db as TRAIN_FN
    except Exception:
        TRAIN_FN = None


# ---------------------------
# Seed data (Dutch, diverse)
# ---------------------------

HIGH_RISK = [
    "Mijn partner bedreigt mij met een mes. Ik ben bang voor mijn leven.",
    "Er is een man in mijn huis met een pistool. Ik verstop me in de kast.",
    "Ze schreeuwt en slaat dingen stuk. Ze heeft zichzelf gesneden.",
    "Hij zegt dat hij me gaat vermoorden als ik de politie bel.",
    "Ze heeft brand gesticht in de keuken na een ruzie.",
    "Hij sloeg me voor mijn kinderen. Ze huilen allemaal.",
    "Er ligt een bebloede vrouw buiten op straat. Ze ademt amper.",
    "Mijn buurman dreigt met een wapen. Iedereen is in paniek.",
    "Ze heeft een mes tegen haar eigen keel gehouden.",
    "Er is iemand met een bijl die probeert de deur in te slaan.",
    "Hij sloeg met een stok op de hond en daarna op mij.",
    "Ze dreigt de kinderen iets aan te doen als ik niet luister.",
    "Hij zegt dat hij zichzelf van het leven gaat beroven.",
    "Ze is agressief en onder invloed, ze sloeg me met een pan.",
    "Er is een overval gaande bij de supermarkt, ik ben getuige.",
    "Ze heeft benzine gegoten in het huis en dreigt het aan te steken.",
    "Hij heeft een mes in zijn hand en komt dichterbij.",
    "Ze sloeg me en gooide me op de grond.",
    "Hij heeft iemand met opzet aangereden met de auto.",
    "Ze probeert uit het raam te springen. Ik kan haar niet tegenhouden."
]

LOW_RISK = [
    "Ik heb hulp nodig bij het verplaatsen van een zwaar object.",
    "Mijn kat is vast komen te zitten in de boom.",
    "De straatverlichting is kapot, kunt u dit melden?",
    "Ik heb mijn sleutels verloren en kan mijn huis niet in.",
    "Ik heb geluidsoverlast van de buren, kunt u iemand sturen?",
    "Mijn auto is gestolen maar ik ben veilig.",
    "Een hond loopt los op straat zonder eigenaar.",
    "Er ligt afval op de weg dat gevaarlijk kan zijn voor verkeer.",
    "Ik heb per ongeluk 112 gebeld, excuses.",
    "Een verkeersbord ligt omver, gevaarlijke situatie voor fietsers.",
    "Er is een waterlek in mijn kelder, geen spoed.",
    "De lift zit vast in mijn gebouw, ik zit er niet in.",
    "Mijn kind is zijn fiets kwijtgeraakt in het park.",
    "De verwarming werkt niet maar ik heb geen direct gevaar.",
    "Er is een gebroken raam bij een leeg gebouw.",
    "Ik wil melding maken van een klein ongeluk zonder letsel.",
    "Een dronken persoon ligt te slapen op een bankje.",
    "Er is een scooter omgevallen op de stoep.",
    "Ik hoor lawaai in een leegstaand gebouw.",
    "Een winkelwagentje drijft in de gracht."
]

def seed_calls():
    """Insert 40 Dutch calls (20 high-risk, 20 low-risk) with labels."""
    session = SessionLocal()
    inserted = 0
    try:
        # Create a set of existing transcripts to avoid duplicates
        existing = {t[0] for t in session.query(CallRecord.transcript).all()}

        # High risk: label ~ 0.80–1.00
        for text in HIGH_RISK:
            if text in existing:
                continue
            rec = CallRecord(
                transcript=text,
                danger_score=round(random.uniform(0.8, 1.0), 2),
                threat_type="fysiek",   # keep simple; model may or may not use this
                #created_at=datetime.datetime.utcnow()
            )
            session.add(rec)
            inserted += 1

        # Low risk: label ~ 0.00–0.30
        for text in LOW_RISK:
            if text in existing:
                continue
            rec = CallRecord(
                transcript=text,
                danger_score=round(random.uniform(0.0, 0.3), 2),
                threat_type="laag",
                #created_at=datetime.datetime.utcnow()
            )
            session.add(rec)
            inserted += 1

        session.commit()
        print(f"✅ Seeded {inserted} records.")
    except Exception as e:
        session.rollback()
        print("❌ Seeding failed:", e)
        raise
    finally:
        session.close()
    return inserted


def retrain_model():
    if TRAIN_FN is None:
        print("⚠️ Could not find a training function. Expected one of:\n"
              "   - model.train_pipeline.train_model_from_db()\n"
              "   - model.training.retrain_model_from_db()\n"
              "Please ensure your training script exposes one of these.")
        sys.exit(1)

    try:
        TRAIN_FN()
        print("✅ Model retrained and danger_score_model.pkl saved.")
    except Exception as e:
        print("❌ Retraining failed:", e)
        raise


if __name__ == "__main__":
    count = seed_calls()
    if count > 0:
        retrain_model()
    else:
        print("ℹ️ No new records to insert (duplicates skipped). Retraining anyway...")
        retrain_model()

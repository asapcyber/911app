# seed_dutch_calls.py
from sqlalchemy.orm import Session
from model.db import SessionLocal, engine
from model.models import Base, CallRecord

Base.metadata.create_all(bind=engine)

dutch_calls = [
    {
        "transcript": "Hallo, er is iemand ingebroken in mijn huis. Ik hoorde glas breken en iemand loopt binnen!",
        "threat_type": "fysiek",
        "danger_score": 0.9
    },
    {
        "transcript": "Mijn vrouw heeft zichzelf opgesloten in de badkamer en ze zegt dat ze zichzelf iets aan gaat doen.",
        "threat_type": "verbaal",
        "danger_score": 0.85
    },
    {
        "transcript": "Er is een man op straat met een mes. Hij lijkt verward en bedreigt mensen.",
        "threat_type": "fysiek",
        "danger_score": 0.95
    },
    {
        "transcript": "Er staat rook in het gebouw, ik denk dat er brand is op de tweede verdieping!",
        "threat_type": "fysiek",
        "danger_score": 0.8
    },
    {
        "transcript": "Ik hoor constante schreeuwen bij de buren, mogelijk huiselijk geweld.",
        "threat_type": "verbaal",
        "danger_score": 0.75
    },
    {
        "transcript": "Een kind is vermist geraakt in het park, we kunnen hem nergens vinden.",
        "threat_type": "anders",
        "danger_score": 0.7
    },
    {
        "transcript": "Iemand is flauwgevallen in de supermarkt, we weten niet wat er aan de hand is.",
        "threat_type": "anders",
        "danger_score": 0.6
    },
    {
        "transcript": "Een man staat op het dak en roept dat hij wil springen.",
        "threat_type": "verbaal",
        "danger_score": 0.92
    }
]

db: Session = SessionLocal()
for call in dutch_calls:
    db.add(CallRecord(**call))

db.commit()
db.close()
print("Seeded Dutch 112 calls successfully.")
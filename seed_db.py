from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.models import Base, Call, ThreatType
from datetime import datetime

engine = create_engine('sqlite:///112_calls.db')
Session = sessionmaker(bind=engine)
session = Session()

# Create tables
Base.metadata.create_all(engine)

# Sample data
sample_calls = [
    {
        "transcript": "My boyfriend is threatening me again. He's drunk and has a knife.",
        "threat_type": ThreatType.physical,
        "danger_score": 0.92,
        "emotions": {"fear": 0.8, "anger": 0.1, "sadness": 0.1},
        "location": "Amsterdam",
        "response_action": "Send immediate police and medical help",
    },
    {
        "transcript": "There’s someone shouting on the street, threatening passersby.",
        "threat_type": ThreatType.verbal,
        "danger_score": 0.6,
        "emotions": {"fear": 0.6, "anger": 0.2, "confusion": 0.2},
        "location": "Rotterdam",
        "response_action": "Dispatch police unit to investigate",
    },
    {
        "transcript": "My sister is sending me threatening messages online.",
        "threat_type": ThreatType.online,
        "danger_score": 0.3,
        "emotions": {"anxiety": 0.7, "frustration": 0.2},
        "location": "The Hague",
        "response_action": "Document and refer to cybercrime unit",
    },
    {
        "transcript": "A man is hitting his partner in the apartment next to mine.",
        "threat_type": ThreatType.physical,
        "danger_score": 0.85,
        "emotions": {"fear": 0.9},
        "location": "Utrecht",
        "response_action": "Immediate intervention required",
    },
    {
        "transcript": "My daughter is threatening to hurt herself again. She's locked in the bathroom.",
        "threat_type": ThreatType.self_harm,
        "danger_score": 0.88,
        "emotions": {"fear": 0.7, "sadness": 0.2},
        "location": "Eindhoven",
        "response_action": "Send ambulance and crisis team",
    },
]

# Insert
for call_data in sample_calls:
    call = Call(
        timestamp=datetime.utcnow(),
        transcript=call_data["transcript"],
        threat_type=call_data["threat_type"],
        danger_score=call_data["danger_score"],
        emotions=call_data["emotions"],
        location=call_data["location"],
        response_action=call_data["response_action"]
    )
    session.add(call)

session.commit()
print(f"✅ Seeded {session.query(Call).count()} records in 112_calls.db")

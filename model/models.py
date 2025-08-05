from sqlalchemy import create_engine, Column, Integer, String, Float, Enum, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import enum

Base = declarative_base()

class ThreatType(enum.Enum):
    verbal = "verbal"
    physical = "physical"
    self_harm = "self_harm"
    online = "online"
    unknown = "unknown"

class CallRecord(Base):
    __tablename__ = 'call_records'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    transcript = Column(String, nullable=False)
    danger_score = Column(Float, nullable=True)  # Optional: set during analysis
    sentiment = Column(String, nullable=True)
    emotions = Column(String, nullable=True)     # Stored as comma-separated string
    
class Call(Base):
    __tablename__ = 'calls'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    caller_id = Column(String, nullable=True)
    transcript = Column(Text, nullable=False)
    threat_type = Column(Enum(ThreatType), default=ThreatType.unknown)
    danger_score = Column(Float, nullable=True)
    emotions = Column(JSON, nullable=True)
    location = Column(String, nullable=True)
    response_action = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    risk_factors = relationship("RiskFactor", back_populates="call")
    mcp_queries = relationship("MCPQuery", back_populates="call")

class RiskFactor(Base):
    __tablename__ = 'risk_factors'
    
    id = Column(Integer, primary_key=True)
    call_id = Column(Integer, ForeignKey('calls.id'))
    factor = Column(String)
    impact = Column(Float)
    direction = Column(Enum("increase", "decrease", name="impact_direction"))
    
    call = relationship("Call", back_populates="risk_factors")

class MCPQuery(Base):
    __tablename__ = 'mcp_queries'
    
    id = Column(Integer, primary_key=True)
    call_id = Column(Integer, ForeignKey('calls.id'))
    query_text = Column(Text)
    response_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    call = relationship("Call", back_populates="mcp_queries")

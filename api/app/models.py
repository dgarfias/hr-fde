import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Float, Text, Boolean
from app.database import Base

class Load(Base):
    __tablename__ = "loads"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    load_id = Column(String, unique=True, nullable=False, index=True)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    pickup_datetime = Column(DateTime, nullable=False)
    delivery_datetime = Column(DateTime, nullable=False)
    equipment_type = Column(String, nullable=False)
    loadboard_rate = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)
    weight = Column(Float, nullable=True)
    commodity_type = Column(String, nullable=True)
    num_of_pieces = Column(Integer, nullable=True)
    miles = Column(Float, nullable=True)
    dimensions = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Offer(Base):
    __tablename__ = "offers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    call_id = Column(String, nullable=False, index=True)
    mc_number = Column(String, nullable=False)
    carrier_name = Column(String, nullable=True)
    load_id = Column(String, nullable=False)
    agreed_rate = Column(Float, nullable=True)
    initial_rate = Column(Float, nullable=True)
    negotiation_rounds = Column(Integer, default=0)
    outcome = Column(String, nullable=False)  # price_agreed, declined, callback_requested, not_eligible
    sentiment = Column(String, nullable=True)   # positive, neutral, negative
    origin = Column(String, nullable=True)
    destination = Column(String, nullable=True)
    equipment_type = Column(String, nullable=True)
    transcript_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class CallRecord(Base):
    __tablename__ = "call_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    run_id = Column(String, unique=True, nullable=False, index=True)
    
    # Carrier info
    mc_number = Column(String, nullable=True)
    carrier_name = Column(String, nullable=True)
    
    # Load info
    load_id = Column(String, nullable=True)
    origin = Column(String, nullable=True)
    destination = Column(String, nullable=True)
    equipment_type = Column(String, nullable=True)
    
    # Offer / negotiation
    agreed_rate = Column(Float, nullable=True)
    initial_rate = Column(Float, nullable=True)  # Original loadboard rate
    outcome = Column(String, nullable=True)  # agreed, declined, not_eligible, no_match, dropped
    sentiment = Column(String, nullable=True)  # positive, neutral, negative
    
    # Call metadata
    duration_seconds = Column(Integer, nullable=True)
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    summary = Column(Text, nullable=True)
    
    # Boolean flags for metrics
    loads_found = Column(Boolean, default=True)
    call_dropped = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)

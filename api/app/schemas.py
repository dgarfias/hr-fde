from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

# --- Load Schemas ---

class LoadBase(BaseModel):
    load_id: str
    origin: str
    destination: str
    pickup_datetime: datetime
    delivery_datetime: datetime
    equipment_type: str
    loadboard_rate: float
    notes: Optional[str] = None
    weight: Optional[float] = None
    commodity_type: Optional[str] = None
    num_of_pieces: Optional[int] = None
    miles: Optional[float] = None
    dimensions: Optional[str] = None

class LoadCreate(LoadBase):
    pass

class LoadResponse(LoadBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class LoadSearchParams(BaseModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    equipment_type: Optional[str] = None
    pickup_date: Optional[str] = None  # YYYY-MM-DD

class LoadMatchItem(BaseModel):
    """Individual load inside the match response."""
    load_id: str
    origin: str
    destination: str
    pickup_datetime: datetime
    delivery_datetime: datetime
    equipment_type: str
    loadboard_rate: float
    miles: float
    notes: Optional[str] = None

class LoadMatchResponse(BaseModel):
    """Load match response for voice agent tools.
    Returns a single flat object with a `loads` array inside,
    mirroring the FMCSAVerifyResponse pattern (status flag + data).
    The agent checks `found`, then reads from `loads`."""
    found: bool
    count: int = 0
    loads: list[LoadMatchItem] = []

# --- FMCSA Schemas ---

class FMCSAVerifyRequest(BaseModel):
    mc_number: str = Field(..., min_length=1, description="Motor Carrier Number")

class FMCSAVerifyResponse(BaseModel):
    eligible: bool
    carrier_name: Optional[str] = None
    status: Optional[str] = None
    mc_number: str

# --- Offer Schemas ---

class OfferCreate(BaseModel):
    call_id: str
    mc_number: str
    carrier_name: Optional[str] = None
    load_id: str
    agreed_rate: Optional[float] = None
    initial_rate: Optional[float] = None
    negotiation_rounds: int = 0
    outcome: str = Field(..., pattern="^(price_agreed|declined|callback_requested|not_eligible)$")
    sentiment: Optional[str] = Field(None, pattern="^(positive|neutral|negative)$")
    origin: Optional[str] = None
    destination: Optional[str] = None
    equipment_type: Optional[str] = None
    transcript_summary: Optional[str] = None

class OfferResponse(OfferCreate):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Metrics Schemas ---

class MetricsResponse(BaseModel):
    total_calls: int
    total_offers: int
    conversion_rate: float
    avg_negotiation_rounds: float
    avg_agreed_rate: Optional[float] = None
    sentiment_distribution: dict[str, int]
    outcome_distribution: dict[str, int]
    calls_last_7_days: list[dict]

# --- Call Log Schemas ---

class CallStartRequest(BaseModel):
    caller_number: Optional[str] = None
    workflow_run_id: Optional[str] = None
    session_id: Optional[str] = None

class CallEndRequest(BaseModel):
    call_id: str
    duration_seconds: int
    status: str = Field(..., pattern="^(completed|failed)$")

class CallLogResponse(BaseModel):
    id: str
    call_id: str
    workflow_run_id: Optional[str] = None
    session_id: Optional[str] = None
    caller_number: Optional[str] = None
    started_at: datetime
    ended_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    status: str

    class Config:
        from_attributes = True

# --- Call Record Schemas ---

class CallRecordCreate(BaseModel):
    run_id: str  # From @trigger.run_id in HappyRobot
    mc_number: Optional[str] = None
    carrier_name: Optional[str] = None
    
    # Load info
    load_id: Optional[str] = None
    origin: Optional[str] = None
    destination: Optional[str] = None
    equipment_type: Optional[str] = None
    
    # Negotiation
    agreed_rate: Optional[float] = None
    initial_rate: Optional[float] = None  # Original loadboard rate
    
    # Classifications
    outcome: str = Field(..., pattern="^(agreed|declined|not_eligible|no_match|dropped)$")
    sentiment: Optional[str] = Field(None, pattern="^(positive|neutral|negative)$")
    
    # Call metadata
    duration_seconds: Optional[int] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    summary: Optional[str] = None
    
    # Flags
    loads_found: bool = True
    call_dropped: bool = False

class CallRecordResponse(CallRecordCreate):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Health Schemas ---

class HealthResponse(BaseModel):
    status: str
    version: str = "1.0.0"

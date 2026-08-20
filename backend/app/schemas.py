from typing import Literal, Optional
from pydantic import BaseModel, Field


class ChatHistoryItem(BaseModel):
    role: Literal["user", "bot"]
    text: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    history: list[ChatHistoryItem] = []


class ChatResponse(BaseModel):
    answer: str
    topic: str
    sources: list[str] = []


class LoadItem(BaseModel):
    """A single appliance/load the user wants backed up during an outage."""
    name: str
    watts: float = Field(gt=0)
    quantity: int = Field(default=1, ge=1)


class RecommendationRequest(BaseModel):
    monthly_units: float = Field(gt=0, description="Average monthly electricity consumption in kWh (units)")
    city: Optional[str] = Field(default=None, description="City, used for context/reason text; not yet used in sizing math")
    roof_area_sqft: float = Field(default=0, ge=0, description="Available roof area in sq ft. 0 = unknown/skip check")
    backup_hours: float = Field(default=0, ge=0, description="Hours of backup needed during an outage")
    battery_required: bool = False
    major_loads: list[LoadItem] = Field(default_factory=list, description="Appliances that must run on backup power")
    system_preference: Literal["on-grid", "hybrid", "off-grid", "auto"] = "auto"
    grid_available: bool = Field(default=True, description="Whether grid connection exists at the site")
    panel_watt: int = 585


class RecommendationResponse(BaseModel):
    system_kw: float
    panels: int
    inverter_kw: float
    battery_kwh: float
    system_type: str
    reason: str
    note: str

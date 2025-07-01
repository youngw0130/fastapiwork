from pydantic import BaseModel
from typing import Optional

class RegionBase(BaseModel):
    name: str
    city: str
    gu: str
    housing_price: int
    transport_score: float
    safety_score: float
    environment_score: float
    score: float

class RegionCreate(RegionBase):
    pass

class Region(RegionBase):
    id: int

    class Config:
        from_attributes = True
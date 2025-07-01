from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    city = Column(String)
    gu = Column(String)
    housing_price = Column(Integer)
    transport_score = Column(Float)
    safety_score = Column(Float)
    environment_score = Column(Float)
    score = Column(Float)
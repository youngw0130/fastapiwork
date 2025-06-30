from sqlalchemy.orm import Session
from . import models, schemas

def get_region(db: Session, region_id: int):
    return db.query(models.Region).filter(models.Region.id == region_id).first()

def get_regions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Region).offset(skip).limit(limit).all()

def create_region(db: Session, region: schemas.RegionCreate):
    score = (region.transport_score + region.safety_score + region.environment_score) / 3

    db_region = models.Region(
        name=region.name,
        city=region.city,
        gu=region.gu,
        housing_price=region.housing_price,
        transport_score=region.transport_score,
        safety_score=region.safety_score,
        environment_score=region.environment_score,
        score=round(score, 2)
    )
    db.add(db_region)
    db.commit()
    db.refresh(db_region)
    return db_region
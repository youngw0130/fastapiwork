from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal

router = APIRouter(prefix="/regions", tags=["regions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Region)
def create(region: schemas.RegionCreate, db: Session = Depends(get_db)):
    return crud.create_region(db, region)

@router.get("/", response_model=list[schemas.Region])
def read_all(db: Session = Depends(get_db)):
    return crud.get_regions(db)

@router.get("/{region_id}", response_model=schemas.Region)
def read_one(region_id: int, db: Session = Depends(get_db)):
    db_region = crud.get_region(db, region_id)
    if not db_region:
        raise HTTPException(status_code=404, detail="Not found")
    return db_region

@router.put("/{region_id}", response_model=schemas.Region)
def update_region(region_id: int, region: schemas.RegionCreate, db: Session = Depends(get_db)):
    db_region = crud.get_region(db, region_id)
    if not db_region:
        raise HTTPException(status_code=404, detail="Not found")
    db_region.name = region.name
    db_region.city = region.city
    db_region.gu = region.gu
    db_region.housing_price = region.housing_price
    db_region.transport_score = region.transport_score
    db_region.safety_score = region.safety_score
    db_region.environment_score = region.environment_score
    db_region.score = region.score
    db.commit()
    db.refresh(db_region)
    return db_region

@router.delete("/{region_id}")
def delete_region(region_id: int, db: Session = Depends(get_db)):
    db_region = crud.get_region(db, region_id)
    if not db_region:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(db_region)
    db.commit()
    return {"ok": True}
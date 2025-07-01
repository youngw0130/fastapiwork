from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.database import Base, engine, SessionLocal
from app.routers import region
from app import crud, models

import os

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(region.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    regions = crud.get_regions(db)
    return templates.TemplateResponse("index.html", {"request": request, "regions": regions})

@app.get("/regions/{region_id}")
def region_detail(region_id: int, request: Request, db: Session = Depends(get_db)):
    region = crud.get_region(db, region_id)
    if not region:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse("region_detail.html", {"request": request, "region": region})

def insert_dummy_data():
    db = SessionLocal()
    # 기존 데이터 모두 삭제
    db.query(models.Region).delete()
    db.commit()
    # 더미 데이터 삽입
    dummy_regions = [
        models.Region(name="강남역", city="서울", gu="강남구", housing_price=2000000, transport_score=4.5, safety_score=4.2, environment_score=4.0, score=4.7),
        models.Region(name="잠실", city="서울", gu="송파구", housing_price=1700000, transport_score=4.3, safety_score=4.1, environment_score=4.2, score=4.5),
        models.Region(name="홍대입구", city="서울", gu="마포구", housing_price=1500000, transport_score=4.0, safety_score=3.8, environment_score=3.9, score=4.1),
        models.Region(name="광화문", city="서울", gu="종로구", housing_price=1600000, transport_score=4.2, safety_score=4.0, environment_score=4.1, score=4.3),
        models.Region(name="구로디지털단지", city="서울", gu="구로구", housing_price=1200000, transport_score=3.7, safety_score=3.5, environment_score=3.8, score=3.9),
        models.Region(name="신촌", city="서울", gu="서대문구", housing_price=1400000, transport_score=4.1, safety_score=3.9, environment_score=3.7, score=4.0),
        models.Region(name="건대입구", city="서울", gu="광진구", housing_price=1300000, transport_score=3.8, safety_score=3.6, environment_score=3.9, score=3.8),
        models.Region(name="노원", city="서울", gu="노원구", housing_price=1100000, transport_score=3.5, safety_score=3.7, environment_score=3.6, score=3.6),
        models.Region(name="목동", city="서울", gu="양천구", housing_price=1250000, transport_score=3.9, safety_score=3.8, environment_score=3.7, score=3.9),
        models.Region(name="여의도", city="서울", gu="영등포구", housing_price=1750000, transport_score=4.2, safety_score=4.0, environment_score=4.1, score=4.4),
    ]
    db.add_all(dummy_regions)
    db.commit()
    db.close()

insert_dummy_data()
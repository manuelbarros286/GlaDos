
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.api.schemas import ReportSchema
from src.models.intelligence_report import IntelligenceReport
from src.ingestion.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/reports", response_model=List[ReportSchema])
async def get_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reports = db.query(IntelligenceReport).offset(skip).limit(limit).all()

    return reports

@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    from sqlalchemy import func
    stats = db.query(IntelligenceReport.source,
                     func.count(IntelligenceReport.id)
                     ).group_by(IntelligenceReport.source).all()

    return {source: count for source, count in stats}
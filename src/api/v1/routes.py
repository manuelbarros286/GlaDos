
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.api.schemas import ReportSchema, PaginatedReportSchema
from src.models.intelligence_report import IntelligenceReport
from src.ingestion.database import SessionLocal
from sqlalchemy import func

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/reports", response_model=PaginatedReportSchema)
async def get_reports(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    total_count = db.query(IntelligenceReport).count()

    reports = (db.query(IntelligenceReport)
               .order_by(IntelligenceReport.published_date.desc())
               .offset(skip)
               .limit(limit)
               .all())

    return {
        "total": total_count,
        "page" : (skip // limit) * 1,
        "limit" : limit,
        "results" : reports
    }

@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    stats = db.query(IntelligenceReport.source,
                     func.count(IntelligenceReport.id)
                     ).group_by(IntelligenceReport.source).all()

    return {source: count for source, count in stats}

@router.get("/search", response_model=List[ReportSchema])
async def search_reports(query: str, db: Session = Depends(get_db)):
    search_query = func.plainto_tsquery('english', query)
    search_vector = func.to_tsvector('english', IntelligenceReport.title + " " + IntelligenceReport.content)
    results = db.query(IntelligenceReport).filter(
        search_vector.op('@@')(search_query)
    ).order_by(func.ts_rank(search_vector, search_query).desc()
    ).limit(20).all()

    if not results:
        raise HTTPException(status_code=404, detail="No reports not found.")

    return results

@router.get("/trending-topics")
async def get_trending_topics(db: Session = Depends(get_db)):
    reports = db.query(IntelligenceReport.title).limit(100).all()

    all_text = " ".join([report.title for report in reports])
    from collections import Counter
    import re
    words = re.findall(r'\b\w+\b', all_text.lower())
    stop_words = {'and', 'the', 'for', 'with', 'from', 'more', 'about', 'identified', 'to', 'of', 'in', 'at', 's'}
    filtered_words = [w for w in words if w not in stop_words]

    top_topics = Counter(filtered_words).most_common(15)

    return {"trending_topics": {word: count for word, count in top_topics}}
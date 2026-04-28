from pydantic import BaseModel
from datetime import datetime
from typing import List

class ReportSchema(BaseModel):
    id: int
    title: str
    source: str
    link: str
    published_date: datetime

    class Config:
        from_attributes = True # Work with SQLAlchemy objects

class PaginatedReportSchema(BaseModel):
    total: int
    page: int
    limit: int
    results: List[ReportSchema]

    class Config:
        from_attributes = True

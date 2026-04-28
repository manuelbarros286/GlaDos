from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReportSchema(BaseModel):
    id: int
    title: str
    source: str
    link: str
    published_date: datetime

    class Config:
        from_attributes = True # Tells Pydantic to work with SQLAlchemy objects

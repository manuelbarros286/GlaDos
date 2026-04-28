from sqlalchemy import Column, Integer, String, Text, DateTime, UniqueConstraint
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class IntelligenceReport(Base):
    __tablename__ = 'intelligence_reports'

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=True)
    link = Column(String(1000), unique=True, nullable=False)
    source = Column(String(100), nullable=False)
    published_date = Column(DateTime, default=datetime.now(), nullable=False)

    # unique links
    __table_args__ = (UniqueConstraint('link', name='_link_uc'),)

    def __repr__(self):
        return f"<IntelligenceReport(title='{self.title[:30]}...', source='{self.source}')>"

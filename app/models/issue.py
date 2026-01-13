from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base
from sqlalchemy import DateTime
from sqlalchemy.sql import func

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="open")
    version = Column(Integer, default=1)

resolved_at = Column(DateTime, nullable=True)
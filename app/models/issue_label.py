from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base

class IssueLabel(Base):
    __tablename__ = "issue_labels"

    issue_id = Column(Integer, ForeignKey("issues.id"), primary_key=True)
    label_id = Column(Integer, ForeignKey("labels.id"), primary_key=True)

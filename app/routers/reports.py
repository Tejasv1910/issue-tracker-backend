from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import SessionLocal
from app.models.issue import Issue

router = APIRouter(prefix="/reports", tags=["Reports"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/top-assignees")
def top_assignees(db: Session = Depends(get_db)):
    result = (
        db.query(
            Issue.assignee_id,
            func.count(Issue.id).label("issue_count")
        )
        .group_by(Issue.assignee_id)
        .order_by(func.count(Issue.id).desc())
        .all()
    )

    return [
        {"assignee_id": r.assignee_id, "issue_count": r.issue_count}
        for r in result
    ]

@router.get("/latency")
def average_resolution_time(db: Session = Depends(get_db)):
    result = (
        db.query(
            func.avg(
                func.extract(
                    "epoch",
                    Issue.resolved_at - Issue.created_at
                )
            )
        )
        .filter(Issue.resolved_at.isnot(None))
        .scalar()
    )

    if result is None:
        return {"average_resolution_seconds": None}

    return {"average_resolution_seconds": int(result)}

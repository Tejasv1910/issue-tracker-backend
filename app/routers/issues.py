from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import SessionLocal
from app.models.issue import Issue
from app.schemas.issue import IssueCreate
from app.schemas.issue import IssueResponse
from fastapi import HTTPException
from app.schemas.issue import IssueUpdate
from app.models.comment import Comment
from app.schemas.comment import CommentCreate
from app.models.label import Label
from app.models.issue_label import IssueLabel
from app.schemas.label import LabelAssign, LabelCreate
from app.schemas.issue import BulkStatusUpdate
import csv
from fastapi import UploadFile, File

router = APIRouter(prefix="/issues", tags=["Issues"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_issue(issue: IssueCreate, db: Session = Depends(get_db)):
    new_issue = Issue(
        title=issue.title,
        description=issue.description
    )
    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)
    return new_issue

@router.get("/", response_model=List[IssueResponse])
def get_issues(db: Session = Depends(get_db)):
    issues = db.query(Issue).all()
    return issues

@router.get("/{issue_id}", response_model=IssueResponse)
def get_issue(issue_id: int, db: Session = Depends(get_db)):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()

    if issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")

    return issue

@router.patch("/{issue_id}", response_model=IssueResponse)
def update_issue(issue_id: int, issue_update: IssueUpdate, db: Session = Depends(get_db)):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()

    if issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")

    # 🔒 VERSION CHECK (MOST IMPORTANT PART)
    if issue.version != issue_update.version:
        raise HTTPException(
            status_code=409,
            detail="Issue was updated by another user"
        )

    # Update fields only if provided
    if issue_update.title is not None:
        issue.title = issue_update.title

    if issue_update.description is not None:
        issue.description = issue_update.description

    if issue_update.status is not None:
        issue.status = issue_update.status

    # Increment version
    issue.version += 1

    db.commit()
    db.refresh(issue)

    return issue

@router.post("/{issue_id}/comments")
def add_comment(
    issue_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db)
):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()

    if issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")

    new_comment = Comment(
        issue_id=issue_id,
        body=comment.body
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment

@router.post("/labels")
def create_label(label: LabelCreate, db: Session = Depends(get_db)):
    existing = db.query(Label).filter(Label.name == label.name).first()
    if existing:
        return existing

    new_label = Label(name=label.name)
    db.add(new_label)
    db.commit()
    db.refresh(new_label)
    return new_label

@router.put("/{issue_id}/labels")
def assign_labels(
    issue_id: int,
    data: LabelAssign,
    db: Session = Depends(get_db)
):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    # Remove existing labels
    db.query(IssueLabel).filter(IssueLabel.issue_id == issue_id).delete()

    for label_name in data.labels:
        label = db.query(Label).filter(Label.name == label_name).first()
        if not label:
            label = Label(name=label_name)
            db.add(label)
            db.flush()  # get label.id

        link = IssueLabel(issue_id=issue_id, label_id=label.id)
        db.add(link)

    db.commit()
    return {"message": "Labels updated successfully"}

@router.post("/bulk-status")
def bulk_status_update(
    data: BulkStatusUpdate,
    db: Session = Depends(get_db)
):
    try:
        for issue_id in data.issue_ids:
            issue = db.query(Issue).filter(Issue.id == issue_id).first()

            if not issue:
                raise HTTPException(
                    status_code=400,
                    detail=f"Issue {issue_id} not found"
                )

            issue.status = data.status

        db.commit()
        return {"message": "Bulk status update successful"}

    except Exception as e:
        db.rollback()
        raise e

@router.post("/import")
def import_issues(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    created = 0
    failed = 0
    errors = []

    content = file.file.read().decode("utf-8").splitlines()
    reader = csv.DictReader(content)

    for index, row in enumerate(reader, start=1):
        title = row.get("title")

        if not title or title.strip() == "":
            failed += 1
            errors.append(f"Row {index}: title is required")
            continue

        issue = Issue(
            title=title.strip(),
            description=row.get("description")
        )

        db.add(issue)
        created += 1

    db.commit()

    return {
        "created": created,
        "failed": failed,
        "errors": errors
    }

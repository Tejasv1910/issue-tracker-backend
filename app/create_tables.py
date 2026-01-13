from app.core.database import engine, Base
from app.models.issue import Issue  # IMPORTANT: import model
from app.models.comment import Comment
from app.models.label import Label
from app.models.issue_label import IssueLabel


Base.metadata.create_all(bind=engine)

print("Tables created successfully")


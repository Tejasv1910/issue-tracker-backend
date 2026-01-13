# Issue Tracker Backend

Backend Issue Tracker API built using **FastAPI** and **PostgreSQL** as part of an evaluation assignment.

---

## Tech Stack
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic

---

## Features
- Issue CRUD operations
- Optimistic locking using versioning
- Comments on issues
- Labels (many-to-many relationship)
- Transactional bulk status update
- CSV import with validation summary
- Aggregated reports (top assignees, average resolution time)

---

## Setup

1. Create PostgreSQL database:
issue_tracker


2. Install dependencies:
```bash:
pip install -r requirements.txt

3. Create tables:
python -m app.create_tables

4. Run Server:
uvicorn app.main:app

5. Ope API docs:
http://127.0.0.1:8000/docs


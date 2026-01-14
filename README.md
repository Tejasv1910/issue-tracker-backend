# Issue Tracker Backend API

Backend Issue Tracker application developed as part of a technical evaluation.  
Built using **FastAPI** and **PostgreSQL**, focusing on real-world backend practices.

## Tech Stack
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic

## Features
- Issue CRUD operations
- Optimistic locking using versioning
- Comments on issues
- Labels with many-to-many relationship
- Transactional bulk status updates
- CSV import with validation summary
- Reports (top assignees, average resolution time)

## Setup

1. Create PostgreSQL database:
issue_tracker

2. Install dependencies:
pip install -r requirements.txt

3. Create tables:
python -m app.create_tables

4. Run server:
uvicorn app.main:app

5. Open API docs:
http://127.0.0.1:8000/docs

## Key APIs
- POST /issues
- GET /issues
- PATCH /issues/{id}
- POST /issues/{id}/comments
- PUT /issues/{id}/labels
- POST /issues/bulk-status
- POST /issues/import
- GET /reports/*

## Author
Tejasv

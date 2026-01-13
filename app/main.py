from fastapi import FastAPI
from app.routers.issues import router as issue_router
from app.routers.reports import router as reports_router

app = FastAPI()

app.include_router(issue_router)

@app.get("/")
def root():
    return {"message": "Issue Tracker API is running"}

app.include_router(reports_router)
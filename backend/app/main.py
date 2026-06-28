from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine, Base
# Add analysis and analytics to your imports here!
from app.api.routers import auth, jobs, candidates, analytics
# analysis disabled temporarily for Render deployment

# Initialize DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RecruitIQ API",
    description="Intelligent Candidate Discovery Pipeline",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include ALL Routers
app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(candidates.router)
#app.include_router(analysis.router)   # <--- Add this
app.include_router(analytics.router)  # <--- Add this

@app.get("/health")
def health_check():
    return {"status": "operational", "system": "RecruitIQ Backend"}

@app.get("/")
def home():
    return {"message": "RecruitIQ backend is live"}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine
from app.models import HCP, Interaction
from app.api.hcp_routes import router as hcp_router
from app.api.interaction_routes import router as interaction_router
from app.api.ai_routes import router as ai_router


# keep any ither router imports i already have here
app = FastAPI(
    title="AI-HCP CRM",
    version="1.0.0",
    description="AI First CRM for Healthcare Professionals"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://ai-hcp-crm-chi.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(hcp_router)
app.include_router(interaction_router)
app.include_router(ai_router)

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "AI-HCP CRM Backend Running 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
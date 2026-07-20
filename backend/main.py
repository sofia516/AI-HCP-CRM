from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine
from app.models import HCP, Interaction
from app.api.hcp_routes import router as hcp_router
from app.api.interaction_routes import router as interaction_router
from app.api.ai_routes import router as ai_router


app = FastAPI(
    title="AI-HCP CRM",
    version="1.0.0",
    description="AI First CRM for Healthcare Professionals"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
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
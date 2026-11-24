import sys
import os
import contextlib
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.core.database import Base, engine
from backend.api.routes import router as api_router
from backend.seed_data import seed_database

# Create DB tables
Base.metadata.create_all(bind=engine)

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    print("=====================================================")
    print(" TRACEGRID Backend Engine Initializing...")
    print(f" Team: {settings.TEAM_NAME} | {settings.HACKATHON_TAG}")
    print("=====================================================")
    # Auto-seed database if empty
    try:
        seed_database()
    except Exception as e:
        print(f"Warning during auto-seed: {e}")
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Unified Financial Crime Analytics & Investigation Platform. Team CyboShield (PS05).",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permissive for local development and hackathon evaluation
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root_info():
    return {
        "project": settings.PROJECT_NAME,
        "team": settings.TEAM_NAME,
        "hackathon": settings.HACKATHON_TAG,
        "version": settings.VERSION,
        "documentation": "/docs",
        "health": f"{settings.API_V1_STR}/health"
    }

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)

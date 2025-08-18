from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .interfaces.api.router import api_router
from .infrastructure.database.connection import engine
from .infrastructure.database.models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Backend with DDD",
    description="A FastAPI backend following Domain Driven Design principles",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to FastAPI Backend with DDD",
        "docs": "/docs",
        "redoc": "/redoc",
        "architecture": "Domain Driven Design"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "architecture": "DDD"} 
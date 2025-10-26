from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import images

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)

# CORS middleware - allows frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(images.router)


@app.get("/")
def ping():
    return {
        "message": "API is working!",
        "app": settings.app_name,
        "version": settings.app_version
    }
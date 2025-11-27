from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .routers import analysis
from .core.config import settings
import os

app = FastAPI(
    title="Gym Exercise Form Coach",
    description="AI-powered exercise form analysis using computer vision",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include routers
app.include_router(analysis.router, prefix="/api/v1")


@app.get("/")
async def root():
    """Serve the main web interface"""
    static_file = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(static_file):
        return FileResponse(static_file)
    else:
        return {
            "message": "Gym Exercise Form Coach API",
            "version": "1.0.0",
            "endpoints": {
                "analyze": "/api/v1/analyze",
                "health": "/api/v1/health",
                "supported_exercises": "/api/v1/supported-exercises",
                "docs": "/docs"
            }
        }


@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "message": "Gym Exercise Form Coach API",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/api/v1/analyze",
            "health": "/api/v1/health",
            "supported_exercises": "/api/v1/supported-exercises",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
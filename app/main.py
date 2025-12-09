from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.core.config import settings
from app.database import Base,engine
from app.routers import auth, users, posts
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)

# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App starting up")
    yield
    logger.info("App shutting down")


# Create FastAPI app
app = FastAPI(
    title= settings.PROJECT_NAME,
    version = "1.0.0",
    description= "Twitter-like API Backend",
    lifespan= lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]

)


# Health check
@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint"""
    return {"status" : "ok", "version": "1.0.0"}


# Include router
app.include_router(auth.router,prefix=settings.API_V1_STR)
app.include_router(users.router,prefix=settings.API_V1_STR)
app.include_router(posts.router,prefix=settings.API_V1_STR)



# Global exception hanlder
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail" : "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload = settings.DEBUG
    )
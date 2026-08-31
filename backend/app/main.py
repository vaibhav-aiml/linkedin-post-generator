from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from backend.app.core.config import settings
from backend.app.core.database import engine, Base
from backend.app.core.limiter import limiter
from backend.app.api.v1 import auth, posts, analyzer, export, upload

# Ensure database tables exist on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Production-grade API for AI-powered LinkedIn Post & Message Generation, Analytics, Document Extraction, and PDF Export.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Configure CORS
origins = settings.cors_origins_list
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API v1 Routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(posts.router, prefix="/api/v1")
app.include_router(analyzer.router, prefix="/api/v1")
app.include_router(export.router, prefix="/api/v1")
app.include_router(upload.router, prefix="/api/v1")

# Also register legacy route prefixes for backward compatibility with existing frontend
app.include_router(auth.router, prefix="/api")
app.include_router(posts.router, prefix="/api")
app.include_router(analyzer.router, prefix="/api")
app.include_router(export.router, prefix="/api")
app.include_router(upload.router, prefix="/api")


@app.api_route("/", methods=["GET", "HEAD"], tags=["Root"])
@limiter.exempt
def root():
    return {
        "message": "Welcome to LinkedIn Content Studio API v2.0",
        "docs": "/docs",
        "health": "/api/health"
    }


@app.api_route("/health", methods=["GET", "HEAD"], tags=["Health Diagnostics"])
@app.api_route("/api/health", methods=["GET", "HEAD"], tags=["Health Diagnostics"])
@limiter.exempt
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "llm_provider": settings.LLM_PROVIDER
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=settings.PORT, reload=settings.DEBUG)


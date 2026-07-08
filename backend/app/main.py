from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import admin, auth, emotions, favorites, recommendations
from .core.config import get_settings
from .core.database import ensure_indexes

settings = get_settings()

app = FastAPI(
    title="MoodTune AI API",
    description="Facial-expression based music recommendations with Spotify fallback support.",
    version="1.0.0",
    openapi_url=f"{settings.api_prefix}/openapi.json",
    docs_url=f"{settings.api_prefix}/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup() -> None:
    try:
        await ensure_indexes()
    except Exception as exc:
        print(f"MongoDB index creation skipped: {exc}")


@app.get("/")
async def root():
    return {"name": settings.app_name, "docs": f"{settings.api_prefix}/docs"}


@app.get(f"{settings.api_prefix}/health")
async def health():
    return {"status": "ok", "environment": settings.environment}


app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(emotions.router, prefix=settings.api_prefix)
app.include_router(recommendations.router, prefix=settings.api_prefix)
app.include_router(favorites.router, prefix=settings.api_prefix)
app.include_router(admin.router, prefix=settings.api_prefix)

from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from ..core.database import db
from ..core.security import get_current_user
from ..models.schemas import RecommendationCreate
from ..services.recommendations import choose_genres
from ..services.spotify import local_tracks, spotify_service

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.post("")
async def create_recommendation(payload: RecommendationCreate, user: dict = Depends(get_current_user)):
    history = await db.recommendations.find({"user_id": user["id"]}).sort("created_at", -1).limit(8).to_list(length=8)
    genres = choose_genres(payload.emotion, user.get("favourite_genres", []), history)
    tracks = await spotify_service.search_tracks(genres)
    source = "spotify"
    if not tracks:
        tracks = local_tracks(genres)
        source = "local"
    document = {
        "user_id": user["id"],
        "emotion": payload.emotion,
        "confidence": payload.confidence,
        "genres": genres,
        "tracks": tracks,
        "source": source,
        "created_at": datetime.now(timezone.utc),
    }
    result = await db.recommendations.insert_one(document)
    document["id"] = str(result.inserted_id)
    document.pop("_id", None)
    return document


@router.get("/history")
async def recommendation_history(user: dict = Depends(get_current_user)):
    cursor = db.recommendations.find({"user_id": user["id"]}).sort("created_at", -1).limit(30)
    items = []
    async for item in cursor:
        item["id"] = str(item.pop("_id"))
        items.append(item)
    return items

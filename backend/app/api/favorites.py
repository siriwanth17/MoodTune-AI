from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from pymongo.errors import DuplicateKeyError
from ..core.database import db
from ..core.security import get_current_user
from ..models.schemas import FavoriteCreate

router = APIRouter(prefix="/favorites", tags=["Favorites"])


@router.get("")
async def list_favorites(user: dict = Depends(get_current_user)):
    cursor = db.favorites.find({"user_id": user["id"]}).sort("created_at", -1)
    items = []
    async for item in cursor:
        item["id"] = str(item.pop("_id"))
        items.append(item)
    return items


@router.post("")
async def add_favorite(payload: FavoriteCreate, user: dict = Depends(get_current_user)):
    document = {"user_id": user["id"], "track_id": payload.track.track_id, "track": payload.track.model_dump(), "created_at": datetime.now(timezone.utc)}
    try:
        result = await db.favorites.insert_one(document)
        document["id"] = str(result.inserted_id)
    except DuplicateKeyError:
        existing = await db.favorites.find_one({"user_id": user["id"], "track_id": payload.track.track_id})
        existing["id"] = str(existing.pop("_id"))
        return existing
    return document


@router.delete("/{track_id}")
async def remove_favorite(track_id: str, user: dict = Depends(get_current_user)):
    await db.favorites.delete_one({"user_id": user["id"], "track_id": track_id})
    return {"message": "Favorite removed"}

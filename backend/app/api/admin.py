from collections import Counter
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends
from ..core.database import db
from ..core.security import require_admin

router = APIRouter(prefix="/admin", tags=["Admin"])


async def bucket_counts(collection: str, field: str, days: int = 30):
    since = datetime.now(timezone.utc) - timedelta(days=days)
    pipeline = [
        {"$match": {field: {"$gte": since}}},
        {"$group": {"_id": {"$dateToString": {"format": "%Y-%m-%d", "date": f"${field}"}}, "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
    ]
    return [{"date": row["_id"], "count": row["count"]} async for row in db[collection].aggregate(pipeline)]


@router.get("/stats")
async def stats(_: dict = Depends(require_admin)):
    total_users = await db.users.count_documents({})
    total_recommendations = await db.recommendations.count_documents({})
    emotions = [row["emotion"] async for row in db.emotion_history.find({}, {"emotion": 1})]
    most_detected = Counter(emotions).most_common(1)
    users = []
    async for user in db.users.find({}, {"password_hash": 0}).sort("created_at", -1).limit(100):
        user["id"] = str(user.pop("_id"))
        users.append(user)
    return {
        "total_users": total_users,
        "total_recommendations": total_recommendations,
        "most_detected_emotion": most_detected[0][0] if most_detected else "none",
        "daily_activity": await bucket_counts("recommendations", "created_at", 14),
        "monthly_activity": await bucket_counts("recommendations", "created_at", 365),
        "api_statistics": {
            "emotion_detections": await db.emotion_history.count_documents({}),
            "favorites": await db.favorites.count_documents({}),
            "spotify_enabled": bool(__import__("app.core.config", fromlist=["get_settings"]).get_settings().spotify_client_id),
        },
        "users": users,
    }

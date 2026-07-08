from motor.motor_asyncio import AsyncIOMotorClient
from .config import get_settings

settings = get_settings()
client = AsyncIOMotorClient(settings.mongo_url)
db = client[settings.mongo_db]


async def ensure_indexes() -> None:
    await db.users.create_index("email", unique=True)
    await db.recommendations.create_index([("user_id", 1), ("created_at", -1)])
    await db.emotion_history.create_index([("user_id", 1), ("timestamp", -1)])
    await db.favorites.create_index([("user_id", 1), ("track_id", 1)], unique=True)
    await db.admin_logs.create_index("created_at")

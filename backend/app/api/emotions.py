from fastapi import APIRouter, Depends
from ..core.database import db
from ..core.security import get_current_user
from ..models.schemas import EmotionDetectRequest
from ..services.ai import emotion_detector

router = APIRouter(prefix="/emotions", tags=["Emotion Detection"])


@router.post("/detect")
async def detect_emotion(payload: EmotionDetectRequest, user: dict = Depends(get_current_user)):
    result = emotion_detector.analyze(payload.image)
    await db.emotion_history.insert_one({"user_id": user["id"], **result})
    return result


@router.get("/history")
async def emotion_history(user: dict = Depends(get_current_user)):
    cursor = db.emotion_history.find({"user_id": user["id"]}).sort("timestamp", -1).limit(30)
    items = []
    async for item in cursor:
        item["id"] = str(item.pop("_id"))
        items.append(item)
    return items

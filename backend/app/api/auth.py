from datetime import datetime, timedelta, timezone
import secrets
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from ..core.database import db
from ..core.security import create_access_token, get_current_user, hash_password, verify_password
from ..models.schemas import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    ProfileUpdate,
    ResetPasswordRequest,
    UserCreate,
    UserLogin,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


def public_user(user: dict) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user.get("role", "user"),
        "favourite_genres": user.get("favourite_genres", []),
        "profile_picture": user.get("profile_picture"),
        "created_at": user.get("created_at"),
    }


@router.post("/register")
async def register(payload: UserCreate):
    existing = await db.users.find_one({"email": payload.email.lower()})
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    now = datetime.now(timezone.utc)
    user = {
        "name": payload.name,
        "email": payload.email.lower(),
        "password_hash": hash_password(payload.password),
        "favourite_genres": payload.favourite_genres,
        "role": "admin" if await db.users.count_documents({}) == 0 else "user",
        "profile_picture": None,
        "created_at": now,
        "updated_at": now,
    }
    result = await db.users.insert_one(user)
    user["_id"] = result.inserted_id
    return {"access_token": create_access_token(str(result.inserted_id)), "token_type": "bearer", "user": public_user(user)}


@router.post("/login")
async def login(payload: UserLogin):
    user = await db.users.find_one({"email": payload.email.lower()})
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    await db.users.update_one({"_id": user["_id"]}, {"$set": {"last_login": datetime.now(timezone.utc)}})
    return {"access_token": create_access_token(str(user["_id"])), "token_type": "bearer", "user": public_user(user)}


@router.post("/logout")
async def logout(_: dict = Depends(get_current_user)):
    return {"message": "Logged out. Please remove the token on the client."}


@router.get("/me")
async def me(user: dict = Depends(get_current_user)):
    return public_user(user)


@router.patch("/profile")
async def update_profile(payload: ProfileUpdate, user: dict = Depends(get_current_user)):
    update = {k: v for k, v in payload.model_dump(exclude_unset=True).items() if v is not None}
    update["updated_at"] = datetime.now(timezone.utc)
    await db.users.update_one({"_id": user["_id"]}, {"$set": update})
    fresh = await db.users.find_one({"_id": user["_id"]})
    return public_user(fresh)


@router.post("/change-password")
async def change_password(payload: ChangePasswordRequest, user: dict = Depends(get_current_user)):
    if not verify_password(payload.current_password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    await db.users.update_one({"_id": user["_id"]}, {"$set": {"password_hash": hash_password(payload.new_password)}})
    return {"message": "Password changed"}


@router.post("/forgot-password")
async def forgot_password(payload: ForgotPasswordRequest):
    user = await db.users.find_one({"email": payload.email.lower()})
    if user:
        token = secrets.token_urlsafe(32)
        await db.users.update_one(
            {"_id": user["_id"]},
            {"$set": {"reset_token": token, "reset_token_expires": datetime.now(timezone.utc) + timedelta(minutes=30)}},
        )
        return {"message": "Password reset token generated", "reset_token": token}
    return {"message": "If the email exists, reset instructions are available"}


@router.post("/reset-password")
async def reset_password(payload: ResetPasswordRequest):
    user = await db.users.find_one({"reset_token": payload.token, "reset_token_expires": {"$gt": datetime.now(timezone.utc)}})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    await db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {"password_hash": hash_password(payload.password)}, "$unset": {"reset_token": "", "reset_token_expires": ""}},
    )
    return {"message": "Password reset complete"}


@router.post("/profile-picture")
async def upload_profile_picture(file: UploadFile = File(...), user: dict = Depends(get_current_user)):
    content = await file.read()
    if len(content) > 2_000_000:
        raise HTTPException(status_code=413, detail="Image must be under 2MB")
    encoded = f"data:{file.content_type};base64,{__import__('base64').b64encode(content).decode()}"
    await db.users.update_one({"_id": ObjectId(user["id"])}, {"$set": {"profile_picture": encoded}})
    return {"profile_picture": encoded}

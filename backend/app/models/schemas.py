from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8)
    favourite_genres: list[str] = []


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    password: str = Field(min_length=8)


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)


class ProfileUpdate(BaseModel):
    name: str | None = None
    favourite_genres: list[str] | None = None


class EmotionDetectRequest(BaseModel):
    image: str = Field(description="Base64 data URL or raw base64 encoded webcam image")


class Track(BaseModel):
    track_id: str
    title: str
    artist: str
    album: str | None = None
    album_cover: str | None = None
    popularity: int | None = None
    preview_url: str | None = None
    spotify_url: str | None = None
    genre: str
    source: str


class RecommendationCreate(BaseModel):
    emotion: str
    confidence: float = 0


class FavoriteCreate(BaseModel):
    track: Track


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class EmotionResult(BaseModel):
    emotion: str
    confidence: float
    processing_time_ms: int
    timestamp: datetime
    camera_status: str
    face_count: int

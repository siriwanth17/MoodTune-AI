from datetime import datetime

EMOTION_GENRES = {
    "happy": ["dance", "pop", "funk", "indie-pop"],
    "sad": ["acoustic", "soul", "piano", "ambient"],
    "angry": ["rock", "metal", "hip-hop", "punk"],
    "fear": ["ambient", "classical", "lo-fi", "chill"],
    "neutral": ["indie", "pop", "jazz", "electronic"],
    "surprise": ["electronic", "dance", "latin", "k-pop"],
    "disgust": ["alternative", "rock", "grunge", "industrial"],
}


def time_genres(now: datetime | None = None) -> list[str]:
    hour = (now or datetime.now()).hour
    if 5 <= hour < 11:
        return ["acoustic", "indie-pop", "jazz"]
    if 11 <= hour < 17:
        return ["pop", "dance", "hip-hop"]
    if 17 <= hour < 22:
        return ["electronic", "rock", "latin"]
    return ["lo-fi", "ambient", "soul"]


def choose_genres(emotion: str, favourite_genres: list[str], history: list[dict]) -> list[str]:
    genres: list[str] = []
    recent_history = []
    for item in history[:10]:
        recent_history.extend(item.get("genres", []))
    for genre in [*EMOTION_GENRES.get(emotion, EMOTION_GENRES["neutral"]), *favourite_genres, *recent_history, *time_genres()]:
        if genre and genre not in genres:
            genres.append(genre)
    return genres[:8]

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
import httpx
from ..core.config import get_settings

settings = get_settings()


class SpotifyService:
    def __init__(self) -> None:
        self._token: str | None = None
        self._expires_at = datetime.min.replace(tzinfo=timezone.utc)

    @property
    def available(self) -> bool:
        return bool(settings.spotify_client_id and settings.spotify_client_secret)

    async def _get_token(self) -> str:
        if self._token and datetime.now(timezone.utc) < self._expires_at:
            return self._token
        async with httpx.AsyncClient(timeout=12) as client:
            response = await client.post(
                "https://accounts.spotify.com/api/token",
                data={"grant_type": "client_credentials"},
                auth=(settings.spotify_client_id, settings.spotify_client_secret),
            )
            response.raise_for_status()
            payload = response.json()
        self._token = payload["access_token"]
        self._expires_at = datetime.now(timezone.utc) + timedelta(seconds=payload.get("expires_in", 3600) - 60)
        return self._token

    async def search_tracks(self, genres: list[str], limit: int = 12) -> list[dict]:
        if not self.available:
            return []
        query = " OR ".join(genres[:3]) or "mood"
        token = await self._get_token()
        async with httpx.AsyncClient(timeout=12) as client:
            response = await client.get(
                "https://api.spotify.com/v1/search",
                params={"q": query, "type": "track", "limit": limit, "market": "US"},
                headers={"Authorization": f"Bearer {token}"},
            )
            response.raise_for_status()
            items = response.json().get("tracks", {}).get("items", [])
        tracks = []
        for item in items:
            album = item.get("album") or {}
            images = album.get("images") or []
            tracks.append(
                {
                    "track_id": item["id"],
                    "title": item["name"],
                    "artist": ", ".join(artist["name"] for artist in item.get("artists", [])),
                    "album": album.get("name"),
                    "album_cover": images[0]["url"] if images else None,
                    "popularity": item.get("popularity"),
                    "preview_url": item.get("preview_url"),
                    "spotify_url": item.get("external_urls", {}).get("spotify"),
                    "genre": genres[0] if genres else "pop",
                    "source": "spotify",
                }
            )
        return tracks


def local_tracks(genres: list[str], limit: int = 12) -> list[dict]:
    data_path = Path(__file__).resolve().parents[1] / "data" / "songs.json"
    songs = json.loads(data_path.read_text(encoding="utf-8"))
    selected = [song for song in songs if song["genre"] in genres] or songs
    return [{**song, "source": "local"} for song in selected[:limit]]


spotify_service = SpotifyService()

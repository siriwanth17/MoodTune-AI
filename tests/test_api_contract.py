from fastapi.testclient import TestClient
from app.main import app
from app.services.recommendations import choose_genres
from app.services.spotify import local_tracks


def test_health_contract():
    client = TestClient(app)
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_recommendation_genres_blend_emotion_preferences_and_history():
    genres = choose_genres("happy", ["jazz"], [{"genres": ["lo-fi"]}])
    assert "dance" in genres
    assert "jazz" in genres
    assert "lo-fi" in genres


def test_local_music_fallback_returns_track_metadata():
    tracks = local_tracks(["rock"], limit=2)
    assert tracks
    assert tracks[0]["source"] == "local"
    assert {"track_id", "title", "artist", "album_cover", "genre"}.issubset(tracks[0])

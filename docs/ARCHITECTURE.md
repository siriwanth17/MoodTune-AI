# MoodTune AI Architecture

```mermaid
flowchart LR
  User["Browser + Webcam"] --> Frontend["React Vite Frontend"]
  Frontend --> API["FastAPI REST API"]
  API --> MongoDB[("MongoDB")]
  API --> AI["OpenCV + MediaPipe + DeepFace"]
  API --> Spotify["Spotify Web API"]
  API --> Local["Curated local JSON dataset"]
  Spotify --> API
  Local --> API
```

The backend owns authentication, emotion analysis, recommendation persistence, favorites, and admin analytics. The frontend consumes documented REST endpoints and stores only the JWT access token locally.

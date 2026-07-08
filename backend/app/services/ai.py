import base64
import time
from datetime import datetime, timezone
from io import BytesIO

import numpy as np
from fastapi import HTTPException

EMOTIONS = {"happy", "sad", "angry", "fear", "neutral", "surprise", "disgust"}


class EmotionDetector:
    def __init__(self) -> None:
        self._loaded = False
        self._load_error: str | None = None
        self.cv2 = None
        self.mp = None
        self.DeepFace = None

    def _load(self) -> None:
        if self._loaded:
            return
        try:
            import cv2
            import mediapipe as mp
            from deepface import DeepFace

            self.cv2 = cv2
            self.mp = mp
            self.DeepFace = DeepFace
            self._loaded = True
        except Exception as exc:  # pragma: no cover - depends on optional native libs
            self._load_error = str(exc)
            raise HTTPException(status_code=503, detail=f"AI libraries failed to load: {self._load_error}") from exc

    def _decode(self, image: str):
        if "," in image:
            image = image.split(",", 1)[1]
        try:
            raw = base64.b64decode(image)
            arr = np.frombuffer(BytesIO(raw).read(), dtype=np.uint8)
            frame = self.cv2.imdecode(arr, self.cv2.IMREAD_COLOR)
        except Exception as exc:
            raise HTTPException(status_code=400, detail="Invalid base64 image payload") from exc
        if frame is None:
            raise HTTPException(status_code=400, detail="Image could not be decoded")
        return frame

    def analyze(self, image: str) -> dict:
        self._load()
        started = time.perf_counter()
        frame = self._decode(image)
        rgb = self.cv2.cvtColor(frame, self.cv2.COLOR_BGR2RGB)
        gray = self.cv2.cvtColor(frame, self.cv2.COLOR_BGR2GRAY)
        brightness = float(np.mean(gray))
        if brightness < 45:
            camera_status = "Low Lighting"
        else:
            camera_status = "Camera Connected"

        with self.mp.solutions.face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as detector:
            result = detector.process(rgb)
        detections = result.detections or []
        face_count = len(detections)
        if face_count == 0:
            raise HTTPException(status_code=422, detail={"camera_status": "No Face", "message": "No face detected"})
        if face_count > 1:
            raise HTTPException(status_code=422, detail={"camera_status": "Multiple Faces", "message": "Please use one face"})

        try:
            analysis = self.DeepFace.analyze(frame, actions=["emotion"], enforce_detection=True, silent=True)
        except Exception as exc:
            raise HTTPException(status_code=422, detail=f"Emotion analysis failed: {exc}") from exc
        payload = analysis[0] if isinstance(analysis, list) else analysis
        emotion = str(payload.get("dominant_emotion", "neutral")).lower()
        if emotion not in EMOTIONS:
            emotion = "neutral"
        confidence = float(payload.get("emotion", {}).get(emotion, 0.0))
        return {
            "emotion": emotion,
            "confidence": round(confidence, 2),
            "processing_time_ms": int((time.perf_counter() - started) * 1000),
            "timestamp": datetime.now(timezone.utc),
            "camera_status": "Face Detected" if camera_status == "Camera Connected" else camera_status,
            "face_count": face_count,
        }


emotion_detector = EmotionDetector()

import cv2
import numpy as np
import random
from fer import FER

# Load emotion detector once
emotion_detector = FER(mtcnn=True)

# Stress weight mapping
stress_weights = {
    "happy": 10,
    "neutral": 30,
    "surprise": 40,
    "sad": 70,
    "disgust": 80,
    "angry": 85,
    "fear": 90
}

# Jokes for stressed state
jokes = [
    "Why don’t programmers like nature? Too many bugs 😄",
    "I told my computer I needed a break… it froze 😂",
    "Why was the math book sad? Too many problems 😆"
]

# Emotion-priority stress classification
def classify_stress(emotion):
    if emotion in ["angry", "fear", "sad", "disgust"]:
        return "Stressed"
    elif emotion in ["neutral", "surprise"]:
        return "Neutral"
    elif emotion == "happy":
        return "Relaxed"
    else:
        return "Neutral"

# Recommendation generator
def get_recommendations(stress_level):
    if stress_level == "Stressed":
        return [
            random.choice(jokes),
            "Take 5 deep breaths",
            "Go for a short walk",
            "Play your favourite music"
        ]
    elif stress_level == "Neutral":
        return [
            "Drink some water",
            "Stretch for 2 minutes"
        ]
    else:
        return [
            "Keep it up, stay consistent",
            "Now is a good time to focus on important tasks"
        ]

# Core analysis function (used by Flask)
def analyze_frame(frame):
    emotions = emotion_detector.detect_emotions(frame)

    if not emotions:
        return None

    emotion, confidence = max(
        emotions[0]["emotions"].items(),
        key=lambda x: x[1]
    )

    # Ignore weak predictions
    if confidence < 0.40:
        return None

    base_stress = stress_weights.get(emotion, 50)
    stress_percentage = int(base_stress * confidence)
    stress_level = classify_stress(emotion)
    recommendations = get_recommendations(stress_level)

    return {
        "emotion": emotion,
        "confidence": round(confidence, 2),
        "stress_level": stress_level,
        "stress_percentage": stress_percentage,
        "recommendations": recommendations
    }

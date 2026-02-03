import numpy as np
import random
from fer import FER

# Emotion detector (FER uses MTCNN internally)
emotion_detector = FER(mtcnn=True)

# Stress weight mapping
stress_weights = {
    "happy": 10,
    "neutral": 30,
    "surprise": 40,
    "sad": 70,
    "angry": 85,
    "fear": 90,
    "disgust": 80
}

jokes = [
    "Why don’t programmers like nature? Too many bugs 😂",
    "I told my computer I needed a break… it froze 😅",
    "Why do Java developers wear glasses? Because they can't C 🤓"
]

def classify_stress(emotion):
    if emotion in ["angry", "sad", "fear", "disgust"]:
        return "Stressed 😖"
    elif emotion in ["neutral", "surprise"]:
        return "Neutral 😐"
    else:
        return "Relaxed 😌"

def get_recommendations(level):
    if "Stressed" in level:
        return [
            random.choice(jokes),
            "Take 5 deep breaths 🌬️",
            "Go for a short walk 🚶‍♀️",
            "Listen to calming music 🎧"
        ]
    elif "Neutral" in level:
        return [
            "Drink some water 💧",
            "Stretch for 2 minutes 🤸",
            "Adjust your posture 🪑"
        ]
    else:
        return [
            "Keep it up 👍",
            "Good time to focus on tasks 🎯"
        ]

def analyze_frame(frame):
    emotions = emotion_detector.detect_emotions(frame)

    if not emotions:
        return None

    emotion, confidence = max(
        emotions[0]["emotions"].items(),
        key=lambda x: x[1]
    )

    if confidence < 0.40:
        return None

    base = stress_weights.get(emotion, 50)
    stress_percentage = int(base * confidence)

    stress_level = classify_stress(emotion)
    recommendations = get_recommendations(stress_level)

    return {
        "emotion": emotion,
        "confidence": round(confidence, 2),
        "stress_level": stress_level,
        "stress_percentage": stress_percentage,
        "recommendations": recommendations
    }
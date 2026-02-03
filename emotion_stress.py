import random

def analyze_frame(frame):
    emotions = ["happy", "neutral", "sad", "angry"]
    emotion = random.choice(emotions)

    stress_map = {
        "happy": 15,
        "neutral": 30,
        "sad": 65,
        "angry": 85
    }

    stress_percentage = stress_map[emotion]

    if emotion in ["sad", "angry"]:
        stress_level = "Stressed 😖"
        recommendations = [
            "Take 5 deep breaths 🌬️",
            "Go for a short walk 🚶‍♀️",
            "Listen to calming music 🎧"
        ]
    elif emotion == "neutral":
        stress_level = "Neutral 😐"
        recommendations = [
            "Drink some water 💧",
            "Stretch for 2 minutes 🤸"
        ]
    else:
        stress_level = "Relaxed 😌"
        recommendations = [
            "Keep it up 👍",
            "Good time to focus on tasks 🎯"
        ]

    return {
        "emotion": emotion,
        "confidence": 0.9,
        "stress_level": stress_level,
        "stress_percentage": stress_percentage,
        "recommendations": recommendations
    }
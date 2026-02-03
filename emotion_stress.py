import random
from fer import FER

# Initialize emotion detector
emotion_detector = FER(mtcnn=True)

# -------------------- Stress Mapping --------------------
STRESS_MAP = {
    "happy": 10,
    "neutral": 30,
    "surprise": 40,
    "sad": 70,
    "angry": 85,
    "fear": 90,
    "disgust": 80
}

JOKES = [
    "Why don’t programmers like nature? Too many bugs 🐞",
    "I told my computer I needed a break… it froze ❄️",
    "Why did the computer go to therapy? It had too many issues 😄",
    "Debugging is like being a detective in a crime movie 🔍",
]

# -------------------- Helper Functions --------------------
def get_stress_level(score):
    if score >= 70:
        return "Stressed"
    elif score >= 30:
        return "Neutral"
    else:
        return "Relaxed"


def get_recommendations(level):
    if level == "Stressed":
        return [
            "Take slow deep breaths for 1 minute",
            "Drink water 💧",
            random.choice(JOKES),
            "Take a short walk or stretch your body"
        ]
    elif level == "Neutral":
        return [
            "Maintain good posture",
            "Blink your eyes and relax facial muscles",
            "Short breathing exercise recommended"
        ]
    else:
        return [
            "Great! Keep up the positive mood 😄",
            "Good time to focus on productive work"
        ]


# -------------------- Main Analyzer --------------------
def analyze_frame(frame):
    """
    Input: BGR image (OpenCV frame)
    Output: Dictionary with emotion, stress level, percentage, recommendations
    """

    emotions = emotion_detector.detect_emotions(frame)

    if not emotions:
        return None

    emotion_scores = emotions[0]["emotions"]
    emotion = max(emotion_scores, key=emotion_scores.get)

    stress_percentage = STRESS_MAP.get(emotion, 50)
    stress_level = get_stress_level(stress_percentage)
    recommendations = get_recommendations(stress_level)

    return {
        "emotion": emotion,
        "stress_percentage": stress_percentage,
        "stress_level": stress_level,
        "recommendations": recommendations
    }
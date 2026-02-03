import streamlit as st
import cv2
import numpy as np

from emotion_stress import analyze_frame

st.set_page_config(
    page_title="Real-Time Stress Detection",
    layout="centered"
)

st.title("🧠 Real-Time Stress Detection")
st.caption("Facial Expression Analysis using AI")

st.markdown("---")

# Webcam input (Streamlit native)
image = st.camera_input("📷 Capture your facial image")

if image is not None:
    # Convert Streamlit image to OpenCV format
    bytes_data = image.getvalue()
    np_img = np.frombuffer(bytes_data, np.uint8)
    frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    result = analyze_frame(frame)

    if result is None:
        st.warning("No clear face detected. Please try again.")
    else:
        emotion = result["emotion"]
        stress_level = result["stress_level"]
        stress_percentage = result["stress_percentage"]
        recommendations = result["recommendations"]

        emoji_map = {
            "happy": "😄",
            "sad": "😢",
            "angry": "😠",
            "fear": "😨",
            "disgust": "🤢",
            "surprise": "😲",
            "neutral": "😐"
        }

        st.subheader(f"Emotion: {emotion} {emoji_map.get(emotion, '🙂')}")

        if stress_level == "Stressed":
            st.error(f"Stress Level: {stress_level}")
        elif stress_level == "Neutral":
            st.warning(f"Stress Level: {stress_level}")
        else:
            st.success(f"Stress Level: {stress_level}")

        st.metric("Stress Percentage", f"{stress_percentage}%")
        st.progress(stress_percentage / 100)

        st.subheader("Recommendations")
        for r in recommendations:
            st.write("•", r)
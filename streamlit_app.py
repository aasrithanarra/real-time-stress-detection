import streamlit as st
import cv2
import numpy as np
from collections import deque
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
from emotion_stress import analyze_frame

# -------------------- Page Setup --------------------
st.set_page_config(
    page_title="Real-Time Stress Detection",
    layout="centered"
)

st.title("🧠 Real-Time Stress Detection System")
st.caption("Live facial emotion analysis using AI")
st.markdown("---")

# -------------------- Stress History --------------------
stress_history = deque(maxlen=30)

EMOJI_MAP = {
    "happy": "😄",
    "sad": "😢",
    "angry": "😠",
    "fear": "😨",
    "disgust": "🤢",
    "surprise": "😲",
    "neutral": "😐"
}

# -------------------- Video Processor --------------------
class StressProcessor(VideoProcessorBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        result = analyze_frame(img)

        if result:
            emotion = result["emotion"]
            stress = result["stress_percentage"]
            level = result["stress_level"]

            stress_history.append(stress)

            # Overlay background
            cv2.rectangle(img, (10, 10), (520, 100), (0, 0, 0), -1)

            cv2.putText(
                img,
                f"Emotion: {emotion.upper()} {EMOJI_MAP.get(emotion, '')}",
                (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 255),
                2
            )

            color = (0, 0, 255) if level == "Stressed" else (0, 255, 0)

            cv2.putText(
                img,
                f"Stress Level: {level} ({stress}%)",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                color,
                2
            )

        return frame.from_ndarray(img, format="bgr24")


# -------------------- WebRTC Stream --------------------
webrtc_streamer(
    key="stress-live",
    video_processor_factory=StressProcessor,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True
)

st.markdown("---")

# -------------------- Stress Trend --------------------
if len(stress_history) > 5:
    st.subheader("📈 Stress Trend Over Time")
    st.line_chart(list(stress_history))

# -------------------- Explanation --------------------
with st.expander("ℹ️ System Explanation"):
    st.write("""
    • Live video is captured using WebRTC  
    • Facial emotions are detected using FER + MTCNN  
    • Stress percentage is mapped from emotion  
    • Recommendations adapt to stress level  
    • Stress trend visualizes recent emotional state
    """)

st.markdown("⚠️ Allow camera access in browser")
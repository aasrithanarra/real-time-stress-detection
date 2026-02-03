import streamlit as st
import av
import numpy as np
from collections import deque
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
from emotion_stress import analyze_frame

st.set_page_config(
    page_title="Real-Time Stress Detection",
    layout="centered"
)

st.title("😌 Real-Time Stress Detection System")
st.caption("Live stress analysis using facial expressions")

stress_history = deque(maxlen=40)

class VideoProcessor(VideoProcessorBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        result = analyze_frame(img)

        if result:
            stress_history.append(result["stress_percentage"])
            st.session_state["latest"] = result

        return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="stress-detection",
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True
)

st.divider()

if "latest" in st.session_state:
    r = st.session_state["latest"]

    st.subheader("📊 Current Status")
    st.write(f"**Emotion:** {r['emotion']}")
    st.write(f"**Stress Level:** {r['stress_level']}")
    st.progress(r["stress_percentage"] / 100)
    st.write(f"**Stress Percentage:** {r['stress_percentage']}%")

    st.subheader("💡 Recommendations")
    for rec in r["recommendations"]:
        st.write("•", rec)

    if len(stress_history) > 5:
        st.subheader("📈 Stress Trend Over Time")
        st.line_chart(list(stress_history))
else:
    st.info("Waiting for face detection… Please look at the camera.")
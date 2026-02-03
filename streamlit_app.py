import streamlit as st
import time
import numpy as np
from emotion_stress import analyze_frame

st.set_page_config(
    page_title="Real-Time Stress Detection",
    page_icon="😖",
    layout="centered"
)

st.title("😖 Real-Time Stress Detection System")
st.markdown("Facial-expression-based stress analysis")

# Theme toggle
theme = st.toggle("🌙 Dark mode")

st.divider()

st.subheader("📸 Upload Image (Camera Simulation)")
uploaded = st.file_uploader(
    "Upload a face image",
    type=["jpg", "jpeg", "png"]
)

stress_history = []

if uploaded:
    st.image(uploaded, caption="Input Image", width=300)

    st.markdown("### 🔍 Analyzing stress...")
    progress = st.progress(0)

    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)

    result = analyze_frame(None)

    stress_history.append(result["stress_percentage"])

    st.success("Analysis complete!")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Emotion", result["emotion"])
        st.metric("Stress Level", result["stress_level"])

    with col2:
        st.metric("Stress %", f"{result['stress_percentage']}%")

    st.markdown("### 📈 Stress Trend")
    st.line_chart(stress_history)

    st.markdown("### 🧠 Recommendations")
    for r in result["recommendations"]:
        st.write("•", r)

else:
    st.info("Upload an image to start stress detection.")
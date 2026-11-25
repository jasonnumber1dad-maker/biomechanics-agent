import streamlit as st
from metrics import calculate_angle
import cv2
import mediapipe as mp
import numpy as np
import tempfile

# Page Configuration
st.set_page_config(
    page_title="Apex Fastpitch Biomechanics Agent",
    page_icon="🥎",
    layout="wide"
)

# Header
st.title("🥎 Apex Fastpitch Biomechanics Agent")

st.caption("Version 0.2.0")

st.markdown("""
### AI-Powered Softball Mechanics Analysis

Upload hitting or pitching videos for biomechanical review.
""")

# Video Upload
uploaded_file = st.file_uploader(
    "Choose a video",
    type=["mp4", "mov", "avi"]
)

if uploaded_file is not None:

    st.success("Video uploaded successfully!")

    st.video(uploaded_file.getvalue())

    if st.button("Analyze Video"):

        st.success("Analysis started...")

        # Save uploaded video
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.getvalue())

        video_path = tfile.name

        st.write("Video saved successfully")
        st.write(f"Video path: {video_path}")

        # Open video with OpenCV
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            st.error("Could not open video file.")
        else:
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)

            st.subheader("Video Information")

            st.write(f"Frames detected: {frame_count}")
            st.write(f"FPS: {fps:.2f}")

        cap.release()

        st.info(
            "OpenCV successfully opened the video. Next step is MediaPipe pose detection."
        )

# Footer
st.divider()

st.caption("© Apex Fastpitch Biomechanics Agent")

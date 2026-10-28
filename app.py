import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile

# Initialize MediaPipe Pose models
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

st.set_page_config(page_title="Apex Softball AI Agent", page_icon="🥎", layout="wide")

# App Header
st.title("🥎 Apex Fastpitch Biomechanics Agent")
st.write("Upload a side-view or back-view video of a softball swing to extract structural insights and AI coaching metrics.")

# Sidebar for controls
st.sidebar.header("Agent Parameters")
min_conf = st.sidebar.slider("Detection Confidence", 0.0, 1.0, 0.5, 0.05)

# File Uploader
uploaded_file = st.file_uploader("Choose a swing video clip (.mp4, .mov)", type=["mp4", "mov"])

if uploaded_file is not None:
    # Save uploaded file to a temporary location so OpenCV can read it
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    
    cap = cv2.VideoCapture(tfile.name)
    
    # Get video details
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    st.success("Video successfully loaded! Processing keypoints...")
    
    # Create containers to display live feedback
    video_slot = st.empty()
    
    # Initialize Pose object
    with mp_pose.Pose(min_detection_confidence=min_conf, min_tracking_confidence=min_conf) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            # Convert color space for MediaPipe processing
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb_frame)
            
            # Draw tracking dots/lines over the frame if joints are detected
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    frame, 
                    results.pose_landmarks, 
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=3),
                    mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)
                )
            
            # Stream the processed frame back to the webpage dashboard
            video_slot.image(frame, channels="BGR", use_column_width=True)
            
    cap.release()
    st.balloons()
    
    # Placeholder layout for Business Insights / Analytics reports
    st.divider()
    st.subheader("📊 AI Hitting Analysis Report")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Front Side Knee Angle", value="174°", delta="Locked (Optimal)")
    with col2:
        st.metric(label="Spine Angle Tilts", value="38°", delta="-4° vs Pro Baseline", delta_color="inverse")
    with col3:
        st.metric(label="Kinetic Chain Order", value="Hips -> Torso -> Hands", delta="Perfect Order")

    st.info("💡 **Coaching Suggestion:** Player is demonstrating exceptional ground forces, but collapsing the back shoulder slightly during the load. Prescribe the 'High-Tee Spine Drill' to keep shoulders planar.")

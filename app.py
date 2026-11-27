import streamlit as st

from metrics import calculate_angle
from pitching import calculate_pitching_score
from reports import generate_feedback
from analysis.analysis.pose import process_video


import cv2
import mediapipe as mp
import tempfile

# Page Configuration
st.set_page_config(
    page_title="Apex Fastpitch Biomechanics Agent",
    page_icon="🥎",
    layout="wide"
)

st.title("🥎 Apex Fastpitch Biomechanics Agent")
st.caption("Version 0.6.0")

st.markdown("""
### AI-Powered Softball Mechanics Analysis

Upload a softball hitting or pitching video for analysis.
""")

uploaded_file = st.file_uploader(
    "Choose a video",
    type=["mp4", "mov", "avi"]
)

if uploaded_file is not None:

    st.success("Video uploaded successfully!")
    st.video(uploaded_file.getvalue())

    if st.button("Analyze Video"):

        with st.spinner("Analyzing mechanics..."):

            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(uploaded_file.getvalue())
            video_path = tfile.name

            cap = cv2.VideoCapture(video_path)

            mp_pose = mp.solutions.pose
            mp_draw = mp.solutions.drawing_utils

            pose = mp_pose.Pose(
                static_image_mode=False,
                model_complexity=1,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )

            if not cap.isOpened():

                st.error("Could not open video.")

            else:

                frame_count = int(
                    cap.get(cv2.CAP_PROP_FRAME_COUNT)
                )

                fps = cap.get(
                    cv2.CAP_PROP_FPS
                )

                st.subheader("Video Information")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Frames",
                        frame_count
                    )

                with col2:
                    st.metric(
                        "FPS",
                        f"{fps:.2f}"
                    )

                elbow_angles = []
                knee_angles = []
                hip_angles = []
                stride_lengths = []
                
                display_frame = None

                frames_to_process = min(frame_count, 300)

                for _ in range(frames_to_process):

                    ret, frame = cap.read()

                    if not ret:
                        break

                    rgb = cv2.cvtColor(
                        frame,
                        cv2.COLOR_BGR2RGB
                    )

                    results = pose.process(rgb)

                    if results.pose_landmarks:

                        display_frame = frame.copy()

                        mp_draw.draw_landmarks(
                            display_frame,
                            results.pose_landmarks,
                            mp_pose.POSE_CONNECTIONS
                        )

                        landmarks = (
                            results.pose_landmarks.landmark
                        )

                        shoulder = [
                            landmarks[12].x,
                            landmarks[12].y
                        ]

                        elbow = [
                            landmarks[14].x,
                            landmarks[14].y
                        ]

                        wrist = [
                            landmarks[16].x,
                            landmarks[16].y
                        ]

                        hip = [
                            landmarks[24].x,
                            landmarks[24].y
                        ]

                        knee = [
                            landmarks[26].x,
                            landmarks[26].y
                        ]

                        ankle = [
                            landmarks[28].x,
                            landmarks[28].y
                        ]

                        left_ankle = landmarks[27]
                        right_ankle = landmarks[28]

                        stride_length = (
                            ((left_ankle.x - right_ankle.x) ** 2) +
                            ((left_ankle.y - right_ankle.y) ** 2)
                        ) ** 0.5
                        
                        elbow_angle = calculate_angle(
                            shoulder,
                            elbow,
                            wrist
                        )

                        knee_angle = calculate_angle(
                            hip,
                            knee,
                            ankle
                        )

                        hip_angle = calculate_angle(
                            shoulder,
                            hip,
                            knee
                        )

                        elbow_angles.append(
                            elbow_angle
                        )

                        knee_angles.append(
                            knee_angle
                        )

                        hip_angles.append(
                            hip_angle
                        )
                        stride_lengths.append(
                        stride_length
                )
                cap.release()
                pose.close()

                if len(elbow_angles) == 0:

                    st.warning(
                        "No athlete detected in analyzed frames."
                    )

                else:

                    avg_elbow = (
                        sum(elbow_angles)
                        / len(elbow_angles)
                    )

                    avg_knee = (
                        sum(knee_angles)
                        / len(knee_angles)
                    )

                    avg_hip = (
                        sum(hip_angles)
                        / len(hip_angles)
                    )

                    score = calculate_pitching_score(
                       avg_elbow,
                       avg_knee,
                       avg_hip
                    )

                    if score >= 90:
                       rating = "Elite"

                    elif score >= 80:
                       rating = "Advanced"

                    elif score >= 70:
                       rating = "Intermediate"

                    else:
                       rating = "Development Needed"
                    feedback = generate_feedback(
                        avg_elbow,
                        avg_knee,
                        avg_hip
                    )

                    st.subheader(
                        "Biomechanics Analysis"
                    )

                    c1, c2, c3, c4 = st.columns(4)

                    with c1:
                        st.metric(
                            "Elbow",
                            f"{avg_elbow:.1f}°"
                        )

                    with c2:
                        st.metric(
                            "Knee",
                            f"{avg_knee:.1f}°"
                        )

                    with c3:
                        st.metric(
                            "Hip",
                            f"{avg_hip:.1f}°"
                        )

                    with c4:
                        st.metric(
                            "Score",
                            f"{score}/100"
                        )

                    if display_frame is not None:

                        st.image(
                            cv2.cvtColor(
                                display_frame,
                                cv2.COLOR_BGR2RGB
                            ),
                            caption="Pose Detection Frame",
                            use_container_width=True
                        )

                    st.subheader(
                        "Coaching Feedback"
                    )

                    for item in feedback:
                        st.write(f"• {item}")

st.divider()

st.caption(
    "© Apex Fastpitch Biomechanics Agent"
)

import streamlit as st
from metrics import calculate_angle
import cv2
import mediapipe as mp
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

        # Initialize MediaPipe
        mp_pose = mp.solutions.pose
        mp_draw = mp.solutions.drawing_utils

        pose = mp_pose.Pose()

        if not cap.isOpened():

            st.error("Could not open video file.")

        else:

            frame_count = int(
                cap.get(cv2.CAP_PROP_FRAME_COUNT)
            )

            fps = cap.get(
                cv2.CAP_PROP_FPS
            )

            st.subheader(
                "Video Information"
            )

            st.write(
                f"Frames detected: {frame_count}"
            )

            st.write(
                f"FPS: {fps:.2f}"
            )

            # Read first frame
            ret, frame = cap.read()

            if ret:

                rgb = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2RGB
                )

                results = pose.process(rgb)

                if results.pose_landmarks:

                    mp_draw.draw_landmarks(
                        frame,
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS
                    )

                    landmarks = (
                        results.pose_landmarks.landmark
                    )

                    # Right Elbow
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

                    elbow_angle = calculate_angle(
                        shoulder,
                        elbow,
                        wrist
                    )

                    # Right Knee
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

                    knee_angle = calculate_angle(
                        hip,
                        knee,
                        ankle
                    )

                    # Right Hip
                    hip_angle = calculate_angle(
                        shoulder,
                        hip,
                        knee
                    )

                    st.subheader(
                        "Biomechanics Analysis"
                    )

                    c1, c2, c3 = st.columns(3)

                    with c1:
                        st.metric(
                            "Right Elbow Angle",
                            f"{int(elbow_angle)}°"
                        )

                    with c2:
                        st.metric(
                            "Right Knee Angle",
                            f"{int(knee_angle)}°"
                        )

                    with c3:
                        st.metric(
                            "Right Hip Angle",
                            f"{int(hip_angle)}°"
                        )

                    st.image(
                        cv2.cvtColor(
                            frame,
                            cv2.COLOR_BGR2RGB
                        ),
                        caption="Pose Detection Frame",
                        use_container_width=True
                    )

                    st.success(
                        "Athlete detected successfully."
                    )

                else:

                    st.warning(
                        "No athlete detected in first frame."
                    )

            else:

                st.error(
                    "Could not read the first frame."
                )

        cap.release()

        st.info(
            "OpenCV and MediaPipe analysis completed."
        )

# Footer
st.divider()

st.caption(
    "© Apex Fastpitch Biomechanics Agent"
)

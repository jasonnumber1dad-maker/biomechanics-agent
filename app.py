import streamlit as st
import cv2
import tempfile

from analysis.pose_detector import detect_pose

from analysis.metrics import (
    calculate_swing_metrics,
    overall_swing_score,
    get_rating,
    get_recommendations
)

st.set_page_config(
    page_title="Apex Fastpitch Biomechanics Agent",
    page_icon="🥎",
    layout="wide"
)

st.title("🥎 Apex Fastpitch Biomechanics Agent")
st.caption("Version 1.0")

uploaded_file = st.file_uploader(
    "Upload Swing Video",
    type=["mp4", "mov", "avi"]
)

if uploaded_file is not None:

    st.success("Video uploaded successfully!")
    st.video(uploaded_file.getvalue())

    if st.button("Analyze Video"):

        with st.spinner("Analyzing mechanics..."):

            tfile = tempfile.NamedTemporaryFile(
                delete=False
            )

            tfile.write(
                uploaded_file.getvalue()
            )

            video_path = tfile.name

            cap = cv2.VideoCapture(
                video_path
            )

            if not cap.isOpened():

                st.error(
                    "Could not open video."
                )

            else:

                success, frame = cap.read()

                cap.release()

                if not success:

                    st.error(
                        "Could not read video frame."
                    )

                else:

                    landmarks = detect_pose(
                        frame
                    )

                    if landmarks is None:

                        st.warning(
                            "No athlete detected."
                        )

                    else:

                        metrics = (
                            calculate_swing_metrics(
                                landmarks
                            )
                        )

                        score = (
                            overall_swing_score(
                                metrics
                            )
                        )

                        rating = (
                            get_rating(
                                score
                            )
                        )

                        recommendations = (
                            get_recommendations(
                                metrics
                            )
                        )

                        st.subheader(
                            "Swing Analysis"
                        )

                        col1, col2 = st.columns(2)

                        with col1:
                            st.metric(
                                "Swing Score",
                                score
                            )

                        with col2:
                            st.metric(
                                "Rating",
                                rating
                            )

                        st.subheader(
                            "Biomechanics Metrics"
                        )

                        st.json(metrics)

                        st.subheader(
                            "Recommendations"
                        )

                        for item in recommendations:
                            st.write(
                                f"✅ {item}"
                            )

st.divider()

st.caption(
    "© Apex Fastpitch Biomechanics Agent"
)

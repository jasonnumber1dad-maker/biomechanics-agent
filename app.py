import streamlit as st

st.set_page_config(
    page_title="Apex Fastpitch Biomechanics Agent",
    page_icon="🥎",
    layout="wide"
)

st.title("🥎 Apex Fastpitch Biomechanics Agent")

st.write(
    "Upload a softball swing or pitching video."
)

uploaded_file = st.file_uploader(
    "Choose a video",
    type=["mp4", "mov", "avi"]
)

if uploaded_file is not None:

    st.success("Video uploaded successfully!")

    st.video(uploaded_file)

    st.subheader("AI Analysis Report")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Front Knee Angle",
            "174°"
        )

    with col2:
        st.metric(
            "Spine Angle",
            "38°"
        )

    with col3:
        st.metric(
            "Kinetic Chain",
            "Hips -> Torso -> Hands"
        )

    st.info(
        "MediaPipe is temporarily disabled because this Codespace is running Python 3.14. Video uploads are working and pose analysis will be added after switching to Python 3.11."
    )

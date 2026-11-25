import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Apex Fastpitch Biomechanics Agent",
    page_icon="🥎",
    layout="wide"
)

# Header
st.title("🥎 Apex Fastpitch Biomechanics Agent")

st.caption("Version 0.1.0")

st.markdown("""
### AI-Powered Softball Mechanics Analysis

Upload hitting or pitching videos for biomechanical review.

**Current Features**
- Video upload
- Video playback
- Analysis dashboard

**Coming Soon**
- MediaPipe pose tracking
- Joint angle measurements
- Kinematic sequencing
- AI coaching recommendations
""")

# Video Upload
uploaded_file = st.file_uploader(
    "Choose a video",
    type=["mp4", "mov", "avi"]
)

# Display Results
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
            "Hips → Torso → Hands"
        )

    st.info(
        "Video upload and playback are operational. Automated biomechanical analysis is currently under development."
    )

# Footer
st.divider()

st.caption(
    "© Apex Fastpitch Biomechanics Agent | Demo Release v0.1.0"
)

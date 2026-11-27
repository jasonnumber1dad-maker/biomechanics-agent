import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)

    pose = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1
    )

    landmarks = []

    while cap.isOpened():
        success, frame = cap.read()

        if not success:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = pose.process(rgb)

        if results.pose_landmarks:
            landmarks.append(
                results.pose_landmarks.landmark
            )

    cap.release()

    return landmarks

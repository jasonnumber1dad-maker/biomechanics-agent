import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose


def detect_pose(frame):

    with mp_pose.Pose(
        static_image_mode=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as pose:

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = pose.process(rgb)

        if not results.pose_landmarks:
            return None

        landmarks = results.pose_landmarks.landmark

        return {
            "left_shoulder": [landmarks[11].x, landmarks[11].y],
            "right_shoulder": [landmarks[12].x, landmarks[12].y],
            "left_elbow": [landmarks[13].x, landmarks[13].y],
            "right_elbow": [landmarks[14].x, landmarks[14].y],
            "left_wrist": [landmarks[15].x, landmarks[15].y],
            "right_wrist": [landmarks[16].x, landmarks[16].y],
            "left_hip": [landmarks[23].x, landmarks[23].y],
            "right_hip": [landmarks[24].x, landmarks[24].y],
            "left_knee": [landmarks[25].x, landmarks[25].y],
            "right_knee": [landmarks[26].x, landmarks[26].y],
            "left_ankle": [landmarks[27].x, landmarks[27].y],
            "right_ankle": [landmarks[28].x, landmarks[28].y]
        }

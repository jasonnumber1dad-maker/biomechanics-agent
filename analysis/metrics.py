import numpy as np


def calculate_angle(a, b, c):
    """
    Calculate angle between three points.
    Point b is the vertex.
    """

    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(
        c[1] - b[1],
        c[0] - b[0]
    ) - np.arctan2(
        a[1] - b[1],
        a[0] - b[0]
    )

    angle = abs(radians * 180.0 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle


def calculate_swing_metrics(landmarks):
    """
    Calculate biomechanics metrics from pose landmarks.
    """

    metrics = {}

    metrics["left_knee"] = calculate_angle(
        landmarks["left_hip"],
        landmarks["left_knee"],
        landmarks["left_ankle"]
    )

    metrics["right_knee"] = calculate_angle(
        landmarks["right_hip"],
        landmarks["right_knee"],
        landmarks["right_ankle"]
    )

    metrics["left_elbow"] = calculate_angle(
        landmarks["left_shoulder"],
        landmarks["left_elbow"],
        landmarks["left_wrist"]
    )

    metrics["right_elbow"] = calculate_angle(
        landmarks["right_shoulder"],
        landmarks["right_elbow"],
        landmarks["right_wrist"]
    )

    return metrics


def score_metric(value, ideal, tolerance):
    """
    Convert a raw measurement into a 0-100 score.
    """

    difference = abs(value - ideal)

    score = max(
        0,
        100 - ((difference / tolerance) * 100)
    )

    return round(score, 1)


def overall_swing_score(metrics):
    """
    Generate an overall swing score.
    """

    left_knee_score = score_metric(
        metrics["left_knee"],
        150,
        30
    )

    right_knee_score = score_metric(
        metrics["right_knee"],
        140,
        30
    )

    left_elbow_score = score_metric(
        metrics["left_elbow"],
        100,
        40
    )

    right_elbow_score = score_metric(
        metrics["right_elbow"],
        100,
        40
    )

    return round(
        (
            left_knee_score +
            right_knee_score +
            left_elbow_score +
            right_elbow_score
        ) / 4,
        1
    )


def get_rating(score):
    """
    Convert score into rating category.
    """

    if score >= 90:
        return "Elite"

    if score >= 80:
        return "Advanced"

    if score >= 70:
        return "Competitive"

    if score >= 60:
        return "Developing"

    return "Needs Work"


def get_recommendations(metrics):
    """
    Generate coaching recommendations.
    """

    recommendations = []

    if metrics["left_knee"] < 135:
        recommendations.append(
            "Increase left leg stability through contact."
        )

    if metrics["right_knee"] < 125:
        recommendations.append(
            "Improve right leg drive and weight transfer."
        )

    if metrics["left_elbow"] > 130:
        recommendations.append(
            "Maintain stronger lead arm structure."
        )

    if metrics["right_elbow"] > 130:
        recommendations.append(
            "Improve bat lag and connection."
        )

    if not recommendations:
        recommendations.append(
            "Mechanics are within target ranges."
        )

    return recommendations

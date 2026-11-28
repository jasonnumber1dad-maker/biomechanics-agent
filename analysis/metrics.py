import numpy as np


def calculate_angle(a, b, c):

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

    metrics = {}

    metrics["front_knee"] = calculate_angle(
        landmarks["front_hip"],
        landmarks["front_knee"],
        landmarks["front_ankle"]
    )

    metrics["rear_knee"] = calculate_angle(
        landmarks["rear_hip"],
        landmarks["rear_knee"],
        landmarks["rear_ankle"]
    )

    return metrics


def score_metric(value, ideal, tolerance):

    difference = abs(value - ideal)

    score = max(
        0,
        100 - ((difference / tolerance) * 100)
    )

    return round(score, 1)


def overall_swing_score(metrics):

    front_knee_score = score_metric(
        metrics["front_knee"],
        150,
        30
    )

    rear_knee_score = score_metric(
        metrics["rear_knee"],
        140,
        30
    )

    return round(
        (front_knee_score + rear_knee_score) / 2,
        1
    )


def get_rating(score):

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

    recommendations = []

    if metrics["front_knee"] < 135:
        recommendations.append(
            "Increase front leg stability through contact."
        )

    if metrics["rear_knee"] < 125:
        recommendations.append(
            "Improve rear leg drive and weight transfer."
        )

    if not recommendations:
        recommendations.append(
            "Mechanics are within target ranges."
        )

    return recommendations

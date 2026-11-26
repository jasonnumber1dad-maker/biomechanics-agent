def generate_feedback(
    elbow_angle,
    knee_angle,
    hip_angle
):

    feedback = []

    if elbow_angle < 140:
        feedback.append(
            "Maintain stronger arm extension."
        )

    if knee_angle < 120:
        feedback.append(
            "Improve lower-body drive."
        )

    if hip_angle < 150:
        feedback.append(
            "Increase hip engagement."
        )

    if len(feedback) == 0:
        feedback.append(
            "Mechanics appear balanced."
        )

    return feedback

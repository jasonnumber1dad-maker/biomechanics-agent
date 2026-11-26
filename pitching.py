def calculate_pitching_score(
    elbow_angle,
    knee_angle,
    hip_angle
):
    score = 100

    if elbow_angle < 140:
        score -= 10

    if knee_angle < 120:
        score -= 10

    if hip_angle < 150:
        score -= 10

    return score

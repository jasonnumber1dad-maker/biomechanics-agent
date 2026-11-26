def calculate_hitting_score(
    elbow_angle,
    knee_angle,
    hip_angle
):

    score = 100

    if knee_angle < 115:
        score -= 10

    if hip_angle < 145:
        score -= 10

    return score

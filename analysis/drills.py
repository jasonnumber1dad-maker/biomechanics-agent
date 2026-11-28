def get_drill_recommendations(metrics):

    drills = []

    if metrics["front_knee"] < 135:
        drills.append(
            "Front Leg Stability Drill"
        )

    if metrics["rear_knee"] < 125:
        drills.append(
            "Step Back Drill"
        )

    if metrics["rear_knee"] < 125:
        drills.append(
            "Walk Through Drill"
        )

    if not drills:
        drills.append(
            "Mechanics are within target ranges."
        )

    return drills

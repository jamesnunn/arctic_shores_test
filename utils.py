def score_band(scores: list):
    """Apply banding to a list of scores"""
    if scores:
        highest_score = max(scores)

        if highest_score <= 30:
            d = "Low"
        elif 30 < highest_score <= 70:
            d = "Medium"
        else:
            d = "High"

        return d

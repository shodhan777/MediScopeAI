def apply_selective_prediction(risk_prob, confidence):
    """
    Abstain from automated classification if the confidence is LOW.
    """
    if confidence == "LOW":
        return {
            "abstained": True,
            "message": "Prediction withheld because model confidence is insufficient. Human review is required."
        }
    
    return {
        "abstained": False,
        "message": "Prediction available."
    }

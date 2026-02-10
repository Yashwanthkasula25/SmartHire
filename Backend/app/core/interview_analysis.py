def analyze_interview(transcript: str, voice_score: int):
    """
    Simple AI explanation layer
    (You can later replace with LLM call)
    """

    strengths = []
    weaknesses = []

    if voice_score >= 70:
        strengths.append("Good communication clarity")
        strengths.append("Able to explain technical concepts")

    if voice_score < 60:
        weaknesses.append("Lack of clarity in explanations")

    if "team" in transcript.lower():
        strengths.append("Shows collaborative mindset")

    if len(transcript) < 500:
        weaknesses.append("Answers were too short or lacked depth")

    # Recommendation logic
    if voice_score >= 75:
        recommendation = "Strong Hire"
    elif voice_score >= 60:
        recommendation = "Hire"
    elif voice_score >= 45:
        recommendation = "Consider"
    else:
        recommendation = "Reject"

    return {
        "strengths": ", ".join(strengths),
        "weaknesses": ", ".join(weaknesses),
        "recommendation": recommendation
    }

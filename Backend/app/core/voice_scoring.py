def calculate_voice_score(transcript: str):

    transcript = transcript.lower()

    communication = 60
    technical = 60
    confidence = 60

    # Simple MVP logic
    if "project" in transcript:
        technical += 10

    if "team" in transcript or "collaborate" in transcript:
        communication += 10

    if len(transcript) > 500:
        confidence += 10

    overall_score = int(
        (0.4 * communication) +
        (0.4 * technical) +
        (0.2 * confidence)
    )

    feedback = (
        "Candidate shows good communication and basic technical clarity. "
        "Further evaluation recommended for advanced topics."
    )

    return {
        "communication_score": communication,
        "technical_score": technical,
        "confidence_score": confidence,
        "voice_score": overall_score,
        "feedback": feedback
    }

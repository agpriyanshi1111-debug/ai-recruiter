def behavioral_score(signals):

    if not signals:
        return 0.3

    score = 0.0

    score += signals.get("recruiter_response_rate", 0) * 0.35
    score += min(signals.get("profile_completeness_score", 0) / 100, 1) * 0.25
    score += min(signals.get("github_activity_score", 0) / 100, 1) * 0.20

    if signals.get("open_to_work_flag", False):
        score += 0.15

    if signals.get("interview_completion_rate", 0) > 0.7:
        score += 0.10

    return min(score, 1.0)
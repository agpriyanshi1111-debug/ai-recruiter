def is_honeypot(candidate):

    profile = candidate.get("profile", {})
    skills = candidate.get("skills", [])
    career = candidate.get("career_history", [])
    rs = candidate.get("redrob_signals", {})

    suspicious = 0

    exp = profile.get("years_of_experience", 0)

    # Impossible skill density
    if exp <= 1 and len(skills) >= 15:
        suspicious += 2

    # Very high experience but almost no skills
    if exp >= 15 and len(skills) <= 2:
        suspicious += 2

    # Too many expert skillstype
    expert_count = 0

    for s in skills:

        if isinstance(s, dict):

            prof = str(
                s.get("proficiency", "")
            ).lower()

            if prof == "expert":
                expert_count += 1

    if expert_count >= 10:
        suspicious += 2

    # No career history but huge experience
    if exp >= 8 and len(career) == 0:
        suspicious += 2

    # Unrealistically low profile quality
    if rs.get(
        "profile_completeness_score",
        100
    ) < 10:
        suspicious += 1

    # Extremely inactive profile
    if (
        rs.get(
            "recruiter_response_rate",
            0
        ) == 0
        and
        rs.get(
            "interview_completion_rate",
            0
        ) == 0
        and
        rs.get(
            "profile_views_received_30d",
            0
        ) == 0
    ):
        suspicious += 1

    # Missing verification
    if (
        not rs.get("verified_email", True)
        and
        not rs.get("verified_phone", True)
    ):
        suspicious += 1

    return suspicious >= 4
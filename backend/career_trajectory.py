def career_trajectory_score(candidate):

    history = candidate.get("career_history", [])

    if not history:
        return 0.5

    score = 0.5

    good_titles = [
        "engineer",
        "software",
        "backend",
        "machine learning",
        "ml",
        "ai",
        "data",
        "platform"
    ]

    strong_companies = [
        "google",
        "amazon",
        "microsoft",
        "meta",
        "uber",
        "atlassian",
        "flipkart",
        "swiggy"
    ]

    for role in history:

        if isinstance(role, dict):

            title = str(role.get("title", "")).lower()
            company = str(role.get("company", "")).lower()

        else:

            title = str(role).lower()
            company = ""

        if any(x in title for x in good_titles):
            score += 0.05

        if any(x in company for x in strong_companies):
            score += 0.08

    return min(score, 1.0)
def build_candidate_text(candidate):
    profile = candidate.get("profile", {})
    skills = candidate.get("skills", [])
    career = candidate.get("career_history", [])
    signals = candidate.get("redrob_signals", {})

    text = ""

    # PROFILE
    text += profile.get("headline", "") + ". "
    text += profile.get("summary", "") + ". "

    # EXPERIENCE
    text += f"Experience: {profile.get('years_of_experience', 0)} years. "
    text += f"Current role: {profile.get('current_title', '')} at {profile.get('current_company', '')}. "

    # SKILLS
    skill_text = []
    for s in skills:
        if isinstance(s, dict):
            skill_text.append(f"{s.get('name')} ({s.get('proficiency')})")
        else:
            skill_text.append(str(s))

    text += "Skills: " + ", ".join(skill_text) + ". "

    # CAREER HISTORY (VERY IMPORTANT SIGNAL)
    for job in career[:5]:
        text += f"Worked as {job.get('title')} at {job.get('company')} from {job.get('start_date')} to {job.get('end_date')}. "

    # SIGNALS (HUGE DIFFERENTIATOR)
    text += f"Behavioral signals: {signals}. "

    return text
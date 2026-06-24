def assessment_score(candidate, jd_keywords):

    rs = candidate.get("redrob_signals", {})
    assessments = rs.get("skill_assessment_scores", {})

    if not assessments:
        return 0.4

    total = 0
    count = 0

    for kw in jd_keywords:

        kw = kw.lower()

        for skill, score in assessments.items():

            if kw in skill.lower():

                total += score / 100.0
                count += 1

    if count == 0:
        return 0.4

    return total / count


def availability_score(candidate):

    rs = candidate.get("redrob_signals", {})

    score = 0.5

    if rs.get("open_to_work_flag", False):
        score += 0.2

    notice = rs.get("notice_period_days", 90)

    if notice <= 30:
        score += 0.2

    elif notice <= 60:
        score += 0.1

    if rs.get("willing_to_relocate", False):
        score += 0.1

    return min(score, 1.0)
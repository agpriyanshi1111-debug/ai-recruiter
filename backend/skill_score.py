def skill_match_score(job_keywords, candidate_skills):

    if not job_keywords:
        return 0.0

    job_set = set([k.lower().strip() for k in job_keywords if k])

    cand_set = set()

    for s in candidate_skills:

        if isinstance(s, str):
            cand_set.add(s.lower().strip())

        elif isinstance(s, dict):

            # try ALL possible field names (dataset-robust)
            for key in ["name", "skill", "skill_name", "title"]:
                if key in s and s[key]:
                    cand_set.add(str(s[key]).lower().strip())

            # sometimes nested skill dict
            if "skill" in s and isinstance(s["skill"], str):
                cand_set.add(s["skill"].lower().strip())

        else:
            cand_set.add(str(s).lower().strip())

    if not cand_set:
        return 0.0

    overlap = job_set.intersection(cand_set)

    return len(overlap) / max(len(job_set), 1)
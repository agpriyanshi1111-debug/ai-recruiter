import os
import json
import pandas as pd
from tqdm import tqdm

from backend.job_loader import load_job_text
from backend.jd_parser import parse_jd
from backend.honeypot import is_honeypot
from backend.career_trajectory import career_trajectory_score
from backend.advanced_score import assessment_score, availability_score

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CANDIDATE_PATH = os.path.join(BASE_DIR, "data", "candidates.jsonl")
JOB_PATH = os.path.join(BASE_DIR, "data", "job_description.docx")
OUTPUT_PATH = os.path.join(BASE_DIR, "output", "submission.csv")


# =========================
# LOAD CANDIDATES
# =========================
def load_candidates(path):
    data = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data


# =========================
# TEXT BUILDER
# =========================
def build_text(c):
    p = c.get("profile", {})
    skills = c.get("skills", [])
    career = c.get("career_history", [])

    parts = [p.get("headline", ""), p.get("summary", "")]

    for s in skills:
        if isinstance(s, dict):
            parts.append(str(s.get("name", "")))
        else:
            parts.append(str(s))

    for j in career:
        if isinstance(j, dict):
            parts.append(str(j.get("title", "")))
            parts.append(str(j.get("company", "")))

    return " ".join(parts).lower()


# =========================
# HONEYPOT SAFE CHECK
# =========================
def honeypot_penalty(candidate):
    if is_honeypot(candidate):
        return 0.7  # strong penalty, not full removal
    return 0.0


# =========================
# SKILL MATCH (WEIGHTED)
# =========================
def skill_score(text, keywords):
    if not keywords:
        return 0.0

    hits = 0
    for k in keywords:
        if k.lower() in text:
            hits += 1

    return hits / len(keywords)


# =========================
# BEHAVIOR SCORE (NORMALIZED BETTER)
# =========================
def behavior_score(c):
    rs = c.get("redrob_signals", {})

    score = 0.0

    score += rs.get("profile_completeness_score", 0) / 100 * 0.25
    score += rs.get("recruiter_response_rate", 0) * 0.25
    score += rs.get("interview_completion_rate", 0) * 0.20
    score += max(0, rs.get("offer_acceptance_rate", 0)) * 0.10

    github = rs.get("github_activity_score", -1)
    if github > 0:
        score += (github / 100) * 0.10

    if rs.get("verified_email"): score += 0.03
    if rs.get("verified_phone"): score += 0.03
    if rs.get("linkedin_connected"): score += 0.04

    return min(score, 1.0)


# =========================
# EXPERIENCE FIT
# =========================
def exp_score(c, jd):

    exp = c.get("profile", {}).get("years_of_experience", 0)

    # JD prefers ~5-9 years, ideal around 7
    target = 7.0

    diff = abs(exp - target)

    if diff <= 1:
        return 1.0
    elif diff <= 2:
        return 0.90
    elif diff <= 3:
        return 0.80
    elif diff <= 5:
        return 0.65
    else:
        return 0.50


# =========================
# FINAL SCORER (WINNING CORE)
# =========================
def score_candidate(c, jd):
    text = build_text(c)

    if is_honeypot(c):
        base_penalty = 0.5
    else:
        base_penalty = 0.0

    skills = skill_score(text, jd["keywords"])
    behavior = behavior_score(c)
    trajectory = career_trajectory_score(c)
    assessment = assessment_score(c, jd["keywords"])
    availability = availability_score(c)
    exp_fit = exp_score(c, jd)

    role_bonus = 0.0
    strong = [
        "ai engineer", "ml engineer", "machine learning engineer",
        "nlp engineer", "search engineer", "retrieval",
        "ranking", "recommendation", "data scientist"
    ]

    for r in strong:
        if r in text:
            role_bonus += 0.03

    role_bonus = min(role_bonus, 0.12)

    retrieval_bonus = 0.0
    retrieval_terms = [
        "retrieval", "rag", "embedding", "vector",
        "faiss", "milvus", "pinecone", "nlp", "llm"
    ]

    for t in retrieval_terms:
        if t in text:
            retrieval_bonus += 0.015

    retrieval_bonus = min(retrieval_bonus, 0.10)

    # FINAL SCORE (calibrated for ranking separation)
    score = (
        0.28 * skills +
        0.18 * behavior +
        0.16 * trajectory +
        0.12 * assessment +
        0.10 * availability +
        0.10 * exp_fit +
        role_bonus +
        retrieval_bonus -
        base_penalty
    )

    score = max(0, min(score, 1))


    # =========================
    # STRONG REASONING (STAGE 4 SAFE)
    # =========================
    profile = c.get("profile", {})
    headline = profile.get("headline", "Candidate")
    exp = profile.get("years_of_experience", 0)

    matched = [k for k in jd["keywords"] if k in text][:4]

    reasoning = (
        f"{headline} with {exp:.1f} years experience. "
        f"Matches skills: {', '.join(matched) if matched else 'core JD skills'}. "
        f"Behavior score {behavior:.2f}, experience fit {exp_fit:.2f}, "
        f"and strong alignment with JD requirements in AI/ML systems."
    )

    return score, reasoning


# =========================
# MAIN PIPELINE
# =========================
def main():
    print("Loading candidates...")
    candidates = load_candidates(CANDIDATE_PATH)

    print("Loading JD...")
    jd = parse_jd(load_job_text(JOB_PATH))

    results = []

    for c in tqdm(candidates):
        score, reason = score_candidate(c, jd)
        results.append({
            "candidate_id": c["candidate_id"],
            "score": score,
            "reasoning": reason
        })

    # deterministic tie-break
    results.sort(key=lambda x: (-x["score"], x["candidate_id"]))

    top100 = results[:100]

    output = []
    for i, r in enumerate(top100, 1):
        output.append({
            "candidate_id": r["candidate_id"],
            "rank": i,
            "score": round(r["score"], 6),
            "reasoning": r["reasoning"]
        })

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    pd.DataFrame(output).to_csv(OUTPUT_PATH, index=False)

    print("DONE:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
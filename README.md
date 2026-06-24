# AI Recruiter – Intelligent Candidate Discovery & Ranking

## Overview

AI Recruiter is an intelligent candidate ranking system developed for the Redrob Intelligent Candidate Discovery & Ranking Challenge.

The system analyzes a large pool of candidate profiles and automatically identifies the Top 100 candidates for a given job description using a multi-factor ranking engine.

The solution combines:

* Skill Matching
* Behavioral Signal Analysis
* Career Trajectory Evaluation
* Assessment Performance
* Availability Scoring
* Semantic Similarity Matching
* Honeypot Detection
* Explainable Candidate Reasoning

A Streamlit dashboard is included for interactive exploration of ranking results.

---

# Problem Statement

Recruiters often receive thousands of applications for a single role.

Manually identifying the most relevant candidates is:

* Time-consuming
* Expensive
* Inconsistent

This project automates candidate discovery by ranking applicants according to their relevance to the job description while incorporating behavioral intelligence and profile quality signals.

---

# Dataset

The ranking system processes:

* Candidate profiles
* Skills and expertise
* Career history
* Behavioral signals
* Recruiter interaction metrics
* Assessment outcomes

Each candidate is evaluated against the provided job description.

---

# Solution Architecture

## Stage 1 — Data Loading

Candidate profiles are loaded from:

```text
data/candidates.jsonl
```

Job description is loaded from:

```text
data/job_description.docx
```

---

## Stage 2 — Candidate Representation

For every candidate the system extracts:

* Professional headline
* Profile summary
* Skills
* Career history

These fields are combined into a unified candidate representation.

---

## Stage 3 — Multi-Factor Candidate Scoring

The ranking score combines several independent signals.

### Skill Matching

Measures overlap between candidate skills and job requirements.

### Behavioral Analysis

Evaluates:

* Recruiter response rate
* Interview completion rate
* Offer acceptance rate
* Profile completeness
* Verification signals

### Career Trajectory

Measures consistency and progression throughout a candidate’s career.

### Assessment Performance

Rewards strong technical assessment outcomes.

### Availability Scoring

Prioritizes candidates available sooner.

### Semantic Matching

Uses SentenceTransformer embeddings and cosine similarity to measure relevance between:

* Candidate profile
* Job description

### Role Relevance Bonus

Additional weighting for:

* AI Engineer
* ML Engineer
* NLP Engineer
* Data Scientist
* Search Engineer

---

## Stage 4 — Honeypot Detection

The system identifies suspicious profiles using:

* Behavioral inconsistencies
* Signal anomalies
* Profile irregularities

Detected honeypot candidates are penalized before final ranking.

---

# Ranking Formula

The final ranking score combines multiple weighted components:

```python
score = (
    0.18 * skills +
    0.22 * semantic +
    0.15 * behavior +
    0.12 * trajectory +
    0.10 * assessment +
    0.08 * availability +
    0.08 * exp_fit +
    role_bonus +
    retrieval_bonus -
    base_penalty
)
```

Scores are normalized between:

```text
0.0 → 1.0
```

---

# Explainability

Each recommended candidate includes automatically generated reasoning.

Example:

"Senior NLP Engineer with 8.9 years of experience. Background includes Python, Vector Search and Embedding Systems. Candidate demonstrates strong recruiter engagement, experience alignment and technical relevance to the role."

---

# Streamlit Dashboard

The project includes an interactive dashboard featuring:

## Dashboard

* Ranking Overview
* KPI Cards
* Score Distribution
* Candidate Leaderboard

## Candidate Explorer

* Candidate Lookup
* Detailed Ranking Explanation
* Ranking Insights

## Analytics

* Ranking Trends
* Score Distribution Analysis
* Top Performer Analysis

## Export

* Submission Download
* Summary Statistics

---

# Project Structure

```text
ai-recruiter/

├── backend/
│   ├── app.py
│   ├── embedder.py
│   ├── ranker.py
│   ├── honeypot.py
│   ├── advanced_score.py
│   ├── career_trajectory.py
│   ├── jd_parser.py
│   ├── job_loader.py
│   ├── validate_submission.py
│   ├── inspect_data.py
│   ├── signal_score.py
│   ├── skill_score.py
│   └── text_builder.py
│
├── data/
│   ├── candidates.jsonl
│   └── job_description.docx
│
├── output/
│   └── submission.csv
│
├── streamlit_app.py
├── requirements.txt
└── README.md
```

---

# Installation

```bash
pip install -r requirements.txt
```

---

# Generate Rankings

```bash
python -m backend.app
```

Output:

```text
output/submission.csv
```

---

# Launch Dashboard

```bash
python -m streamlit run streamlit_app.py
```

---

# Technologies Used

* Python
* Pandas
* Streamlit
* Plotly
* Sentence Transformers
* Hugging Face
* Scikit-Learn
* FAISS
* Information Retrieval Techniques

---

# Future Improvements

* Cross-Encoder Re-ranking
* Learning-to-Rank Models
* Dynamic Weight Optimization
* Recruiter Feedback Loops
* Enhanced Explainability

---Author

Built for the Redrob Intelligent Candidate Discovery & Ranking Challenge.

Designed to provide scalable, explainable, and high-quality candidate recommendations.

import re

def parse_jd(text):

    text = text.lower()

    # strong keyword anchors from JD
    skill_keywords = [
        "python", "sql", "spark", "airflow",
        "vector", "embedding", "retrieval",
        "faiss", "milvus", "pinecone",
        "machine learning", "nlp", "llm",
        "ranking", "ndcg", "map", "ab testing"
    ]

    found = []

    for k in skill_keywords:
        if k in text:
            found.append(k)

    # experience extraction (basic but stable)
    exp_match = re.findall(r"(\d+)[\+\- ]*years?", text)
    exp_vals = [int(x) for x in exp_match] if exp_match else [5, 9]

    return {
        "keywords": found,
        "years_min": min(exp_vals),
        "years_max": max(exp_vals)
    }
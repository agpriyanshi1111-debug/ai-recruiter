import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def semantic_score(job_vec, cand_vec):
    return float(cosine_similarity([job_vec], [cand_vec])[0][0])
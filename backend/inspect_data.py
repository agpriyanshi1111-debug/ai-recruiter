import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# try multiple possible locations
POSSIBLE_PATHS = [
    os.path.join(BASE_DIR, "candidates.jsonl"),
    os.path.join(BASE_DIR, "data", "candidates.jsonl"),
    os.path.join(BASE_DIR, "backend", "candidates.jsonl"),
]

CANDIDATE_PATH = None

for path in POSSIBLE_PATHS:
    if os.path.exists(path):
        CANDIDATE_PATH = path
        break

if CANDIDATE_PATH is None:
    raise FileNotFoundError("candidates.jsonl not found in expected locations")

print("Using file:", CANDIDATE_PATH)


def read_jsonl(path):
    data = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line))
    return data


candidates = read_jsonl(CANDIDATE_PATH)

print("Total candidates:", len(candidates))
print("\nKeys:", candidates[0].keys())
print("\nProfile sample:", candidates[0].get("profile", {}))
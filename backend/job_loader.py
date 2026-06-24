from docx import Document

def load_job_text(path: str) -> str:
    if path.endswith(".docx"):
        doc = Document(path)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

    # fallback for .md if used later
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
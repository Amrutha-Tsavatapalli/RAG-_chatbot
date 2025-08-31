# modules/resume_parser.py
import fitz  # PyMuPDF
import docx
import os

def extract_text(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        doc = fitz.open(file_path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text
    elif ext == ".docx":
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return ""

def parse_resume(file_path):
    text = extract_text(file_path).lower()
    stream = "cs" if "python" in text or "java" in text else "general"
    skills = [word for word in ["python", "java", "sql", "ml", "communication"] if word in text]
    return {"stream": stream, "skills": skills}

import os
import fitz
from docx import Document

def read_txt(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def read_pdf(path):
    doc = fitz.open(path)
    text = []
    for page in doc:
        text.append(page.get_text())
    return "\n".join(text)

def read_docx(path):
    doc = Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

def read_file(path):
    ext = os.path.splitext(path)[1].lower()

    if ext == ".txt":
        return read_txt(path)
    elif ext == ".pdf":
        return read_pdf(path)
    elif ext == ".docx":
        return read_docx(path)
    else:
        raise ValueError(f"Unsupported format: {ext}")
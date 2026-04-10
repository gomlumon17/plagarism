import re

def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()

def sent_split(text):
    return re.split(r'(?<=[.!?])\s+', text)

def chunk_text(text, chunk_size=2, overlap=1):
    sentences = sent_split(text)
    chunks = []

    step = max(1, chunk_size - overlap)

    for i in range(0, len(sentences), step):
        chunk = " ".join(sentences[i:i + chunk_size]).strip()
        if len(chunk.split()) >= 8:
            chunks.append(chunk)

    return chunks
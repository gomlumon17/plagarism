from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
import tempfile
import shutil
import os

from src.detector import detect_plagiarism

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>Plagiarism Detector</h1>
    <form action="/compare" method="post" enctype="multipart/form-data">
        <input type="file" name="file1" required><br><br>
        <input type="file" name="file2" required><br><br>
        <input type="number" name="threshold" value="0.78" step="0.01"><br><br>
        <button type="submit">Compare</button>
    </form>
    """

@app.post("/compare")
async def compare(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    threshold: float = Form(0.78)
):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as f1:
            shutil.copyfileobj(file1.file, f1)
            path1 = f1.name

        with tempfile.NamedTemporaryFile(delete=False) as f2:
            shutil.copyfileobj(file2.file, f2)
            path2 = f2.name

        report, percent = detect_plagiarism(path1, path2, threshold)

        return JSONResponse({
            "plagiarism_percentage": percent,
            "rows": len(report)
        })

    except Exception as e:
        return {"error": str(e)}
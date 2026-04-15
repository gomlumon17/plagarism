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
    <html>
    <body>
        <h1>Online Assignment Submission and Plagiarism Detection Portal</h1>
        <form action="/compare" method="post" enctype="multipart/form-data">
            <label>File 1:</label><br>
            <input type="file" name="file1" required><br><br>

            <label>File 2:</label><br>
            <input type="file" name="file2" required><br><br>

            <label>Threshold:</label><br>
            <input type="number" name="threshold" value="0.78" step="0.01" min="0.30" max="0.95"><br><br>

            <button type="submit">Compare</button>
        </form>
    </body>
    </html>
    """

@app.post("/compare")
async def compare(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    threshold: float = Form(0.78)
):
    path1 = None
    path2 = None
    try:
        suffix1 = os.path.splitext(file1.filename)[1]
        suffix2 = os.path.splitext(file2.filename)[1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix1) as f1:
            shutil.copyfileobj(file1.file, f1)
            path1 = f1.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix2) as f2:
            shutil.copyfileobj(file2.file, f2)
            path2 = f2.name

        report, percent = detect_plagiarism(path1, path2, threshold=threshold)

        return JSONResponse({
            "plagiarism_percentage": percent,
            "total_rows": len(report),
            "top_matches": report.head(5).to_dict(orient="records")
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

    finally:
        if path1 and os.path.exists(path1):
            os.remove(path1)
        if path2 and os.path.exists(path2):
            os.remove(path2)
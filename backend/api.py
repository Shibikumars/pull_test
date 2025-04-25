from fastapi import FastAPI
from fastapi.responses import FileResponse
import subprocess

app = FastAPI()

@app.get("/")
def home():
    return {"message": "PRism API running"}

@app.get("/review")
def run_code_review():
    subprocess.run(["python", "code_review.py"])
    return FileResponse("report.html", media_type="text/html")

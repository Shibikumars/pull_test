from fastapi import FastAPI, UploadFile, Form
from pydantic import BaseModel
import openai

app = FastAPI()

class LLMRequest(BaseModel):
    use_case: str  # "code" or "doc"

@app.get("/")
def home():
    return {"message": "PRism API running"}

@app.post("/recommend")
def recommend_model(data: LLMRequest):
    if data.use_case == "code":
        return {"model": "Mistral or OpenAI Codex"}
    if data.use_case == "doc":
        return {"model": "GPT-4 or Claude"}
    return {"model": "Unknown"}

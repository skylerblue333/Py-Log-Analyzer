from fastapi import FastAPI
from pydantic import BaseModel
from src.analyzer import parse_log, analyze

app = FastAPI(title="Log Analyzer API")

class LogRequest(BaseModel):
    log_text: str

@app.post("/analyze")
def analyze_logs(req: LogRequest):
    entries = parse_log(req.log_text)
    return analyze(entries)

@app.get("/health")
def health():
    return {"status": "ok"}

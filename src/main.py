"""
Py-Log-Analyzer: Analyzes log streams for error patterns
"""
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Py-Log-Analyzer", version="3.0.0")

from typing import List
class LogEntry(BaseModel):
    level: str
    message: str

@app.post("/api/v1/analyze")
def analyze_logs(logs: List[LogEntry]):
    errors = [l for l in logs if l.level.upper() in ["ERROR", "FATAL"]]
    return {"total": len(logs), "error_count": len(errors), "error_rate": len(errors)/len(logs) if logs else 0}


@app.get("/health")
def health():
    return {"status": "healthy", "service": "Py-Log-Analyzer", "timestamp": int(time.time())}

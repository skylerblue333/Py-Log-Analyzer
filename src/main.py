from collections import Counter
from enum import StrEnum

from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="Sky Log Triage", version="0.1.0")

MAX_BATCH = 1000
MAX_MESSAGE_CHARS = 4096


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogEntry(BaseModel):
    level: LogLevel
    message: str = Field(min_length=1, max_length=MAX_MESSAGE_CHARS)
    source: str | None = Field(default=None, max_length=128)

    @field_validator("message")
    @classmethod
    def message_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("message cannot be blank")
        return value

    @field_validator("source")
    @classmethod
    def normalize_source(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("source cannot be blank when supplied")
        return value


class AnalyzeRequest(BaseModel):
    logs: list[LogEntry] = Field(min_length=1, max_length=MAX_BATCH)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok", "service": "sky-log-triage"}


@app.get("/readyz")
def readyz() -> dict[str, object]:
    return {"status": "ready", "max_batch": MAX_BATCH}


@app.post("/v1/analyze")
def analyze_logs(request: AnalyzeRequest) -> dict[str, object]:
    level_counts = Counter(entry.level.value for entry in request.logs)
    source_counts = Counter(entry.source for entry in request.logs if entry.source)
    severe = level_counts[LogLevel.ERROR.value] + level_counts[LogLevel.CRITICAL.value]
    total = len(request.logs)
    return {
        "total": total,
        "severe_count": severe,
        "severe_rate": severe / total,
        "levels": dict(sorted(level_counts.items())),
        "sources": dict(sorted(source_counts.items())),
    }

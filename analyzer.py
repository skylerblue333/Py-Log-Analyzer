"""Structured log analysis foundation using the mature Polars dataframe engine."""
import re
import polars as pl

LEVEL = re.compile(r"\b(DEBUG|INFO|WARNING|ERROR|CRITICAL)\b")

def analyze(lines: list[str]) -> pl.DataFrame:
    rows = [{"line": line, "level": (LEVEL.search(line).group(1) if LEVEL.search(line) else "UNKNOWN")} for line in lines]
    return pl.DataFrame(rows).group_by("level").len().sort("len", descending=True)

if __name__ == "__main__":
    print(analyze(["INFO started", "ERROR failed", "INFO done"]))

import re
from collections import Counter
from dataclasses import dataclass
from typing import List, Dict

LOG_PATTERN = re.compile(
    r'(?P<ip>[\d.]+) - - \[(?P<time>[^\]]+)\] '
    r'"(?P<method>\w+) (?P<path>[^ ]+) HTTP/[\d.]+" '
    r'(?P<status>\d+) (?P<size>\d+)'
)

@dataclass
class LogEntry:
    ip: str
    time: str
    method: str
    path: str
    status: int
    size: int

def parse_log(log_text: str) -> List[LogEntry]:
    entries = []
    for line in log_text.splitlines():
        m = LOG_PATTERN.match(line)
        if m:
            entries.append(LogEntry(
                ip=m.group("ip"),
                time=m.group("time"),
                method=m.group("method"),
                path=m.group("path"),
                status=int(m.group("status")),
                size=int(m.group("size")),
            ))
    return entries

def analyze(entries: List[LogEntry]) -> Dict:
    if not entries:
        return {}
    status_counts = Counter(e.status for e in entries)
    top_ips = Counter(e.ip for e in entries).most_common(5)
    top_paths = Counter(e.path for e in entries).most_common(5)
    error_rate = sum(1 for e in entries if e.status >= 400) / len(entries)
    return {
        "total_requests": len(entries),
        "error_rate": round(error_rate, 4),
        "status_codes": dict(status_counts),
        "top_ips": top_ips,
        "top_paths": top_paths,
    }

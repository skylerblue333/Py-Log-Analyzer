from src.analyzer import parse_log, analyze

SAMPLE_LOG = '''127.0.0.1 - - [10/Oct/2023:13:55:36 -0700] "GET /index.html HTTP/1.1" 200 2326
127.0.0.1 - - [10/Oct/2023:13:55:37 -0700] "POST /api/data HTTP/1.1" 201 512
10.0.0.1 - - [10/Oct/2023:13:55:38 -0700] "GET /missing HTTP/1.1" 404 0
10.0.0.1 - - [10/Oct/2023:13:55:39 -0700] "GET /error HTTP/1.1" 500 0'''

def test_parse_log():
    entries = parse_log(SAMPLE_LOG)
    assert len(entries) == 4

def test_analyze_error_rate():
    entries = parse_log(SAMPLE_LOG)
    result = analyze(entries)
    assert result["error_rate"] == 0.5

def test_analyze_total():
    entries = parse_log(SAMPLE_LOG)
    result = analyze(entries)
    assert result["total_requests"] == 4

def test_empty_log():
    result = analyze([])
    assert result == {}

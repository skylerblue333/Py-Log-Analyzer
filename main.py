import re
import collections
import logging

logging.basicConfig(level=logging.INFO)

def analyze_logs(log_lines):
    # Simplified Apache/Nginx log regex
    log_pattern = re.compile(r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<time>.*?)\] "(?P<method>\w+) (?P<path>.*?) HTTP/.*?" (?P<status>\d+) (?P<size>\d+)')
    
    ip_counter = collections.Counter()
    status_counter = collections.Counter()
    
    for line in log_lines:
        match = log_pattern.search(line)
        if match:
            data = match.groupdict()
            ip_counter[data['ip']] += 1
            status_counter[data['status']] += 1
            
    return ip_counter, status_counter

if __name__ == "__main__":
    sample_logs = [
        '192.168.1.1 - - [10/Oct/2023:13:55:36 -0700] "GET /index.html HTTP/1.1" 200 2326',
        '10.0.0.2 - - [10/Oct/2023:13:55:37 -0700] "GET /api/data HTTP/1.1" 404 512',
        '192.168.1.1 - - [10/Oct/2023:13:55:38 -0700] "POST /login HTTP/1.1" 200 1024'
    ]
    
    ips, statuses = analyze_logs(sample_logs)
    logging.info(f"Top IPs: {ips.most_common(3)}")
    logging.info(f"Status Codes: {dict(statuses)}")
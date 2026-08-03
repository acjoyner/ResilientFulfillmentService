"""
Fulfillment Service Diagnostics & Monitoring Tools
Custom tool definitions for Google Antigravity SDK Fulfillment Subagent
"""

import os
import requests
import json

APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:8080")
LOG_PATH = os.getenv("LOG_PATH", "/var/log/fulfillment-service/resilient-fulfillment.log")

def check_fulfillment_health() -> str:
    """
    Check the HTTP health status of the Resilient Fulfillment Microservice.
    Returns HTTP status code and JSON health details.
    """
    url = f"{APP_BASE_URL}/actuator/health"
    try:
        response = requests.get(url, timeout=5)
        return json.dumps({
            "status_code": response.status_code,
            "health": response.json() if response.status_code == 200 else response.text
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Failed to reach fulfillment service: {str(e)}"})

def inspect_recent_app_logs(lines: int = 50, filter_level: str = "ERROR") -> str:
    """
    Read recent lines from the application log file and filter by log level (ERROR, WARN, INFO).
    """
    possible_paths = [
        LOG_PATH,
        "target/logs/resilient-fulfillment.log",
        "../target/logs/resilient-fulfillment.log"
    ]
    
    target_file = None
    for p in possible_paths:
        if os.path.exists(p):
            target_file = p
            break
            
    if not target_file:
        return json.dumps({"status": "LOG_FILE_NOT_FOUND", "checked_paths": possible_paths})
        
    try:
        matching_lines = []
        with open(target_file, "r") as f:
            all_lines = f.readlines()
            for line in reversed(all_lines):
                if filter_level.upper() in line:
                    matching_lines.append(line.strip())
                if len(matching_lines) >= lines:
                    break
                    
        return json.dumps({
            "file": target_file,
            "filter": filter_level,
            "count": len(matching_lines),
            "logs": matching_lines
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error reading log file: {str(e)}"})

def get_prometheus_metrics() -> str:
    """
    Fetch Prometheus Micrometer metrics from the Spring Boot Actuator endpoint.
    """
    url = f"{APP_BASE_URL}/actuator/prometheus"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            lines = [l for l in response.text.split("\n") if "hikaricp" in l or "resilience4j" in l or "jvm_gc" in l]
            return "\n".join(lines[:30])
        return f"HTTP {response.status_code}"
    except Exception as e:
        return f"Error fetching metrics: {str(e)}"

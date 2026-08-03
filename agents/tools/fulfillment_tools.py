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


NEXABANK_SERVICES = {
    "api-gateway": "http://localhost:8080/actuator/health",
    "account-service": "http://localhost:8081/actuator/health",
    "transaction-service": "http://localhost:8082/actuator/health",
    "notification-service": "http://localhost:8083/actuator/health",
    "loan-service": "http://localhost:8084/actuator/health"
}

def check_nexabank_microservices_health() -> str:
    """
    Performs multi-service health checks across all NexaBank Platform microservice ports
    (Gateway 8080, Account 8081, Transaction 8082, Notification 8083, Loan 8084).
    """
    results = {}
    for svc_name, url in NEXABANK_SERVICES.items():
        try:
            resp = requests.get(url, timeout=3)
            results[svc_name] = {
                "url": url,
                "status_code": resp.status_code,
                "health": resp.json() if resp.status_code == 200 else resp.text[:100]
            }
        except Exception as e:
            results[svc_name] = {
                "url": url,
                "status": "UNREACHABLE",
                "error": str(e)
            }
    return json.dumps(results, indent=2)

"""
Database & Redis Diagnostics Tools
Custom tool definitions for Google Antigravity SDK Database Subagent
"""

import os
import requests
import json

APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:8080")

def check_database_pool_metrics() -> str:
    """
    Fetch HikariCP connection pool metrics (active, idle, pending connections) from Spring Actuator.
    """
    url = f"{APP_BASE_URL}/actuator/prometheus"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            lines = [l for l in response.text.split("\n") if "hikaricp_connections" in l and not l.startswith("#")]
            return "\n".join(lines) if lines else "No HikariCP metrics actively reported."
        return f"HTTP {response.status_code}"
    except Exception as e:
        return json.dumps({"error": f"Failed to query connection pool metrics: {str(e)}"})

def check_redis_cache_status() -> str:
    """
    Verify Redis caching layer status and check cache hits/misses.
    """
    url = f"{APP_BASE_URL}/actuator/health/redis"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code in [200, 503]:
            return json.dumps(response.json(), indent=2)
        return f"HTTP {response.status_code}: {response.text}"
    except Exception as e:
        return json.dumps({"error": f"Failed to connect to Redis health endpoint: {str(e)}"})

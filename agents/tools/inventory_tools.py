"""
Inventory Service & Resilience Diagnostics Tools
Custom tool definitions for Google Antigravity SDK Inventory Subagent
"""

import os
import requests
import json

APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:8080")

def check_circuit_breaker_status() -> str:
    """
    Query Actuator health details specifically for Resilience4j Circuit Breakers and Bulkheads.
    """
    url = f"{APP_BASE_URL}/actuator/health"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            details = data.get("components", {})
            circuit_breakers = details.get("circuitBreakers", {})
            bulkheads = details.get("bulkheads", {})
            return json.dumps({
                "status": data.get("status"),
                "circuit_breakers": circuit_breakers,
                "bulkheads": bulkheads
            }, indent=2)
        return json.dumps({"error": f"HTTP {response.status_code}", "body": response.text})
    except Exception as e:
        return json.dumps({"error": f"Failed to check circuit breaker status: {str(e)}"})

def simulate_circuit_breaker_trip(product_id: str = "PROD-FAIL-999") -> str:
    """
    Triggers a failed order request designed to invoke the Resilience4j Circuit Breaker fallback.
    """
    url = f"{APP_BASE_URL}/api/v1/orders"
    payload = {
        "productId": product_id,
        "quantity": 1,
        "price": 99.99,
        "customerEmail": "circuit-breaker-test@bankofamerica.com"
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
        return json.dumps({
            "http_status": response.status_code,
            "response": response.json()
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Simulation failed: {str(e)}"})

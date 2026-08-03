"""
Fulfillment App Support Subagent
Powered by Google Antigravity SDK
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.fulfillment_tools import check_fulfillment_health, inspect_recent_app_logs, get_prometheus_metrics, check_nexabank_microservices_health

FULFILLMENT_AGENT_PERSONA = """
You are the Fulfillment Microservice Application Support Agent.
Your primary role is to monitor the core Java/Spring Boot application host (http://localhost:8080),
inspect application logs for exceptions (NullPointerException, SQLTimeoutException), check MDC trace IDs,
and provide real-time status updates on application health and JVM performance metrics.
"""

def get_fulfillment_agent_config():
    """
    Returns persona instructions and tools for the Fulfillment Support Subagent.
    """
    return {
        "name": "FulfillmentAppSupportAgent",
        "description": "Monitors Spring Boot app health, logs, MDC trace IDs, and JVM execution.",
        "persona": FULFILLMENT_AGENT_PERSONA,
        "tools": [check_fulfillment_health, check_nexabank_microservices_health, inspect_recent_app_logs, get_prometheus_metrics]
    }

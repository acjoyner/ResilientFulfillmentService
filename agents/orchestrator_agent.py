"""
Enterprise AI Support Orchestrator
NexaBank Global Financial Java Application Support & Observability Platform
Powered by Google Antigravity (AGY) SDK
"""

import asyncio
import os
import sys
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from google.antigravity import Agent, LocalAgentConfig, types
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False

from fulfillment_agent import get_fulfillment_agent_config, check_fulfillment_health, inspect_recent_app_logs, get_prometheus_metrics
from inventory_agent import get_inventory_agent_config, check_circuit_breaker_status, simulate_circuit_breaker_trip
from database_agent import get_database_agent_config, check_database_pool_metrics, check_redis_cache_status

ORCHESTRATOR_SYSTEM_INSTRUCTIONS = """
You are the Senior Enterprise Application Support Orchestrator for NexaBank Global Financial.
You manage a network of specialized L2/L3 support agents:
1. FulfillmentAppSupportAgent (Java / Spring Boot app health & log analysis)
2. InventoryResilienceSupportAgent (Resilience4j Circuit Breakers & Bulkhead concurrency)
3. DatabaseRedisDiagnosticAgent (HikariCP DB pool metrics & Redis cache health)

Your Goal:
During P1/P2 production incidents or routine health checks:
1. Run diagnostic checks across all subagent tools.
2. Synthesize findings into a clear STAR-format Incident Triage Report.
3. Recommend immediate mitigation steps and long-term Root Cause Analysis (RCA) fixes.
"""

async def run_orchestrated_triage():
    """
    Executes an incident triage run across all microservice diagnostic tools.
    """
    print("========================================================================")
    print(" 🚀 NEXABANK ENTERPRISE AI SUPPORT ORCHESTRATOR (Google ADK) ")
    print("========================================================================")
    print(f"Google Antigravity SDK Available: {SDK_AVAILABLE}")
    print("------------------------------------------------------------------------")
    
    # Run diagnostic tools directly across microservices
    print("[1/3] Querying Fulfillment App Support Agent...")
    app_health = check_fulfillment_health()
    print(f"App Health Result: {app_health[:200]}...")
    
    print("\n[2/3] Querying Inventory & Resilience Support Agent...")
    circuit_status = check_circuit_breaker_status()
    print(f"Circuit Breaker Status: {circuit_status[:200]}...")
    
    print("\n[3/3] Querying Database & Redis Diagnostic Agent...")
    db_metrics = check_database_pool_metrics()
    redis_status = check_redis_cache_status()
    print(f"DB Metrics: {db_metrics[:150]}...")
    print(f"Redis Health: {redis_status[:150]}...")

    print("------------------------------------------------------------------------")
    print(" 📊 SYNTHESIZED STAR INCIDENT TRIAGE REPORT")
    print("------------------------------------------------------------------------")
    report = {
        "Incident_Status": "SYSTEM_HEALTHY" if "UP" in app_health else "DEGRADED",
        "Target_Environment": "NexaBank Global Financial - ResilientFulfillmentService",
        "Subagents_Engaged": [
            "FulfillmentAppSupportAgent",
            "InventoryResilienceSupportAgent",
            "DatabaseRedisDiagnosticAgent"
        ],
        "Diagnostic_Summary": {
            "Application_Status": json.loads(app_health) if app_health.startswith("{") else app_health,
            "Resilience_Circuit_Breaker": json.loads(circuit_status) if circuit_status.startswith("{") else circuit_status,
            "Redis_Cache": json.loads(redis_status) if redis_status.startswith("{") else redis_status
        }
    }
    
    print(json.dumps(report, indent=2))
    print("========================================================================")
    return report

if __name__ == "__main__":
    asyncio.run(run_orchestrated_triage())

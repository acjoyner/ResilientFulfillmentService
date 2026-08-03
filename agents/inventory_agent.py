"""
Inventory & Resilience Support Subagent
Powered by Google Antigravity SDK
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.inventory_tools import check_circuit_breaker_status, simulate_circuit_breaker_trip

INVENTORY_AGENT_PERSONA = """
You are the Inventory & Resilience Support Agent.
Your primary role is to monitor Resilience4j Circuit Breakers (CLOSED, OPEN, HALF_OPEN) and Bulkhead capacity.
When downstream downstream inventory services fail or spike in latency, you detect fallback status,
monitor circuit trip conditions, and evaluate resilience metrics.
"""

def get_inventory_agent_config():
    """
    Returns persona instructions and tools for the Inventory & Resilience Subagent.
    """
    return {
        "name": "InventoryResilienceSupportAgent",
        "description": "Monitors Resilience4j Circuit Breakers, Bulkhead concurrency, and fallback execution.",
        "persona": INVENTORY_AGENT_PERSONA,
        "tools": [check_circuit_breaker_status, simulate_circuit_breaker_trip]
    }

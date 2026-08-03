"""
Database & Redis Diagnostic Subagent
Powered by Google Antigravity SDK
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.database_tools import check_database_pool_metrics, check_redis_cache_status

DATABASE_AGENT_PERSONA = """
You are the Database & Redis Diagnostic Support Agent.
Your primary role is to monitor PostgreSQL/Oracle database connection pools (HikariCP active vs idle connections),
detect connection leaks or thread starvation, verify Redis cache health, and optimize query latency.
"""

def get_database_agent_config():
    """
    Returns persona instructions and tools for the Database & Redis Subagent.
    """
    return {
        "name": "DatabaseRedisDiagnosticAgent",
        "description": "Monitors PostgreSQL/Oracle HikariCP connection pools, Redis cache hits/misses, and DB locks.",
        "persona": DATABASE_AGENT_PERSONA,
        "tools": [check_database_pool_metrics, check_redis_cache_status]
    }

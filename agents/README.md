# 🤖 Enterprise Multi-Agent AI Support Network (Google Antigravity SDK)

This module extends **ResilientFulfillmentService** with an autonomous multi-agent AI support network built using the **Google Antigravity (AGY) SDK** (`google-antigravity`).

---

## 🏛️ Multi-Agent Architecture

```
                  ┌────────────────────────────────────────┐
                  │   Enterprise Support Orchestrator      │
                  │   (Google Antigravity SDK Master)      │
                  └──────────────────┬─────────────────────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         │                           │                           │
┌────────▼─────────┐       ┌─────────▼────────┐        ┌─────────▼────────┐
│ Fulfillment App  │       │ Inventory        │        │ Database & Redis │
│ Support Agent    │       │ Resilience Agent │        │ Diagnostic Agent │
└──────────────────┘       └──────────────────┘        └──────────────────┘
  (Monitors App,           (Monitors Bulkheads        (Monitors Oracle/   
   HTTP Endpoints,          & Circuit Breakers)        Postgres Locks &   
   Actuator & Logs)                                    Hikari Connection Pool)
```

---

## 👥 Subagent Responsibilities

### 1. ⚙️ Fulfillment App Support Agent (`fulfillment_agent.py`)
* **Scope**: Spring Boot microservice runtime (`http://localhost:8080`).
* **Tools**:
  * `check_fulfillment_health()`: Pings `/actuator/health` and `/api/v1/orders/health`.
  * `inspect_recent_app_logs()`: Parses `/var/log/fulfillment-service/resilient-fulfillment.log` for MDC trace IDs (`traceId`) and exceptions (`NullPointerException`, `SQLTimeoutException`).
  * `get_prometheus_metrics()`: Fetches JVM memory, GC overhead, and thread metrics.

### 2. 🛡️ Inventory Resilience Agent (`inventory_agent.py`)
* **Scope**: Resilience4j fault tolerance and fallback execution.
* **Tools**:
  * `check_circuit_breaker_status()`: Inspects Circuit Breaker states (`CLOSED`, `OPEN`, `HALF_OPEN`) and Bulkhead thread pools.
  * `simulate_circuit_breaker_trip()`: Triggers synthetic fallback execution.

### 3. 🗄️ Database & Redis Diagnostic Agent (`database_agent.py`)
* **Scope**: Relational persistence and high-speed caching.
* **Tools**:
  * `check_database_pool_metrics()`: Inspects HikariCP active, idle, and pending connections.
  * `check_redis_cache_status()`: Verifies Redis connection health and cache hit/miss baselines.

---

## 🚀 Running the Orchestrated Multi-Agent System

```bash
# 1. Install dependencies
cd agents
pip install -r requirements.txt

# 2. Execute Orchestrated Triage
python3 orchestrator_agent.py
```

# 🏛️ Enterprise System Architecture & L2/L3 Operational Processes
## ResilientFulfillmentService — NexaBank Global Financial Platform Model

This comprehensive document breaks down all system architectures, request processing lifecycles, incident triage workflows, observability pipelines, and autonomous multi-agent AI operations within the **ResilientFulfillmentService** platform.

---

## 📐 1. Full Multi-Tier System Architecture Diagram

```mermaid
flowchart TD
    subgraph Client_Layer ["Client & Ingress Layer"]
        User["Client / Web Browser\n(http://localhost:8080)"]
        F5["F5 Load Balancer /\nOpenShift Edge Router"]
    end

    subgraph App_Layer ["Application & Runtime Layer (RHEL / Docker)"]
        SpringBoot["Java 17 / Spring Boot 3 Microservice\n(resilient-fulfillment-service)"]
        Logback["Logback JSON Logger\nMDC (traceId, spanId)"]
        Actuator["Spring Actuator &\nMicrometer Prometheus"]
        
        subgraph Fault_Tolerance ["Resilience4j Governance"]
            CB["Circuit Breaker\n(CLOSED / OPEN / HALF_OPEN)"]
            BH["Bulkhead Concurrency Guard"]
        end
    end

    subgraph Data_Layer ["Persistence & Caching Layer"]
        Postgres[(PostgreSQL 15 DB\nfulfillment_orders)]
        Redis[(Redis 7 NoSQL Cache\nProductCache - TTL 600s)]
    end

    subgraph Observability_Layer ["Observability & Log Aggregation"]
        Splunk["Splunk Enterprise\n(http://localhost:8000)"]
        Dynatrace["Dynatrace APM &\nProcess Monitoring"]
    end

    subgraph Agentic_Layer ["Autonomous AI Operations (Google ADK)"]
        Orchestrator["Master Support Orchestrator\n(google.antigravity)"]
        SubApp["Fulfillment App Agent"]
        SubInv["Inventory Resilience Agent"]
        SubDB["Database & Redis Agent"]
    end

    User --> F5
    F5 --> SpringBoot
    SpringBoot --> CB
    SpringBoot --> BH
    CB --> Postgres
    SpringBoot --> Redis
    SpringBoot --> Logback
    SpringBoot --> Actuator
    Logback --> Splunk
    Actuator --> Dynatrace

    Orchestrator --> SubApp
    Orchestrator --> SubInv
    Orchestrator --> SubDB
    SubApp --> SpringBoot
    SubInv --> CB
    SubDB --> Postgres
    SubDB --> Redis
```

---

## ⚡ 2. Request Processing & Resilience Lifecycle

### Sequence Diagram: Order Processing, Caching & Fallback Execution

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant Controller as OrderController
    participant Service as FulfillmentService
    participant Redis as Redis ProductCache
    participant Circuit as Resilience4j CircuitBreaker
    participant DB as PostgreSQL DB
    participant Splunk as Splunk MDC Logger

    Client->>Controller: POST /api/v1/orders (productId, qty, price)
    Controller->>Splunk: Inject MDC traceId=abc-123 & Log INFO
    Controller->>Service: processFulfillment(request)
    
    Service->>Redis: Check ProductCache for productId
    alt Cache Hit
        Redis-->>Service: Return cached Product info
    else Cache Miss / Redis Down
        Service->>DB: Query Product table
        DB-->>Service: Return Product details
        Service->>Redis: Populate ProductCache (TTL 600s)
    end

    Service->>Circuit: Execute Inventory Check via CircuitBreaker

    alt Circuit CLOSED (Healthy)
        Circuit-->>Service: Reserve Inventory Success
        Service->>DB: INSERT into fulfillment_orders (STATUS='FULFILLED')
        DB-->>Service: Order Saved
        Service-->>Client: HTTP 200 Order Processed Successfully
    else Downstream Timeout / Circuit OPEN
        Circuit-->>Service: Trip Fallback Handler
        Service->>Splunk: Log WARN status="FALLBACK_PROCESSING"
        Service->>DB: INSERT into fulfillment_orders (STATUS='FALLBACK_PROCESSING')
        Service-->>Client: HTTP 200 Fallback Accepted (Graceful Degradation)
    end
```

---

## 🛠️ 3. L2/L3 Incident Management & Triage Workflow

```mermaid
flowchart LR
    A["🚨 Incident Alert\n(Dynatrace CPU Spike / Splunk Error)"] --> B["1. Host Health Check\n(scripts/rhel-health-check.sh)"]
    B --> C["2. Port & Daemon Verification\n(ss -tulpn / systemctl status)"]
    C --> D{"Diagnostic Routing"}

    D -->|High CPU / Memory Leak| E["Execute scripts/rhel-thread-dump.sh\n(top -H & jcmd Thread.print)"]
    D -->|DB Latency / Pool Exhaustion| F["Query Oracle v$session & v$lock\nCheck HikariCP active count"]
    D -->|API Error / 5xx Spike| G["Query Splunk by MDC traceId\nindex=main status='ERROR'"]

    E --> H["Analyze Heap Dump in MAT &\nTune JVM Flags (-Xmx / G1GC)"]
    F --> I["Gather DBMS_STATS &\nAdd Function-Based Index"]
    G --> J["Issue Developer Defect Patch &\nUpdate Automated RHEL Scripts"]

    H --> K["✅ Service Restored & RCA Documented"]
    I --> K
    J --> K
```

### Detailed Incident Triage Procedures

| Incident Type | Diagnostic Command / Tool | Action Plan & Root Cause Resolution |
| :--- | :--- | :--- |
| **High CPU / JVM Deadlock** | `scripts/rhel-thread-dump.sh`<br>`top -H -p <pid>`<br>`jcmd <pid> Thread.print` | 1. Convert LWP Thread ID to Hexadecimal (`printf "%x\n" <tid>`).<br>2. Search thread dump for `nid=0x<hex>` to identify blocked Java code.<br>3. Patch infinite loop or lock synchronization. |
| **OutOfMemoryError (`heap space`)** | `jcmd <pid> GC.heap_dump`<br>Eclipse MAT | 1. Open `.hprof` in Eclipse MAT.<br>2. Run **Leak Suspects Report** and inspect **Dominator Tree**.<br>3. Identify static collections retaining unclosed references.<br>4. Tune JVM options (`-Xmx2g -Xmx4g -XX:+UseG1GC`). |
| **Database Connection Exhaustion** | Oracle `v$session`, `v$lock`<br>`/actuator/prometheus` | 1. Monitor `hikaricp_connections_active` vs `hikaricp_connections_max`.<br>2. Inspect `v$session` for `STATUS='INACTIVE'` (unclosed JDBC leaks) vs `enqueue` wait events (locking).<br>3. Terminate blocking SID: `ALTER SYSTEM KILL SESSION 'sid,serial#' IMMEDIATE;`. |
| **Disk Full Outage (`/var/log`)** | `df -h /var/log`<br>`lsof +L1 /var/log` | 1. If files were removed via `rm`, locate unreleased file handles using `lsof +L1`.<br>2. Truncate file descriptor to 0 bytes: `> /proc/<PID>/fd/<FD_NUM>`.<br>3. Configure `logrotate` with `copytruncate`. |

---

## 🤖 4. Autonomous Multi-Agent AI Operations (Google ADK)

```mermaid
flowchart TD
    subgraph Master ["Master Support Layer"]
        Orchestrator["Master Support Orchestrator\n(agents/orchestrator_agent.py)"]
    end

    subgraph Subagents ["Specialized L2/L3 Subagent Layer"]
        FulfillmentAgent["Fulfillment App Agent\n(agents/fulfillment_agent.py)"]
        InventoryAgent["Inventory Resilience Agent\n(agents/inventory_agent.py)"]
        DatabaseAgent["Database & Redis Agent\n(agents/database_agent.py)"]
    end

    subgraph Tools ["Python Diagnostic Tool Suite"]
        ToolApp["fulfillment_tools.py\n- check_fulfillment_health()\n- inspect_recent_app_logs()\n- get_prometheus_metrics()"]
        ToolInv["inventory_tools.py\n- check_circuit_breaker_status()\n- simulate_circuit_breaker_trip()"]
        ToolDB["database_tools.py\n- check_database_pool_metrics()\n- check_redis_cache_status()"]
    end

    Orchestrator -->|Delegates Task| FulfillmentAgent
    Orchestrator -->|Delegates Task| InventoryAgent
    Orchestrator -->|Delegates Task| DatabaseAgent

    FulfillmentAgent --> ToolApp
    InventoryAgent --> ToolInv
    DatabaseAgent --> ToolDB

    ToolApp -->|Health & Log Data| Orchestrator
    ToolInv -->|Resilience Metrics| Orchestrator
    ToolDB -->|Connection Pool Stats| Orchestrator

    Orchestrator --> Report["Synthesized STAR Incident Triage Report\n(JSON Output)"]
```

---

## ⚙️ 5. RHEL Systemd Daemon Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Uninstalled
    Uninstalled --> ServiceFileCreated: Run scripts/rhel-systemd-setup.sh
    ServiceFileCreated --> DaemonReloaded: systemctl daemon-reload
    DaemonReloaded --> Stopped: systemctl enable resilient-fulfillment
    Stopped --> Running: systemctl start resilient-fulfillment
    
    state Running {
        [*] --> ActiveHealth: HTTP 200 /actuator/health
        ActiveHealth --> FailureDetected: Exception / Crash
        FailureDetected --> AutoRestart: Restart=always (Wait 10s)
        AutoRestart --> ActiveHealth
    }
    
    Running --> Stopped: systemctl stop resilient-fulfillment
    Stopped --> [*]
```

---

## 📑 6. Complete RHEL Automation Script Index

All scripts are stored in the [`scripts/`](file:///Users/anthonyjoyner/Documents/Projects/ResilientFulfillmentService/scripts/) directory:

| Script Name | Target Environment | Key Purpose | Primary Shell Commands Used |
| :--- | :--- | :--- | :--- |
| [`scripts/rhel-health-check.sh`](file:///Users/anthonyjoyner/Documents/Projects/ResilientFulfillmentService/scripts/rhel-health-check.sh) | RHEL 8/9 / Production | 5-minute automated host & app health monitoring. | `pgrep`, `free -m`, `curl`, `df -h`, `grep` |
| [`scripts/rhel-thread-dump.sh`](file:///Users/anthonyjoyner/Documents/Projects/ResilientFulfillmentService/scripts/rhel-thread-dump.sh) | RHEL 8/9 / Production | High CPU thread triage & JVM thread dump capture. | `top -H`, `jcmd`, `jstack`, `kill -3` |
| [`scripts/rhel-systemd-setup.sh`](file:///Users/anthonyjoyner/Documents/Projects/ResilientFulfillmentService/scripts/rhel-systemd-setup.sh) | RHEL 8/9 / Infrastructure | Provisioning systemd daemons with restart policies. | `useradd`, `systemctl daemon-reload`, `chmod` |
| [`scripts/system_health_check.sh`](file:///Users/anthonyjoyner/Documents/Projects/ResilientFulfillmentService/scripts/system_health_check.sh) | RHEL / OS Audit | System uptime & journalctl log aggregation. | `uptime`, `systemctl`, `journalctl` |

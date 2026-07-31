# 🎯 3:00 PM EST Interview Preparation Cheat Sheet
## Java Application Support Analyst — Global Financial Institution (Genesis10)

> **Role Focus**: Production Application Support (L2/L3), JVM & JBoss Troubleshooting, Oracle/SQL Performance, Splunk & Dynatrace Observability, RHEL Linux Automation, Network Concepts, and Resilience Architecture.

---

## 🚀 1. The 60-Second Elevator Pitch

> *"I am a Senior Application Support Engineer with extensive hands-on experience supporting mission-critical Java enterprise systems in high-throughput financial environments. My core expertise lies in maintaining high availability and resolving complex production incidents across multi-tier architectures—combining deep Java/JVM diagnostic skills (thread dumps, heap analysis, GC tuning) with relational databases like Oracle SQL and NoSQL caching layers like Redis. I leverage Splunk for MDC log tracing and Dynatrace for APM metric monitoring, while automating operational tasks and system health checks using RHEL Linux scripting. I pride myself on taking ownership during P1/P2 outage events, driving rapid root-cause analysis (RCA), and collaborating across development, infrastructure, and release management teams to guarantee strict SLA compliance."*

---

## 🧠 2. Top 5 High-Yield Technical Interview Scenarios

### Scenario 1: JVM Memory Leak / High CPU / OutOfMemoryError (`java.lang.OutOfMemoryError: Java heap space`)
* **Interviewer Asks**: *"How do you troubleshoot a Java application running on JBoss/JVM when memory utilization hits 95% or CPU spikes to 100%?"*
* **Your Answer**:
  1. **Triage & Isolate**: Check **Dynatrace** process metrics to identify whether CPU spike is driven by Garbage Collection (`jvm_gc_overhead_percent`) or runaway worker threads.
  2. **Collect Diagnostics (RHEL Linux)**:
     - Check thread states: `top -H -p <pid>` to locate the high-CPU thread ID (convert PID to Hex).
     - Generate Thread Dump: `jstack <pid> > /var/log/fulfillment-service/thread_dump.txt` or `kill -3 <pid>`.
     - Generate Heap Dump: `jcmd <pid> GC.heap_dump /tmp/heap_dump.hprof`.
  3. **Analyze**: Use Eclipse MAT (Memory Analyzer Tool) or `jhat` to locate memory leaks (e.g., static collections retaining dead objects or unclosed database connections).
  4. **Remediate**: Adjust JVM flags (`-Xms2g -Xmx4g -XX:+UseG1GC`) and file an immediate bug fix ticket for memory leak patching.

---

### Scenario 2: Splunk & Dynatrace Production Incident Investigation
* **Interviewer Asks**: *"An alert fires for high 500 error rates on an outbound fulfillment API during peak market hours. Walk me through your troubleshooting workflow."*
* **Your Answer**:
  1. **Dynatrace APM Overview**: Check Dynatrace response time breakdown to verify if latency is coming from the JVM app, database queries, or downstream HTTP dependencies.
  2. **Splunk MDC Log Trace**: Copy the MDC `traceId` from Dynatrace and run an SPL search in Splunk:
     ```splunk
     index=main "resilient-fulfillment-service" status="FALLBACK_PROCESSING" | stats count by status
     ```
  3. **Root Cause Identification**: Identify whether exceptions are `PSQLException` (database pool exhaustion) or `ConnectTimeoutException` (downstream service timeout).
  4. **Mitigation**: Verify if Resilience4j **Circuit Breakers** tripped to `OPEN` state to protect thread pools, enabling graceful degradation while downstream services recover.

---

### Scenario 3: Database Latency & Connection Pool Exhaustion (Oracle SQL / PostgreSQL)
* **Interviewer Asks**: *"How do you diagnose slow database queries or HikariCP/Db connection timeouts?"*
* **Your Answer**:
  1. **Connection Pool Metrics**: Check `hikaricp_connections_active` vs `hikaricp_connections_max` via Prometheus Actuator metrics (`/actuator/prometheus`).
  2. **Identify Long-Running Queries**: Query Oracle `v$session` or `v$sql` (or PostgreSQL `pg_stat_activity`) for active blocking locks and unindexed table scans.
  3. **Resolution**: Ensure database queries utilize secondary indexes, check connection timeout parameters (`hikari.connection-timeout=5000ms`), and verify connection leak detection is active (`leak-detection-threshold=2000ms`).

---

### Scenario 4: RHEL Linux Scripting & Automated Health Checks
* **Interviewer Asks**: *"How do you automate system health checks and daemon management on Red Hat Enterprise Linux?"*
* **Your Answer**:
  1. **Systemd Daemon Control**: Configure applications as systemd daemons (`/etc/systemd/system/resilient-fulfillment.service`) with automated restart policies (`Restart=on-failure`).
  2. **Bash Automation**: Write automated diagnostic scripts (`scripts/rhel-health-check.sh`) checking:
     - Disk space: `df -h`
     - Listening ports: `ss -tulpn | grep 8080`
     - Health API status: `curl -f http://localhost:8080/actuator/health`
  3. **Log Rotation**: Configure `logrotate` to prevent disk full outages.

---

### Scenario 5: Network Concepts (Load Balancing, Proxy, Firewalls)
* **Interviewer Asks**: *"How do network components like F5 Load Balancers and proxies fit into your application support workflow?"*
* **Your Answer**:
  1. **Health Probes**: Load balancers (F5 / OpenShift Edge Routers) poll `/actuator/health` or `/api/v1/orders/health`. If a node fails 3 consecutive probes, it is automatically removed from the active pool.
  2. **Firewall & Connectivity Triage**: Use `nc -zv <host> <port>` or `telnet <host> <port>` on RHEL to verify TCP firewall ingress/egress permissions.
  3. **Proxy Headers**: Inspect `X-Forwarded-For` and `X-Forwarded-Proto` HTTP headers to trace client IP addresses through corporate proxies.

---

## 🛠️ 3. Technologies & Key Terms Reference Sheet

| Technology | Core Function | Interview Talking Point |
| :--- | :--- | :--- |
| **Java 17 / JVM** | Core Runtime | Garbage Collection (G1GC), Heap Memory (`-Xms`/`-Xmx`), Thread Dumps (`jstack`). |
| **JBoss / Tomcat** | Enterprise App Server | Thread pool sizing (`maxThreads`), WAR/JAR deployments, standalone.xml configuration. |
| **Oracle / SQL** | ACID Transactional Persistence | Transactions, indexing, execution plans (`EXPLAIN PLAN`), connection pooling (HikariCP). |
| **Redis** | High-Speed NoSQL Caching | Key-Value cache (`ProductCache`), TTL expiry (600s), cache hits vs misses, reduced DB load. |
| **Splunk** | Log Aggregation & Analytics | SPL queries (`index=main`), MDC trace ID correlation, structured JSON logging. |
| **Dynatrace** | Application Performance Monitoring | APM, host metrics, CPU/memory bottleneck analysis, synthetic availability monitoring. |
| **Resilience4j** | Fault-Tolerance Architecture | Circuit Breakers (`CLOSED`, `OPEN`, `HALF_OPEN`), Bulkhead thread isolation. |
| **RHEL Linux** | Enterprise OS Platform | Systemd daemons, `top`, `jstack`, `df -h`, `ss -tulpn`, automated bash health scripts. |

---

## 📋 4. Questions to Ask the Interviewer (Demonstrates Senior Maturity)

1. *"What does the current L2/L3 support rotation and escalation workflow look like between the Business Technology Groups and Application Development teams?"*
2. *"Are the Dynatrace APM alerts and Splunk dashboards integrated into an automated ticketing platform like ServiceNow or Jira Service Management?"*
3. *"How are release deployments managed across the Charlotte and Richmond environments—is it primarily OpenShift containerized deployments or RHEL systemd services?"*

# ⚡ Resilient Fulfillment Microservice & Learning Dashboard

A production-grade, highly available microservice built with **Java 17 / Spring Boot 3**, **PostgreSQL** (ACID relational persistence), **Redis** (high-speed NoSQL caching), **Resilience4j** (Bulkhead & Circuit Breaker fault-tolerance patterns), **Actuator / Prometheus / Dynatrace / Splunk** observability, and **Docker Compose / RHEL systemd / OpenShift** infrastructure deployment.

---

## 🎨 Interactive Frontend Dashboard

When the application is running, open your browser and navigate to:
👉 **[http://localhost:8080](http://localhost:8080)**

The dashboard includes:
* **Interactive Scenario Buttons**: Trigger normal orders, downstream service failures, or latency spikes with 1 click.
* **Educational Tooltips**: Every button/control contains a tooltip explaining its corresponding **System Design & Microservice Learning Objective**.
* **Live API Output Console**: Displays real-time terminal logs with MDC trace IDs, latency response timing (ms), and HTTP status.
* **Quick-Access Dashboard Links**: Direct links to Actuator, Prometheus, Circuit Breaker metrics, and database queries.

---

## 🔗 Endpoints & Dashboard Directory

### 1. Web & Application APIs

| HTTP Method | Endpoint | Description | Learning Objective Demonstrated |
| :--- | :--- | :--- | :--- |
| **GET** | `/` | **Interactive Learning Dashboard UI** | Full-Stack UI, Educational Tooltips, Live Console |
| **POST** | `/api/v1/orders` | Process New Order | Dual Persistence (Redis NoSQL + PostgreSQL SQL) |
| **GET** | `/api/v1/orders` | List All Orders | Relational SQL Query (`fulfillment_orders` table) |
| **GET** | `/api/v1/orders/{orderNumber}` | Get Order Details | Order Tracking & Database Lookup |
| **GET** | `/api/v1/orders/health` | Service Uptime API | Basic Application Uptime & Timestamp Check |

---

### 2. Observability & APM Dashboard Endpoints (Dynatrace / Splunk / Prometheus)

| Endpoint | Description | Monitoring Tool Integration |
| :--- | :--- | :--- |
| **`/actuator/prometheus`** | OpenTelemetry / Prometheus metric stream | **Dynatrace ActiveGate** APM ingestion |
| **`/actuator/health`** | Live Readiness & Liveness health status | Kubernetes / OpenShift / F5 Load Balancer probes |
| **`/actuator/metrics`** | Index of all active Micrometer meters | Application metrics overview |
| **`/actuator/metrics/resilience4j.circuitbreaker.state`** | Live Circuit Breaker state metric (`CLOSED`, `OPEN`, `HALF_OPEN`) | Dynatrace / Grafana Alerting |
| **`/actuator/metrics/fulfillment.orders.processing.latency`** | $p50, p95, p99$ response latency distribution | Dynatrace SLA tracking |

---

## 🧪 Testing Scenario Payloads (`POST /api/v1/orders`)

### Scenario A: Normal Transaction (SQL + NoSQL Cache)
```json
{
  "productId": "PROD-100",
  "quantity": 2,
  "pricePerUnit": 49.99,
  "customerEmail": "customer@example.com"
}
```
* **Behavior**: Checks/populates Redis `ProductCache` ($TTL=600\text{s}$), verifies inventory, and saves Order to PostgreSQL with status `FULFILLED`.

---

### Scenario B: Downstream Failure (Resilience4j Circuit Breaker)
```json
{
  "productId": "PROD-FAIL",
  "quantity": 1,
  "pricePerUnit": 100.00,
  "customerEmail": "fallback@example.com"
}
```
* **Behavior**: Simulates downstream Inventory Service exception. Resilience4j catches the exception and routes the order to `FALLBACK_PROCESSING` in PostgreSQL to ensure **zero data loss**.

---

### Scenario C: Latency Spike & Bulkhead (3000ms Latency)
```json
{
  "productId": "PROD-SLOW",
  "quantity": 1,
  "pricePerUnit": 89.99,
  "customerEmail": "latency@example.com"
}
```
* **Behavior**: Introduces a 3000ms delay. Demonstrates Bulkhead concurrency caps (`maxConcurrentCalls=5`) and slow-call rate thresholds.

---

## 🚀 Deployment Options

### Option 1: Docker Compose (Recommended Local Setup)
```bash
# Build & Launch PostgreSQL, Redis, and Spring Boot Stack
docker compose up --build
```

### Option 2: RHEL Linux Daemon (`systemd`)
```bash
# Install systemd service & create /var/log/fulfillment-service log files
sudo bash scripts/rhel-systemd-setup.sh
sudo systemctl start resilient-fulfillment

# Execute RHEL Host Health Check
./scripts/rhel-health-check.sh
```

### Option 3: Red Hat OpenShift Container Platform
```bash
# Login to OpenShift Cluster
oc login --token=sha256~Rpv-wxlvGVGDJeGLNlebKNN2Tlo8CSE56wvfdK4wX9M --server=https://api.rm2.thpm.p1.openshiftapps.com:6443

# Deploy to acjoyner-dev namespace
oc apply -f infra/openshift/resilient-fulfillment-deployment.yaml
```

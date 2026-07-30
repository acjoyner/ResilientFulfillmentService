#!/bin/bash
# ==============================================================================
# RHEL 8/9 System Health Check & Automated Diagnostic Script
# Resilient Fulfillment Microservice Observability Tool
# ==============================================================================

SERVICE_PORT=8080
HEALTH_URL="http://localhost:${SERVICE_PORT}/api/v1/orders/health"
ACTUATOR_HEALTH="http://localhost:${SERVICE_PORT}/actuator/health"
LOG_FILE="/var/log/fulfillment-service/resilient-fulfillment.log"

echo "========================================================================"
echo "          RHEL 8/9 SYSTEM DIAGNOSTIC & HEALTH CHECK REPORT              "
echo "========================================================================"
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "Host: $(hostname)"
echo "Kernel: $(uname -r)"
echo "OS Release: $(cat /etc/redhat-release 2>/dev/null || echo 'macOS / Development Environment')"
echo "------------------------------------------------------------------------"

# 1. Process Status Check
echo -n "[1/5] Checking Java Process Status... "
PID=$(pgrep -f "resilient-fulfillment-service" || pgrep -f "java")
if [ -n "$PID" ]; then
    echo "STATUS: UP (PID: $PID)"
else
    echo "STATUS: DOWN (Process not detected)"
fi

# 2. System Memory & Swap Check
echo "------------------------------------------------------------------------"
echo "[2/5] Memory & Resource Usage:"
if command -v free &>/dev/null; then
    free -m
else
    vm_stat | head -n 5
fi

# 3. Port & HTTP Health Check
echo "------------------------------------------------------------------------"
echo -n "[3/5] HTTP API Endpoint Health (${HEALTH_URL})... "
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "${HEALTH_URL}" 2>/dev/null || echo "000")

if [ "$HTTP_CODE" -eq 200 ]; then
    echo "STATUS: OK (HTTP 200)"
    echo "Response: $(curl -s "${HEALTH_URL}")"
else
    echo "STATUS: UNHEALTHY (HTTP $HTTP_CODE)"
fi

# 4. Actuator & Circuit Breaker Metric Check
echo "------------------------------------------------------------------------"
echo "[4/5] Actuator & Circuit Breaker State Check:"
ACTUATOR_RESP=$(curl -s --max-time 5 "${ACTUATOR_HEALTH}" 2>/dev/null)
if [ -n "$ACTUATOR_RESP" ]; then
    echo "$ACTUATOR_RESP"
else
    echo "Actuator endpoint unreachable at ${ACTUATOR_HEALTH}"
fi

# 5. Disk Space & Log Trail Inspection
echo "------------------------------------------------------------------------"
echo "[5/5] Disk Space Utilization & Log Status:"
df -h / | tail -n 1

if [ -f "$LOG_FILE" ]; then
    echo "Recent log errors in ${LOG_FILE}:"
    grep -i "ERROR\|WARN" "$LOG_FILE" | tail -n 5 || echo "No recent error entries."
else
    echo "Log file ${LOG_FILE} not found at default RHEL path (app running locally)."
fi

echo "========================================================================"
echo "                     DIAGNOSTIC CHECK COMPLETE                          "
echo "========================================================================"

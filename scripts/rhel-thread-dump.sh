#!/bin/bash
# ==============================================================================
# RHEL 8/9 High CPU & Thread Dump Diagnostic Tool
# NexaBank Global Financial Enterprise Java Support Script
# ==============================================================================

SERVICE_NAME="resilient-fulfillment"
LOG_DIR="/var/log/fulfillment-service"
DUMP_DIR="/tmp/thread_dumps"

mkdir -p "$DUMP_DIR"

echo "========================================================================"
# 1. Identify Java Process
PID=$(pgrep -f "$SERVICE_NAME" || pgrep -f "java" | head -n 1)

if [ -z "$PID" ]; then
    echo "ERROR: No active Java process found on host!"
    exit 1
fi

echo "Active Java PID: $PID"
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
echo "------------------------------------------------------------------------"

# 2. Top CPU Threads (LWP / TID)
echo "[1/3] Fetching top 5 CPU consuming threads for PID $PID..."
if command -v top &>/dev/null; then
    top -b -n 1 -H -p "$PID" | head -n 15
fi

# 3. Generate Thread Dump via jcmd / jstack
DUMP_FILE="${DUMP_DIR}/thread_dump_${PID}_$(date +%Y%m%d_%H%M%S).txt"
echo "------------------------------------------------------------------------"
echo "[2/3] Capturing JVM Thread Dump to ${DUMP_FILE}..."

if command -v jcmd &>/dev/null; then
    jcmd "$PID" Thread.print > "$DUMP_FILE"
elif command -v jstack &>/dev/null; then
    jstack "$PID" > "$DUMP_FILE"
else
    echo "Falling back to kill -3..."
    kill -3 "$PID"
fi

echo "Thread dump generated successfully."

# 4. Summary of Thread States
echo "------------------------------------------------------------------------"
echo "[3/3] Thread State Breakdown:"
if [ -f "$DUMP_FILE" ]; then
    grep "java.lang.Thread.State" "$DUMP_FILE" | sort | uniq -c
fi

echo "========================================================================"

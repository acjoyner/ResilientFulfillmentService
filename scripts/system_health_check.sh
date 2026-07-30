#!/bin/bash
# Filename: system_health_check.sh
# Purpose: Automate checking critical service health and log aggregation on a RHEL host.
# Designed to be executed via cronjob or a central monitoring agent.

set -e # Exit immediately if a command exits with a non-zero status.

LOG_DIR="/var/log"
SERVICE_LIST=("sshd" "systemd-journald" "nginx" "java")
REPORT_FILE="./system_report_$(date +%Y%m%d_%H%M).txt"

echo "--- System Health Report: $(date) ---" > "$REPORT_FILE"
echo "System Uptime:" >> "$REPORT_FILE"
uptime >> "$REPORT_FILE"
echo -e "\n--- Service Status Check ---" >> "$REPORT_FILE"

# 1. Check service status using systemctl (RHEL native command)
for svc in "${SERVICE_LIST[@]}"; do
    if systemctl is-active --quiet "$svc" 2>/dev/null; then
        echo "[PASS] $svc is running." >> "$REPORT_FILE"
    else
        echo "[WARN/FAIL] $svc is currently stopped or inactive." >> "$REPORT_FILE"
    fi
done

# 2. Log Aggregation using journalctl for structured review
echo -e "\n--- Recent System Journal Logs (Last 500 lines) ---" >> "$REPORT_FILE"
if command -v journalctl &>/dev/null; then
    journalctl -b -n 500 --no-pager >> "$REPORT_FILE" 2>/dev/null || echo "journalctl output unavailable." >> "$REPORT_FILE"
else
    echo "journalctl command not present on this host environment." >> "$REPORT_FILE"
fi

echo "=====================================================" >> "$REPORT_FILE"
echo "✅ System health check completed successfully." >> "$REPORT_FILE"
echo "Full report generated at: $REPORT_FILE"

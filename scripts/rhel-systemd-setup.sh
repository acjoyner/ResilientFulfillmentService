#!/bin/bash
# ==============================================================================
# RHEL Systemd Service Setup Script for Resilient Fulfillment Service
# Target OS: Red Hat Enterprise Linux 8 / 9
# ==============================================================================

SERVICE_NAME="resilient-fulfillment"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
APP_DIR="/opt/fulfillment-service"
APP_JAR="${APP_DIR}/resilient-fulfillment-service-1.0.0-SNAPSHOT.jar"
LOG_DIR="/var/log/fulfillment-service"
APP_USER="fulfillment"

echo "=== Beginning RHEL Systemd Service Installation ==="

# Step 1: Create application user and log directories if they don't exist
if ! id "${APP_USER}" &>/dev/null; then
    echo "Creating system service user: ${APP_USER}"
    useradd -r -s /sbin/nologin "${APP_USER}"
fi

mkdir -p "${APP_DIR}" "${LOG_DIR}"
chown -R "${APP_USER}:${APP_USER}" "${APP_DIR}" "${LOG_DIR}"
chmod 755 "${APP_DIR}" "${LOG_DIR}"

# Step 2: Write systemd service file
cat <<EOF > "${SERVICE_FILE}"
[Unit]
Description=Resilient Order Fulfillment Microservice
After=syslog.target network.target postgresql.service redis.service

[Service]
Type=simple
User=${APP_USER}
Group=${APP_USER}
WorkingDirectory=${APP_DIR}
ExecStart=/usr/bin/java -Xms512m -Xmx1024m -XX:+UseG1GC -jar ${APP_JAR}
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=${SERVICE_NAME}

# Resource limits & security hardening
LimitNOFILE=65536
PrivateTmp=true
ProtectSystem=full

[Install]
WantedBy=multi-user.target
EOF

chmod 644 "${SERVICE_FILE}"

echo "=== Systemd Service File Generated at ${SERVICE_FILE} ==="
echo "Reloading systemd daemon..."
systemctl daemon-reload

echo "Service configuration completed."
echo "Commands to manage service:"
echo "  sudo systemctl start ${SERVICE_NAME}"
echo "  sudo systemctl enable ${SERVICE_NAME}"
echo "  sudo systemctl status ${SERVICE_NAME}"

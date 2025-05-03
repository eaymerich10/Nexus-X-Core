#!/bin/bash

set -e

SERVICE_NAME="nexus-x-core"
PROJECT_DIR=$(dirname "$(realpath "$0")")

echo "🛑 Parando y deshabilitando el servicio..."
sudo systemctl stop "$SERVICE_NAME"
sudo systemctl disable "$SERVICE_NAME"

echo "🗑 Eliminando archivo de servicio..."
sudo rm -f /etc/systemd/system/"$SERVICE_NAME".service
sudo systemctl daemon-reload
sudo systemctl reset-failed

echo "🧹 Eliminando entorno virtual..."
rm -rf "$PROJECT_DIR/.venv311"

echo "✅ NEXUS-X Core desinstalado completamente."

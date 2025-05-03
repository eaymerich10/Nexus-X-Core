#!/bin/bash

set -e

SERVICE_NAME="nexus-x-core"
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"
PROJECT_DIR=$(dirname "$(realpath "$0")")

echo "Parando y deshabilitando el servicio (user)..."
systemctl --user stop "$SERVICE_NAME"
systemctl --user disable "$SERVICE_NAME"

echo "Eliminando archivo de servicio..."
rm -f "$SYSTEMD_USER_DIR/$SERVICE_NAME.service"
systemctl --user daemon-reload
systemctl --user reset-failed

echo "Eliminando entorno virtual..."
rm -rf "$PROJECT_DIR/.venv311"

echo "NEXUS-X Core desinstalado completamente (user)."

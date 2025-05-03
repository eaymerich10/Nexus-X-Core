#!/bin/bash

set -e

PROJECT_DIR=$(dirname "$(realpath "$0")")
VENV_DIR="$PROJECT_DIR/.venv311"
PYTHON_EXEC="$VENV_DIR/bin/python"
SERVICE_NAME="nexus-x-core"
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"
SERVICE_FILE="$SYSTEMD_USER_DIR/$SERVICE_NAME.service"

echo "Instalando NEXUS-X Core..."

# Crear entorno virtual si no existe
if [ ! -d "$VENV_DIR" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv "$VENV_DIR"
    "$PYTHON_EXEC" -m pip install --upgrade pip
fi

# Instalar dependencias
echo "Instalando dependencias..."
"$PYTHON_EXEC" -m pip install -r requirements.txt

# Crear carpeta systemd --user si no existe
mkdir -p "$SYSTEMD_USER_DIR"

# Crear servicio systemd --user
echo "Configurando servicio systemd --user..."

cat > "$SERVICE_FILE" <<EOL
[Unit]
Description=NEXUS-X Core Assistant Service (User)
After=network.target

[Service]
WorkingDirectory=$PROJECT_DIR
ExecStart=$PYTHON_EXEC -m scripts.run
Restart=always
Environment=PYTHONUNBUFFERED=1
Environment=PYTHONPATH=$PROJECT_DIR

[Install]
WantedBy=default.target
EOL

# Recargar systemd --user, habilitar y arrancar servicio
echo "Habilitando y arrancando servicio (user)..."
systemctl --user daemon-reload
systemctl --user enable "$SERVICE_NAME"
systemctl --user restart "$SERVICE_NAME"

echo "NEXUS-X Core instalado y ejecutándose como servicio de usuario."
echo "Usa 'systemctl --user status $SERVICE_NAME' para comprobar el estado."
echo "Usa 'journalctl --user -u $SERVICE_NAME -f' para seguir los logs en tiempo real."

#!/bin/bash

set -e

PROJECT_DIR=$(dirname "$(realpath "$0")")
VENV_DIR="$PROJECT_DIR/.venv311"
PYTHON_EXEC="$VENV_DIR/bin/python"
SERVICE_NAME="nexus-x-core"

echo "🚀 Instalando NEXUS-X Core..."

# Crear entorno virtual si no existe
if [ ! -d "$VENV_DIR" ]; then
    echo "🐍 Creando entorno virtual..."
    python3 -m venv "$VENV_DIR"
    "$PYTHON_EXEC" -m pip install --upgrade pip
fi

# Instalar dependencias
echo "📦 Instalando dependencias..."
"$PYTHON_EXEC" -m pip install -r requirements.txt

# Crear servicio systemd
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"

echo "⚙️ Configurando servicio systemd..."

sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=NEXUS-X Core Assistant Service
After=network.target

[Service]
WorkingDirectory=$PROJECT_DIR
ExecStart=$PYTHON_EXEC -m scripts.run
Restart=always
User=$USER
Environment=PYTHONUNBUFFERED=1
Environment=PYTHONPATH=$PROJECT_DIR

[Install]
WantedBy=multi-user.target
EOL

# Recargar systemd, habilitar y arrancar servicio
echo "🔄 Habilitando y arrancando servicio..."
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"

echo "✅ NEXUS-X Core instalado y ejecutándose como servicio."
echo "👉 Usa 'sudo systemctl status $SERVICE_NAME' para comprobar el estado."

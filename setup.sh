#!/bin/bash

echo "🔧 Setting up NEXUS-X Core..."

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias del sistema
sudo apt install -y python3 python3-pip python3-venv git sox alsa-utils portaudio19-dev

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias de Python
pip install -r requirements.txt

echo "✅ Setup completo. No olvides añadir tu clave OpenAI en el archivo .env"

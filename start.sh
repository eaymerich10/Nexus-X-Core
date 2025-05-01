#!/bin/bash

SOCKET_PATH="/tmp/wakeword_socket"

echo "🚀 Arrancando wakeword_listener.py..."
python -m wakeword_system.wakeword_listener &
PID_WAKEWORD=$!

# Esperar a que se cree el socket
echo "⏳ Esperando a que wakeword_listener cree el socket..."
while [ ! -e $SOCKET_PATH ]; do
    sleep 0.5
done

echo "🚀 Arrancando main_assistant.py..."
python -m wakeword_system.main_assistant

echo "🛑 Terminando wakeword_listener.py..."
kill $PID_WAKEWORD

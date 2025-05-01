import socket
import time
from services.speech.speech_service import SpeechService

SOCKET_PATH = "/tmp/wakeword_socket"

client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

try:
    client.connect(SOCKET_PATH)
    print("🎧 [Assistant] Conectado al wakeword_listener.py")

    speech_service = SpeechService()

    while True:
        print("🎧 [Assistant] Esperando señal de activación...")
        data = client.recv(1024)
        if not data:
            print("⚠️ [Assistant] Conexión cerrada por el servidor, saliendo...")
            break
        if data.strip() == b"WAKE":
            print("🎧 [Assistant] Activación recibida. Iniciando grabación...")
            time.sleep(0.5)
            transcription = speech_service.listen_and_transcribe()
            print(f"🗣 [Assistant] Transcripción: {transcription}")

except KeyboardInterrupt:
    print("🛑 [Assistant] Detenido por usuario.")
except ConnectionResetError:
    print("❗ [Assistant] Conexión perdida con wakeword_listener.")
finally:
    client.close()
    print("✅ [Assistant] Socket cerrado.")

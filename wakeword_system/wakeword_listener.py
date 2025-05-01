import socket
import os
import platform
from dotenv import load_dotenv
import pvporcupine
import pyaudio

# Cargar variables
load_dotenv()

if platform.machine() == 'x86_64':
    ACCESS_KEY = os.getenv("ACCESS_KEY_UBUNTU")
    KEYWORD_PATH = os.getenv("KEYWORD_PATH_UBUNTU")
elif platform.machine() == 'aarch64':
    ACCESS_KEY = os.getenv("ACCESS_KEY_RPI")
    KEYWORD_PATH = os.getenv("KEYWORD_PATH_RPI")
else:
    raise RuntimeError(f"❌ Plataforma no soportada: {platform.machine()}")

# Configurar socket
SOCKET_PATH = "/tmp/wakeword_socket"
if os.path.exists(SOCKET_PATH):
    os.remove(SOCKET_PATH)

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SOCKET_PATH)
server.listen(1)

# Inicializar Porcupine
porcupine = pvporcupine.create(
    access_key=ACCESS_KEY,
    keyword_paths=[KEYWORD_PATH]
)
pa = pyaudio.PyAudio()
audio_stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

print("🎤 [Wakeword] Esperando conexión...")
try:
    conn, _ = server.accept()
    print("✅ [Wakeword] Conexión establecida con main_assistant.py")

    while True:
        pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = [int.from_bytes(pcm[i:i+2], 'little', signed=True) for i in range(0, len(pcm), 2)]
        result = porcupine.process(pcm)
        if result >= 0:
            print("✅ [Wakeword] Activación detectada, notificando...")
            conn.sendall(b"WAKE\n")

except KeyboardInterrupt:
    print("🛑 [Wakeword] Detenido por usuario.")
except Exception as e:
    print(f"❗ [Wakeword] Error: {e}")
finally:
    audio_stream.stop_stream()
    audio_stream.close()
    pa.terminate()
    porcupine.delete()
    if 'conn' in locals():
        conn.close()
    server.close()
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)
    print("✅ [Wakeword] Socket cerrado y limpiado.")

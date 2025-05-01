import os
import platform
from dotenv import load_dotenv
import pvporcupine
import pyaudio

# Cargar variables desde .env
load_dotenv()

# Detectar plataforma
machine = platform.machine()

if machine == 'x86_64':
    ACCESS_KEY = os.getenv("ACCESS_KEY_UBUNTU")
    KEYWORD_PATH = os.getenv("KEYWORD_PATH_UBUNTU")
elif machine == 'aarch64':
    ACCESS_KEY = os.getenv("ACCESS_KEY_RPI")
    KEYWORD_PATH = os.getenv("KEYWORD_PATH_RPI")
else:
    raise RuntimeError(f"❌ Plataforma no soportada: {machine}")

if not ACCESS_KEY or not KEYWORD_PATH:
    raise ValueError("❌ AccessKey o KeywordPath no definidos para esta plataforma")

class WakeWordService:
    def __init__(self, access_key=ACCESS_KEY, keyword_path=KEYWORD_PATH):
        self.porcupine = pvporcupine.create(
            access_key=access_key,
            keyword_paths=[keyword_path]
        )
        self.pa = pyaudio.PyAudio()
        self.audio_stream = self.pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )

    def wait_for_wakeword(self):
        print("🎤 Esperando palabra de activación...")
        while True:
            pcm = self.audio_stream.read(self.porcupine.frame_length, exception_on_overflow=False)
            pcm = [int.from_bytes(pcm[i:i+2], 'little', signed=True) for i in range(0, len(pcm), 2)]
            result = self.porcupine.process(pcm)
            if result >= 0:
                print("✅ Palabra de activación detectada.")
                return True

    def cleanup(self):
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.porcupine.delete()
        self.pa.terminate()

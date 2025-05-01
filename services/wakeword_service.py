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
        self.access_key = access_key
        self.keyword_path = keyword_path
        self._initialize_porcupine()

    def _initialize_porcupine(self):
        self.porcupine = pvporcupine.create(
            access_key=self.access_key,
            keyword_paths=[self.keyword_path]
        )
        self.pa = pyaudio.PyAudio()
        self.audio_stream = self.pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )
        print("🎙️ [DEBUG] Wake word listener inicializado.")

    def wait_for_wakeword(self):
        print("🎤 Esperando palabra de activación...")
        while True:
            pcm = self.audio_stream.read(self.porcupine.frame_length, exception_on_overflow=False)
            pcm = [int.from_bytes(pcm[i:i+2], 'little', signed=True) for i in range(0, len(pcm), 2)]
            result = self.porcupine.process(pcm)
            if result >= 0:
                print("✅ Palabra de activación detectada.")
                return True

    def pause(self):
        if self.audio_stream.is_active():
            self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.pa.terminate()
        self.porcupine.delete()
        print("🎙️ [DEBUG] Wake word listener detenido y Porcupine destruido temporalmente.")

    def resume(self):
        self._initialize_porcupine()
        print("🎙️ [DEBUG] Wake word listener reactivado y Porcupine reinicializado.")

    def cleanup(self):
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.porcupine.delete()
        self.pa.terminate()
        print("🎙️ [DEBUG] Wake word listener limpiado completamente.")

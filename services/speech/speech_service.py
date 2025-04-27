import subprocess
import time
import os
from assistant.utils.settings_manager import load_settings  # 👈 Importamos el loader de configuración

class SpeechService:
    def __init__(self, whisper_path=None, model_path=None):
        # Cargar configuración de paths si no se pasan explícitamente
        _, _, _, _, whisper_path_cfg, model_path_cfg = load_settings()
        
        self.whisper_path = whisper_path or whisper_path_cfg
        self.model_path = model_path or model_path_cfg

        self.raw_file = "recording_raw.wav"
        self.wav_file = "recording.wav"
        self.device = "hw:2,0"  # Micro USB
        self.duration = 5       # Tiempo máximo de grabación en segundos
        self.language = "es"    # Idioma de transcripción

    def record_audio(self):
        """Graba audio desde el micrófono y para automáticamente cuando detecta silencio."""
        print("🎙️ [DEBUG] Empezando grabación con detección de silencio...")
        try:
            subprocess.run([
                "sox",
                "-t", "alsa", self.device,
                self.raw_file,
                "rate", "44100",
                "silence", "1", "0.1", "1%", "1", "1.5", "1%"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=self.duration + 5)
            print("🎙️ [DEBUG] Grabación terminada (detectó silencio o timeout).")
        except subprocess.TimeoutExpired:
            print("⏱️ [DEBUG] Grabación cortada automáticamente por timeout.")

    def resample_audio(self):
        """Convierte el audio grabado a 16000 Hz."""
        print("🎛️ [DEBUG] Empezando resampleo...")
        subprocess.run([
            "sox", self.raw_file,
            "-c", "1",
            "-r", "16000",
            self.wav_file
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("🎛️ [DEBUG] Resampleo terminado.")

    def transcribe_audio(self):
        """Transcribe el audio grabado usando whisper-cli."""
        print("🧠 [DEBUG] Empezando transcripción...")
        subprocess.run([
            self.whisper_path,
            "-m", self.model_path,
            "-f", self.wav_file,
            "-otxt",
            "-l", self.language
        ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        print("🧠 [DEBUG] Transcripción terminada.")

        txt_file = self.wav_file + ".txt"
        if os.path.exists(txt_file):
            with open(txt_file, "r", encoding="utf-8") as f:
                return f.read().strip()
        else:
            return ""

    def clean_temp_files(self):
        """Elimina archivos temporales de grabación."""
        for file in [self.raw_file, self.wav_file, self.wav_file + ".txt"]:
            if os.path.exists(file):
                os.remove(file)

    def listen_and_transcribe(self):
        """Captura voz y devuelve el texto transcrito."""
        try:
            self.record_audio()
            self.resample_audio()
            time.sleep(0.2)
            transcription = self.transcribe_audio()
            return transcription
        finally:
            self.clean_temp_files()

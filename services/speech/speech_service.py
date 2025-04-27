import subprocess
import time
import os

class SpeechService:
    def __init__(self, whisper_path="/home/nexus/whisper.cpp/whisper-cli", model_path="/home/nexus/whisper.cpp/whisper-cli/models/ggml-tiny.bin"):
        self.whisper_path = whisper_path
        self.model_path = model_path
        self.raw_file = "recording_raw.wav"
        self.wav_file = "recording.wav"
        self.device = "hw:1,0"  # Micro USB
        self.duration = 5       # Tiempo máximo de grabación en segundos
        self.language = "es"    # Idioma de transcripción

    def record_audio(self):
        """Graba audio desde el micrófono y para automáticamente cuando detecta silencio."""
        print("🎙️ [DEBUG] Empezando grabación con detección de silencio...")
        try:
            subprocess.run([
                "sox",
                "-t", "alsa", self.device,
                "-c", "1",
                "-b", "16",
                "-r", "48000",  # <<< Mejora a 48kHz
                "debug_audio.wav",
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

    def listen_and_transcribe(self):
        """Captura voz y devuelve el texto transcrito."""
        try:
            self.record_audio()
            self.resample_audio()
            time.sleep(0.5)  # 👈 Aumentamos para asegurar que recording.wav está escrito
            if not os.path.exists(self.wav_file):
                print("❗ [ERROR] Archivo de audio no encontrado:", self.wav_file)
                return ""
            transcription = self.transcribe_audio()
            return transcription
        finally:
            self.clean_temp_files()


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

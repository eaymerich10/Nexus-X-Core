import subprocess
import time
import os

class SpeechService:
    def __init__(self, whisper_path="/home/nexus/whisper.cpp/whisper-cli", model_path="/home/nexus/whisper.cpp/models/ggml-tiny.bin"):
        self.whisper_path = whisper_path
        self.model_path = model_path
        self.raw_file = os.path.abspath("recording_raw.wav")
        self.wav_file = os.path.abspath("recording.wav")
        self.device = "hw:2,0"  # Micro USB
        self.duration = 3       # Tiempo máximo de grabación en segundos
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
                "-r", "48000",
                self.raw_file,  # Graba en la ruta absoluta correcta
                "silence", "1", "0.1", "1%", "1", "1.5", "1%"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=self.duration + 5)
            print(f"🎙️ [DEBUG] Grabación terminada: {self.raw_file}")
        except subprocess.TimeoutExpired:
            print("⏱️ [DEBUG] Grabación cortada automáticamente por timeout.")

    def resample_audio(self):
        """Convierte el audio grabado a 16000 Hz."""
        print("🎛️ [DEBUG] Empezando resampleo...")
        result = subprocess.run([
            "sox", self.raw_file,
            "-c", "1",
            "-r", "16000",
            self.wav_file
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print("❗ [ERROR] Resampleo fallido:", result.stderr.decode())
        else:
            print("🎛️ [DEBUG] Resampleo terminado.")

    def transcribe_audio(self):
        """Transcribe el audio grabado usando whisper-cli."""
        print("🧠 [DEBUG] Empezando transcripción...")

        if not os.path.exists(self.wav_file):
            print(f"❗ [ERROR] Archivo de audio no encontrado: {self.wav_file}")
            return ""

        result = subprocess.run([
            self.whisper_path,
            "-m", self.model_path,
            "-f", self.wav_file,
            "-otxt",
            "-l", self.language
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        print("🧠 [DEBUG] STDOUT:", result.stdout)
        print("🧠 [DEBUG] STDERR:", result.stderr)

        txt_file = self.wav_file + ".txt"
        if os.path.exists(txt_file):
            with open(txt_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                print("🧠 [DEBUG] CONTENIDO TXT:", content)
                return content
        else:
            print("❗ [ERROR] No se generó el archivo de transcripción.")
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
            time.sleep(0.5)  # Pequeña espera extra para I/O en Raspberry
            transcription = self.transcribe_audio()
            return transcription
        finally:
            self.clean_temp_files()

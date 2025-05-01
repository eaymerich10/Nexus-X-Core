import subprocess
import time
import os

class SpeechService:
    def __init__(self, whisper_path="/home/nexus/whisper.cpp/whisper-cli", model_path="/home/nexus/whisper.cpp/models/ggml-base.bin"):
        base_dir = os.path.dirname(os.path.abspath(__file__))  # /services/speech
        project_root = os.path.abspath(os.path.join(base_dir, "../../"))  # sube dos niveles al root del proyecto

        self.whisper_path = whisper_path
        self.model_path = model_path
        self.wav_file = os.path.join(project_root, "recording.wav")
        self.clean_file = os.path.join(project_root, "recording_clean.wav")
        self.noise_profile = os.path.join(project_root, "utils", "noise.prof")
        self.language = "es"

    def resample_audio(self, input_file):
        print("🎛️ [DEBUG] Empezando resampleo...")
        result = subprocess.run([
            "sox", input_file,
            "-c", "1",
            "-r", "16000",
            self.wav_file
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("🎛️ [DEBUG] STDOUT:", result.stdout.decode())
        print("🎛️ [DEBUG] STDERR:", result.stderr.decode())

        if result.returncode != 0:
            print("❗ [ERROR] Resampleo fallido:", result.stderr.decode())
            return False
        else:
            print("🎛️ [DEBUG] Resampleo terminado.")
            return True

    def reduce_noise(self):
        if os.path.exists(self.noise_profile):
            print(f"🎚️ [DEBUG] Aplicando reducción de ruido usando {self.noise_profile}...")
            result = subprocess.run([
                "sox", self.wav_file, self.clean_file,
                "noisered", self.noise_profile, "0.21"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("🎚️ [DEBUG] STDOUT:", result.stdout.decode())
            print("🎚️ [DEBUG] STDERR:", result.stderr.decode())

            if result.returncode != 0:
                print("❗ [ERROR] Reducción de ruido fallida:", result.stderr.decode())
                self.clean_file = self.wav_file  # usa el archivo original si falla
        else:
            print(f"⚠️ [ADVERTENCIA] Perfil de ruido no encontrado en {self.noise_profile}, usando archivo sin limpiar.")
            self.clean_file = self.wav_file

    def transcribe_audio(self):
        print("🧠 [DEBUG] Empezando transcripción...")

        if not os.path.exists(self.clean_file):
            print(f"❗ [ERROR] Archivo de audio no encontrado: {self.clean_file}")
            return ""

        result = subprocess.run([
            self.whisper_path,
            "-m", self.model_path,
            "-f", self.clean_file,
            "-otxt",
            "-pp",
            "-l", self.language
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        print("🧠 [DEBUG] STDOUT:", result.stdout)
        print("🧠 [DEBUG] STDERR:", result.stderr)

        txt_file = self.clean_file + ".txt"
        if os.path.exists(txt_file):
            with open(txt_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                print("🧠 [DEBUG] CONTENIDO TXT:", content)
                return content
        else:
            print("❗ [ERROR] No se generó el archivo de transcripción.")
            return ""

    def clean_temp_files(self):
        for file in [self.wav_file, self.clean_file, self.clean_file + ".txt"]:
            if os.path.exists(file):
                os.remove(file)

    def process_wav_file(self, raw_file):
        try:
            if not self.resample_audio(raw_file):
                return ""
            self.reduce_noise()
            time.sleep(0.5)
            transcription = self.transcribe_audio()
            return transcription
        finally:
            self.clean_temp_files()

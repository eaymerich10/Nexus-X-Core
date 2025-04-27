from TTS.api import TTS
import subprocess
import os

class TTSService:
    def __init__(self):
        self.tts = TTS(model_name="tts_models/es/css10/vits", progress_bar=False, gpu=False)

    def speak(self, text):
        """Convierte texto en voz y lo reproduce."""
        if not text:
            return

        output_file = "nexus_response.wav"
        self.tts.tts_to_file(
            text=text,
            file_path=output_file
        )

        if os.path.exists(output_file):
            subprocess.run(["aplay", output_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

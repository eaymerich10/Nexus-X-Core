from TTS.api import TTS
import subprocess
import os
import contextlib
import sys

class TTSService:
    def __init__(self):
        self.tts = TTS(model_name="tts_models/es/css10/vits", progress_bar=False, gpu=False)

    def speak(self, text):
        if not text:
            return

        output_file = "nexus_response.wav"

        # Redirige stdout y stderr temporalmente a null
        with open(os.devnull, 'w') as fnull, contextlib.redirect_stdout(fnull), contextlib.redirect_stderr(fnull):
            self.tts.tts_to_file(
                text=text,
                file_path=output_file,
                speaker_wav=None,
                sample_rate=16000
            )

        if os.path.exists(output_file):
            subprocess.run(["aplay", output_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

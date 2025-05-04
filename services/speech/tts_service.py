import subprocess
import os
import contextlib
import sys

from TTS.api import TTS
from services.speech.tts_checker import check_tts_model

class TTSService:
    def __init__(self):
        model_path = os.path.expanduser("~/.local/share/tts/tts_models--es--css10--vits")
        check_tts_model(model_path)

        # Notificar en la GUI que ya está listo
        from gui.nexus_gui import update_gui_status
        update_gui_status("Cargando modelo TTS...")

        self.tts = TTS(model_name="tts_models/es/css10/vits", progress_bar=False, gpu=False)
        update_gui_status("Modelo TTS listo")

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

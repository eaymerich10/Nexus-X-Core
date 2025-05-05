import os
import json
import shutil
from gui import update_gui_status

def check_tts_model(model_path):
    config_file = os.path.join(model_path, 'config.json')

    # Si no existe la carpeta
    if not os.path.exists(model_path):
        msg = f"No se encontró la carpeta del modelo {model_path}. Se descargará al iniciar."
        print(msg)
        update_gui_status("Preparando modelo TTS (descarga inicial)...")
        return

    # Si no existe config.json
    if not os.path.exists(config_file):
        msg = f"No se encontró config.json en {model_path}. Borrando carpeta para forzar redescarga..."
        print(msg)
        update_gui_status("Reparando modelo TTS (faltaba config)...")
        shutil.rmtree(model_path)
        return

    # Si existe, pero está vacío o corrupto
    try:
        with open(config_file, 'r') as f:
            data = json.load(f)
        if not data:
            msg = f"config.json vacío en {model_path}. Borrando carpeta para forzar redescarga..."
            print(msg)
            update_gui_status("Reparando modelo TTS (config vacío)...")
            shutil.rmtree(model_path)
    except json.JSONDecodeError:
        msg = f"config.json corrupto en {model_path}. Borrando carpeta para forzar redescarga..."
        print(msg)
        update_gui_status("Reparando modelo TTS (config corrupto)...")
        shutil.rmtree(model_path)

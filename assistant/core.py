import os
import wave
import time
import platform
import pvporcupine
import pyaudio

from dotenv import load_dotenv
from assistant.context import ContextManager
from assistant.commands.router import handle_command
from services.ai_provider import get_response
from assistant.utils.settings_manager import (
    save_mode_to_config, load_settings
)
from services.speech.speech_service import SpeechService
from services.speech.tts_service import TTSService

VOICE_COMMAND_PATTERNS = [
    ("cambiar modo a", "/modo {value}"),
    ("mi idioma es", "/lang {value}"),
    ("cambiar proveedor a", "/proveedor {value}"),
    ("recuerda", "/recordar {value}"),
    ("cambiar entrada a", "/entrada {value}"),
]

FIXED_COMMANDS = {
    "dime el estado": "/estado",
    "dime en el estado": "/estado",
    "muéstrame el estado": "/estado",
    "reinicia": "/reiniciar",
    "reiniciar asistente": "/reiniciar",
    "modos disponibles": "/modos",
    "lista de modos": "/modos",
}

def preprocess_response(text):
    digit_map = {'0': "cero", '1': "uno", '2': "dos", '3': "tres", '4': "cuatro",
                 '5': "cinco", '6': "seis", '7': "siete", '8': "ocho", '9': "nueve"}
    return "".join(digit_map[c] + " " if c.isdigit() else c for c in text).strip()

def map_voice_phrase_to_command(phrase):
    phrase = phrase.lower().strip()
    for key, command in FIXED_COMMANDS.items():
        if key in phrase:
            return command
    for trigger, template in VOICE_COMMAND_PATTERNS:
        if trigger in phrase:
            value = phrase.split(trigger, 1)[-1].strip()
            return template.format(value=value)
    return phrase

def main_loop(mode=None, lang=None):
    default_mode, default_lang, default_provider, default_input_method, default_whisper_path, default_model_path = load_settings()
    mode = mode or default_mode
    lang = lang or default_lang
    input_method = default_input_method

    ctx = ContextManager()
    ctx.set_mode(mode)

    tts_service = TTSService()
    speech_service = SpeechService(whisper_path=default_whisper_path, model_path=default_model_path)

    if input_method == "voice":
        load_dotenv()
        if platform.machine() == 'x86_64':
            ACCESS_KEY = os.getenv("ACCESS_KEY_UBUNTU")
            KEYWORD_PATH = os.getenv("KEYWORD_PATH_UBUNTU")
        elif platform.machine() == 'aarch64':
            ACCESS_KEY = os.getenv("ACCESS_KEY_RPI")
            KEYWORD_PATH = os.getenv("KEYWORD_PATH_RPI")
        else:
            raise RuntimeError(f"❌ Plataforma no soportada: {platform.machine()}")

        porcupine = pvporcupine.create(
            access_key=ACCESS_KEY,
            keyword_paths=[KEYWORD_PATH],
            sensitivities=[0.8]  # aquí aumentamos la sensibilidad
        )
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate, channels=1,
            format=pyaudio.paInt16, input=True,
            frames_per_buffer=porcupine.frame_length
        )
        print("🎤 NEXUS-X Core arrancado en modo voz (wakeword integrado).\n")
    else:
        print("⌨️ NEXUS-X Core arrancado en modo texto.\n")

    print(f"🛠️ Configuración cargada:")
    print(f"• Modo: {ctx.get_mode()}")
    print(f"• Idioma: {ctx.get_lang()}")
    print(f"• Método entrada: {input_method}")
    if input_method == "voice":
        print(f"• Whisper binario: {default_whisper_path}")
        print(f"• Modelo whisper: {default_model_path}")
    print()

    try:
        print("🎧 Esperando palabra de activación...")
        while True:
            if input_method == "voice":
                pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
                pcm = [int.from_bytes(pcm[i:i+2], 'little', signed=True) for i in range(0, len(pcm), 2)]
                result = porcupine.process(pcm)
                if result < 0:
                    continue

                print("✅ Activación detectada. Grabando...")
                frames = []
                record_seconds = 5
                for _ in range(0, int(porcupine.sample_rate / porcupine.frame_length * record_seconds)):
                    data = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
                    frames.append(data)

                raw_file = "recording_raw.wav"
                wf = wave.open(raw_file, 'wb')
                wf.setnchannels(1)
                wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
                wf.setframerate(porcupine.sample_rate)
                wf.writeframes(b''.join(frames))
                wf.close()

                print(f"🎧 Audio guardado en {raw_file}. Procesando...")
                user_input = speech_service.process_wav_file(raw_file).strip()
            else:
                user_input = input("You: ").strip()

            if user_input.lower() in ["exit", "quit"]:
                print("NEXUS-X Core: Goodbye.")
                break

            mapped_input = map_voice_phrase_to_command(user_input)

            if ctx.get_pending_action():
                result = handle_command(mapped_input, ctx=ctx)
                if result:
                    print("NEXUS-X Core:", result)
                    tts_service.speak(preprocess_response(result))
                continue

            if mapped_input.startswith("/"):
                result = handle_command(mapped_input, ctx=ctx)
                if mapped_input.startswith("/modo"):
                    save_mode_to_config(ctx.get_mode())
                if result:
                    print("NEXUS-X Core:", result)
                    tts_service.speak(preprocess_response(result))
            else:
                name = ctx.identity_memory.get("name")
                interests = ctx.identity_memory.get("interests")
                max_tokens = 80 if input_method == "voice" else 300
                result = get_response(
                    ctx.get_history(), mapped_input,
                    mode=ctx.get_mode(), lang=ctx.get_lang(),
                    max_tokens=max_tokens,
                    extra_context=f"El usuario se llama {name}." if name else "",
                    extra_interests=f"Tiene intereses en: {interests}." if interests else ""
                )

                ctx.add_message("user", mapped_input)
                ctx.add_message("assistant", result)

                print("NEXUS-X Core:", result)
                tts_service.speak(preprocess_response(result))

    except KeyboardInterrupt:
        print("🛑 Interrumpido por el usuario.")
    finally:
        if input_method == "voice":
            audio_stream.stop_stream()
            audio_stream.close()
            pa.terminate()
            porcupine.delete()
            print("✅ Recursos liberados correctamente.")

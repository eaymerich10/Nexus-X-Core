import os
import wave
import random
import platform
import pvporcupine
import pyaudio
import time

from dotenv import load_dotenv
from assistant.context import ContextManager
from assistant.commands.router import handle_command
from services.ai_provider import get_response
from assistant.utils.settings_manager import save_mode_to_config, load_settings
from services.speech.speech_service import SpeechService
from services.speech.tts_service import TTSService
from assistant.utils.constants import VOICE_COMMAND_PATTERNS, FIXED_COMMANDS, ACTIVATION_PHRASES

from gui.nexus_gui import update_gui_chat, update_gui_status, set_user_input_callback

def get_random_activation_phrase():
    return random.choice(ACTIVATION_PHRASES)

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

def stop_and_reopen_audio(pa, porcupine, audio_stream):
    audio_stream.stop_stream()
    audio_stream.close()
    print("Micrófono detenido temporalmente.")
    update_gui_status("Micrófono detenido")
    new_stream = pa.open(
        rate=porcupine.sample_rate, channels=1,
        format=pyaudio.paInt16, input=True,
        frames_per_buffer=porcupine.frame_length
    )
    print("🎙 Micrófono reabierto y listo para grabar.")
    update_gui_status("Micrófono reabierto")
    return new_stream

def main_loop(mode=None, lang=None):
    default_mode, default_lang, default_provider, default_input_method, default_whisper_path, default_model_path = load_settings()
    mode = mode or default_mode
    lang = lang or default_lang
    input_method = default_input_method

    ctx = ContextManager()
    ctx.set_mode(mode)

    tts_service = TTSService()
    speech_service = SpeechService(whisper_path=default_whisper_path, model_path=default_model_path)

    def handle_user_input(user_input):
        if not user_input:
            return

        update_gui_chat("Usuario", user_input)

        if user_input.lower() in ["exit", "quit"]:
            print("Saliendo de NEXUS-X Core.")
            update_gui_chat("NEXUS-X", "Saliendo de NEXUS-X Core.")
            update_gui_status("Detenido")
            os._exit(0)

        mapped_input = map_voice_phrase_to_command(user_input)

        if ctx.get_pending_action():
            result = handle_command(mapped_input, ctx=ctx)
            if result:
                update_gui_chat("NEXUS-X", result)
                if input_method == "voice":
                    update_gui_status("Hablando...")
                    tts_service.speak(preprocess_response(result))
                update_gui_status("Esperando...")
            return

        if mapped_input.startswith("/"):
            result = handle_command(mapped_input, ctx=ctx)
            if mapped_input.startswith("/modo"):
                save_mode_to_config(ctx.get_mode())
            if result:
                update_gui_chat("NEXUS-X", result)
                if input_method == "voice":
                    update_gui_status("Hablando...")
                    tts_service.speak(preprocess_response(result))
                update_gui_status("Esperando...")
        else:
            name = ctx.identity_memory.get("name")
            interests = ctx.identity_memory.get("interests")
            max_tokens = 80 if input_method == "voice" else 300
            update_gui_status("Pensando...")
            result = get_response(
                ctx.get_history(), mapped_input,
                mode=ctx.get_mode(), lang=ctx.get_lang(),
                max_tokens=max_tokens,
                extra_context=f"El usuario se llama {name}." if name else "",
                extra_interests=f"Tiene intereses en: {interests}." if interests else ""
            )
            update_gui_chat("NEXUS-X", result)
            if input_method == "voice":
                update_gui_status("Hablando...")
                tts_service.speak(preprocess_response(result))
            update_gui_status("Esperando...")

    # Vínculo para que GUI pueda mandar input
    set_user_input_callback(handle_user_input)

    if input_method == "voice":
        load_dotenv()
        if platform.machine() == 'x86_64':
            ACCESS_KEY = os.getenv("ACCESS_KEY_UBUNTU")
            KEYWORD_PATH = os.getenv("KEYWORD_PATH_UBUNTU")
        elif platform.machine() == 'aarch64':
            ACCESS_KEY = os.getenv("ACCESS_KEY_RPI")
            KEYWORD_PATH = os.getenv("KEYWORD_PATH_RPI")
        else:
            raise RuntimeError("Plataforma no soportada")

        porcupine = pvporcupine.create(
            access_key=ACCESS_KEY,
            keyword_paths=[KEYWORD_PATH],
            sensitivities=[0.7]
        )
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate, channels=1,
            format=pyaudio.paInt16, input=True,
            frames_per_buffer=porcupine.frame_length
        )
        print("NEXUS-X Core en modo voz.\n")
        update_gui_status("Modo voz activado")
    else:
        print("NEXUS-X Core en modo texto.\n")
        update_gui_status("Modo texto activado")

    try:
        if input_method == "voice":
            while True:
                pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
                pcm = [int.from_bytes(pcm[i:i + 2], 'little', signed=True) for i in range(0, len(pcm), 2)]
                result = porcupine.process(pcm)
                if result < 0:
                    continue

                activation_phrase = get_random_activation_phrase()
                print(f"Activación detectada. {activation_phrase}")
                update_gui_chat("NEXUS-X", activation_phrase)
                update_gui_status("Escuchando...")

                tts_service.speak(preprocess_response(activation_phrase))
                audio_stream = stop_and_reopen_audio(pa, porcupine, audio_stream)

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

                user_input = speech_service.process_wav_file(raw_file).strip()
                handle_user_input(user_input)
        else:
            while True:
                time.sleep(0.1)  # mantiene bucle para permitir input GUI

    except KeyboardInterrupt:
        print("Interrumpido por el usuario.")
        update_gui_chat("NEXUS-X", "Interrumpido por el usuario.")
        update_gui_status("Detenido")
    finally:
        if input_method == "voice":
            audio_stream.stop_stream()
            audio_stream.close()
            pa.terminate()
            porcupine.delete()
            print("Recursos liberados correctamente.")
            update_gui_status("Recursos liberados")

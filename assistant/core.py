from assistant.context import ContextManager
from assistant.commands.router import handle_command
from services.ai_provider import get_response
from assistant.utils.settings_manager import save_mode_to_config, save_lang_to_config, save_provider_to_config, load_settings
from services.speech.speech_service import SpeechService
from services.speech.tts_service import TTSService
from services.wakeword_service import WakeWordService  # 🔗 Importamos el módulo limpio (ya autoconfigurado)
import time

def preprocess_response(text):
    """Preprocesa la respuesta: reemplaza números por palabras dígito a dígito."""
    digit_map = {
        '0': "cero", '1': "uno", '2': "dos", '3': "tres", '4': "cuatro",
        '5': "cinco", '6': "seis", '7': "siete", '8': "ocho", '9': "nueve"
    }

    result = ""
    for char in text:
        if char.isdigit():
            result += digit_map[char] + " "
        else:
            result += char

    return result.strip()

def main_loop(mode=None, lang=None):
    default_mode, default_lang, default_provider, default_input_method, default_whisper_path, default_model_path = load_settings()
    mode = mode or default_mode
    lang = lang or default_lang
    input_method = default_input_method

    ctx = ContextManager()
    ctx.set_mode(mode)

    if input_method == "voice":
        speech_service = SpeechService(
            whisper_path=default_whisper_path,
            model_path=default_model_path
        )
        wakeword_service = WakeWordService()
        print("🎤 NEXUS-X Core arrancado en modo entrada de voz con activación por palabra clave.\n")
    else:
        print("⌨️ NEXUS-X Core arrancado en modo entrada de texto.\n")

    tts_service = TTSService()

    print(f"🛠️ Configuración cargada:")
    print(f"• Modo: {ctx.get_mode()}")
    print(f"• Idioma: {ctx.get_lang()}")
    print(f"• Método entrada: {input_method}")
    if input_method == "voice":
        print(f"• Whisper binario: {default_whisper_path}")
        print(f"• Modelo whisper: {default_model_path}")
    print()

    try:
        while True:
            if input_method == "voice":
                if not wakeword_service.wait_for_wakeword():
                    continue
                print("🎤 Esperando un momento antes de grabar...")
                time.sleep(0.5)  # o incluso 1 segundo
                print("🎤 Escuchando al usuario...")
                user_input = speech_service.listen_and_transcribe().strip()
            else:
                user_input = input("You: ").strip()

            if user_input.lower() in ["exit", "quit"]:
                print("NEXUS-X Core: Goodbye.")
                break

            lower_input = user_input.lower()
            if "me llamo" in lower_input:
                name = lower_input.split("me llamo")[-1].strip().split()[0]
                ctx.identity_memory.set("name", name)
                print(f"💾 [MEMORIA] Nombre guardado: {name}")

            if "mis intereses son" in lower_input:
                interests = lower_input.split("mis intereses son")[-1].strip()
                ctx.identity_memory.set("interests", interests)
                print(f"💾 [MEMORIA] Intereses guardados: {interests}")

            if "mi idioma es" in lower_input:
                language = lower_input.split("mi idioma es")[-1].strip().split()[0]
                ctx.identity_memory.set("preferred_language", language)
                print(f"💾 [MEMORIA] Idioma guardado: {language}")

            if ctx.get_pending_action():
                result = handle_command(user_input, ctx=ctx)
                if result:
                    print("NEXUS-X Core:", result)
                    processed_result = preprocess_response(result)
                    tts_service.speak(processed_result)
                continue

            if user_input.startswith("/"):
                result = handle_command(user_input, ctx=ctx)
                if user_input.startswith("/modo"):
                    save_mode_to_config(ctx.get_mode())
                if result:
                    print("NEXUS-X Core:", result)
                    processed_result = preprocess_response(result)
                    tts_service.speak(processed_result)
            else:
                name = ctx.identity_memory.get("name")
                interests = ctx.identity_memory.get("interests")
                max_tokens = 80 if input_method == "voice" else 300
                result = get_response(
                    ctx.get_history(),
                    user_input,
                    mode=ctx.get_mode(),
                    lang=ctx.get_lang(),
                    max_tokens=max_tokens,
                    extra_context=f"El usuario se llama {name}." if name else "",
                    extra_interests=f"Tiene intereses en: {interests}." if interests else ""
                )

                ctx.add_message("user", user_input)
                ctx.add_message("assistant", result)

                print("NEXUS-X Core:", result)
                processed_result = preprocess_response(result)
                tts_service.speak(processed_result)
    except KeyboardInterrupt:
        print("🛑 Interrumpido por el usuario.")
    finally:
        if input_method == "voice":
            wakeword_service.cleanup()

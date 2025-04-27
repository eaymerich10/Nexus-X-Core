from assistant.context import ContextManager
from assistant.commands.router import handle_command
from services.ai_provider import get_response
from assistant.utils.settings_manager import save_mode_to_config, save_lang_to_config, save_provider_to_config, load_settings
from services.speech.speech_service import SpeechService

def main_loop(mode=None, lang=None):
    default_mode, default_lang, default_provider, default_input_method = load_settings()
    mode = mode or default_mode
    lang = lang or default_lang
    input_method = default_input_method  # <-- Añadido

    ctx = ContextManager()
    ctx.set_mode(mode)

    if input_method == "voice":
        speech_service = SpeechService(
            whisper_path="/home/enric/Proyectos/whisper.cpp/whisper-cli",
            model_path="/home/enric/Proyectos/whisper.cpp/models/ggml-tiny.bin"
        )
        print("🎤 NEXUS-X Core arrancado en modo entrada de voz.\n")
    else:
        print("⌨️ NEXUS-X Core arrancado en modo entrada de texto.\n")

    print(f"🧠 Modo personalidad: {ctx.get_mode()}\n")

    while True:
        if input_method == "voice":
            print("🎤 Escuchando...")
            user_input = speech_service.listen_and_transcribe().strip()
        else:
            user_input = input("You: ").strip()

        print(f"[DEBUG] Entrada capturada: '{user_input}'")  # <-- Añadir aquí


        if user_input.lower() in ["exit", "quit"]:
            print("NEXUS-X Core: Goodbye.")
            break

        if ctx.get_pending_action():
            result = handle_command(user_input, ctx=ctx)
            if result:
                print("NEXUS-X Core:", result)
            continue

        if user_input.startswith("/"):
            result = handle_command(user_input, ctx=ctx)
            if user_input.startswith("/modo"):
                save_mode_to_config(ctx.get_mode())
        else:
            result = get_response(ctx.get_history(), user_input, mode=ctx.get_mode(), lang=ctx.get_lang())

            ctx.add_message("user", user_input)
            ctx.add_message("assistant", result)

        print("NEXUS-X Core:", result)

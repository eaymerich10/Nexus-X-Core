from assistant.context import ContextManager
from assistant.commands.router import handle_command
from services.ai_provider import get_response
from assistant.utils.settings_manager import save_mode_to_config, save_lang_to_config, save_provider_to_config, load_settings

def main_loop(mode=None, lang=None):
    """ 
    Main loop for the NEXUS-X Core assistant.
    This function initializes the context manager, sets the mode, and enters
    an interactive loop where it processes user input.
    """
    default_mode, default_lang, _ = load_settings()
    mode = mode or default_mode
    lang = lang or default_lang

    ctx = ContextManager()
    ctx.set_mode(mode)

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("NEXUS-X Core: Goodbye.")
            break

        # Manejar si hay una acción pendiente de confirmación
        if ctx.get_pending_action():
            result = handle_command(user_input, ctx=ctx)
            if result:
                print("NEXUS-X Core:", result)
            continue

        if user_input.startswith("/"):
            result = handle_command(user_input, ctx=ctx)
            # Si cambió el modo, actualizamos el archivo
            if user_input.startswith("/modo"):
                save_mode_to_config(ctx.get_mode())
        else:
            result = get_response(ctx.get_history(), user_input, mode=ctx.get_mode(), lang=ctx.get_lang())

            ctx.add_message("user", user_input)
            ctx.add_message("assistant", result)

        print("NEXUS-X Core:", result)

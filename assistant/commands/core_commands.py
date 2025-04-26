from core.texts import get_text
from config.personality import get_available_modes
from datetime import datetime
import platform
import subprocess
from core.logger import logger

VALID_LANGS = ["es", "en"]
VALID_PROVIDERS = ["openai", "local"]

def handle_core_command(cmd, args, ctx):
    """
    Handles core commands for the assistant, performing various actions based on the provided command.

    Args:
        cmd (str): The command to execute (e.g., "/hello", "/time", "/modo").
        args (list): A list of arguments associated with the command.
        ctx (object): The context object containing the current state (e.g., language, mode, provider).

    Returns:
        str: A response message based on the executed command, or None if the command is not recognized.

    Commands:
        - "/hello": Returns a greeting message in the current language.
        - "/time": Returns the current time in HH:MM:SS format.
        - "/modo": Changes or lists available modes. Requires an argument to set a new mode.
        - "/lang": Changes or lists available languages. Requires an argument to set a new language.
        - "/proveedor": Changes or lists available AI providers. Requires an argument to set a new provider.
        - "/estado": Returns the current state of the system, including mode, language, provider, temperature, and time.
        - "/reiniciar": Resets the context and logs a manual reset action.
        - "/modos": Lists all available modes.

    Notes:
        - The function uses helper functions like `get_text`, `get_available_modes`, and `get_temperature`.
        - Logging is performed for actions that modify the context (e.g., changing mode, language, or provider).
        - If `ctx` is None, default values are used for language and other context-dependent operations.
    """
    lang = ctx.get_lang() if ctx else "es"
    VALID_MODES = get_available_modes()

    if cmd == "/hello":
        return get_text("hello", lang)

    elif cmd == "/time":
        return f"{get_text('time', lang)}: {datetime.now().strftime('%H:%M:%S')}."

    elif cmd == "/modo":
        if not args:
            return f"{get_text('available_modes', lang)} {', '.join(VALID_MODES)}"
        new_mode = args[0].lower()
        if new_mode not in VALID_MODES:
            return f"{get_text('unknown_mode', lang)} '{new_mode}'. {get_text('available_modes', lang)} {', '.join(VALID_MODES)}"
        if ctx:
            ctx.set_mode(new_mode)
            logger.info(f"[config] Mode changed to '{new_mode}'")
            return f"{get_text('mode_changed', lang)} '{new_mode}'."

    elif cmd == "/lang":
        if not args:
            return f"{get_text('language_changed', lang)}: {', '.join(VALID_LANGS)}"
        new_lang = args[0].lower()
        if new_lang not in VALID_LANGS:
            return f"{get_text('unknown_language', lang)} '{new_lang}'. Available: {', '.join(VALID_LANGS)}"
        if ctx:
            ctx.set_lang(new_lang)
            logger.info(f"[config] Language changed to '{new_lang}'")
            return f"{get_text('language_changed', new_lang)} '{new_lang}'."

    elif cmd == "/proveedor":
        if not args:
            return f"{get_text('provider_changed', lang)}: {', '.join(VALID_PROVIDERS)}"
        provider = args[0].lower()
        if provider not in VALID_PROVIDERS:
            return f"{get_text('unknown_provider', lang)} '{provider}'. Available: {', '.join(VALID_PROVIDERS)}"
        if ctx:
            ctx.set_provider(provider)
            logger.info(f"[config] AI provider changed to '{provider}'")
            return f"{get_text('provider_changed', lang)} '{provider}'."

    elif cmd == "/estado":
        if ctx:
            temperature = get_temperature()
            logger.info("[system] Estado consultado por el usuario")
            return (
                f"🧠 Mode: {ctx.get_mode()}\n"
                f"🌍 Language: {ctx.get_lang()}\n"
                f"⚙️ Provider: {ctx.get_provider()}\n"
                f"🌡️ Temperature: {temperature}\n"
                f"🕓 Time: {datetime.now().strftime('%H:%M:%S')}"
            )

    elif cmd == "/reiniciar":
        if ctx:
            ctx.reset()
            logger.info("[system] NEXUS-X Core reiniciado manualmente por el usuario")
            return get_text("reiniciar", lang)

    elif cmd == "/modos":
        return f"🧠 {get_text('available_modes', lang)}\n" + "\n".join(f"• {m}" for m in VALID_MODES)

    return None  # No comando core

def get_temperature() -> str:
    try:
        if platform.system() == "Linux":
            temp_output = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8").strip()
            return temp_output.replace("temp=", "")
        else:
            return "N/A (Not on Raspberry Pi)"
    except Exception:
        return "Unavailable"

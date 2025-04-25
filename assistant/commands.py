import platform
import subprocess
from datetime import datetime
from core.logger import logger
from core.texts import get_text
from config.personality import get_available_modes

VALID_MODES = ["default", "programador", "filosofico"]
VALID_LANGS = ["es", "en"]
VALID_PROVIDERS = ["openai", "local"]
VALID_MODES = get_available_modes()


def handle_command(command: str, ctx=None) -> str:
    """
    Processes a command string and executes the corresponding action.

    Args:
        command (str): The command string to be processed.
        ctx (optional): Context object to modify state (mode, language, provider).

    Returns:
        str: Result of the executed command.
    """
    tokens = command.split()
    cmd = tokens[0]
    args = tokens[1:]
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
        return "Error: context not available."

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
        return "Error: context not available."

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
        return "Error: context not available."

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
        return "Error: context not available."

    elif cmd == "/reiniciar":
        if ctx:
            ctx.reset()
            logger.info("[system] NEXUS-X Core reiniciado manualmente por el usuario")
            return get_text("reiniciar", lang)
        return "Error: context not available."

    elif cmd == "/modos":
        modes = get_available_modes()
        return f"🧠 {get_text('available_modes', lang)}\n" + "\n".join(f"• {m}" for m in modes)

    else:
        return "Unknown command. Try /modo, /lang, /proveedor, /estado, /reiniciar, /modos, /time or /hello."

def get_temperature() -> str:
    try:
        if platform.system() == "Linux":
            temp_output = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8").strip()
            return temp_output.replace("temp=", "")
        else:
            return "N/A (Not on Raspberry Pi)"
    except Exception:
        return "Unavailable"
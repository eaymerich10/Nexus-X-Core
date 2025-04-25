import platform
import subprocess
from datetime import datetime
from core.logger import logger

VALID_MODES = ["default", "programador", "filosofico"]
VALID_LANGS = ["es", "en"]
VALID_PROVIDERS = ["openai", "local"]

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

    if cmd == "/time":
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}."

    elif cmd == "/hello":
        return "Hello! I'm NEXUS-X Core, your personal assistant."

    elif cmd == "/modo":
        if not args:
            return f"Please specify a mode. Available modes: {', '.join(VALID_MODES)}"
        new_mode = args[0].lower()
        if new_mode not in VALID_MODES:
            return f"Unknown mode '{new_mode}'. Available modes: {', '.join(VALID_MODES)}"
        if ctx:
            ctx.set_mode(new_mode)
            logger.info(f"[config] Mode changed to '{new_mode}'")
            return f"Mode changed to '{new_mode}'."
        return "Error: context not available."

    elif cmd == "/lang":
        if not args:
            return f"Please specify a language. Available: {', '.join(VALID_LANGS)}"
        new_lang = args[0].lower()
        if new_lang not in VALID_LANGS:
            return f"Unknown language '{new_lang}'. Available: {', '.join(VALID_LANGS)}"
        if ctx:
            ctx.set_lang(new_lang)
            logger.info(f"[config] Language changed to '{new_lang}'")
            return f"Language changed to '{new_lang}'."
        return "Error: context not available."

    elif cmd == "/proveedor":
        if not args:
            return f"Please specify a provider. Available: {', '.join(VALID_PROVIDERS)}"
        provider = args[0].lower()
        if provider not in VALID_PROVIDERS:
            return f"Unknown provider '{provider}'. Available: {', '.join(VALID_PROVIDERS)}"
        if ctx:
            ctx.set_provider(provider)
            logger.info(f"[config] AI provider changed to '{provider}'")
            return f"AI provider changed to '{provider}'."
        return "Error: context not available."

    elif cmd == "/estado":
        if ctx:
            temperature = get_temperature()
            logger.info("[system] Estado consulted by user")
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
            return "♻️ Reiniciando subsistemas de NEXUS-X Core... Estado y contexto restaurados."
        return "Error: context not available."

    else:
        return "Unknown command. Try /modo, /lang, /proveedor, /estado, /reiniciar, /time or /hello."

def get_temperature() -> str:
    try:
        if platform.system() == "Linux":
            temp_output = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8").strip()
            return temp_output.replace("temp=", "")
        else:
            return "N/A (Not on Raspberry Pi)"
    except Exception:
        return "Unavailable"
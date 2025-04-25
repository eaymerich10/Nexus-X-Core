from assistant.context import ContextManager
from assistant.commands import handle_command
from services.ai_provider import get_response
import configparser
import os

def load_settings():
    config = configparser.ConfigParser()
    config.read(".nexusrc")
    settings = config["settings"]
    return settings.get("mode", "default"), settings.get("lang", "es"), settings.get("ai_provider", "openai")

def save_mode_to_config(new_mode):
    config = configparser.ConfigParser()
    config.read(".nexusrc")
    if "settings" not in config:
        config["settings"] = {}
    config["settings"]["mode"] = new_mode
    with open(".nexusrc", "w") as configfile:
        config.write(configfile)

def save_lang_to_config(new_lang):
    config = configparser.ConfigParser()
    config.read(".nexusrc")
    if "settings" not in config:
        config["settings"] = {}
    config["settings"]["lang"] = new_lang
    with open(".nexusrc", "w") as configfile:
        config.write(configfile)

def save_provider_to_config(new_provider):
    config = configparser.ConfigParser()
    config.read(".nexusrc")
    if "settings" not in config:
        config["settings"] = {}
    config["settings"]["ai_provider"] = new_provider
    with open(".nexusrc", "w") as configfile:
        config.write(configfile)

def main_loop(mode=None, lang=None):
    """
    Main loop for the NEXUS-X Core assistant.

    This function initializes the context manager, sets the mode, and enters
    an interactive loop where it processes user input. The loop continues
    until the user types "exit" or "quit". It handles commands prefixed with
    "/" and generates responses for regular input.

    Args:
        mode (str, optional): The initial mode for the assistant. If not provided,
                              it defaults to the mode specified in the settings.
        lang (str, optional): The language for the assistant. If not provided,
                              it defaults to the language specified in the settings.

    Behavior:
        - Loads default settings for mode and language if not explicitly provided.
        - Listens for user input in a loop.
        - Processes commands starting with "/" using `handle_command`.
        - Updates the mode in the configuration file if the mode is changed.
        - Generates responses for regular input using `get_response`.
        - Maintains a conversation history using the `ContextManager`.

    Commands:
        - "/modo": Changes the mode and updates the configuration file.
        - "exit" or "quit": Exits the loop and terminates the program.

    Output:
        Prints the assistant's responses to the console.
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

        if user_input.startswith("/"):
            result = handle_command(user_input, ctx=ctx)
            # Si cambió el modo, actualizamos el archivo
            if user_input.startswith("/modo"):
                save_mode_to_config(ctx.get_mode())
        else:
            result = get_response(ctx.get_history(), user_input, mode=ctx.get_mode(), lang=lang)
            ctx.add_message("user", user_input)
            ctx.add_message("assistant", result)

        print("NEXUS-X Core:", result)

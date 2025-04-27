import configparser
import os

def load_settings():
    config = configparser.ConfigParser()
    config.read(".nexusrc")
    settings = config["settings"]
    return (
        settings.get("mode", "default"),
        settings.get("lang", "es"),
        settings.get("ai_provider", "openai"),
        settings.get("input_method", "text")  # <<--- Nuevo: por defecto texto
    )

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

def save_input_method_to_config(new_input_method):
    config = configparser.ConfigParser()
    config.read(".nexusrc")
    if "settings" not in config:
        config["settings"] = {}
    config["settings"]["input_method"] = new_input_method
    with open(".nexusrc", "w") as configfile:
        config.write(configfile)

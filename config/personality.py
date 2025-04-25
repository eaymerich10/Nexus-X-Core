import json
import os

def load_modes():
    modes_path = os.path.join(os.path.dirname(__file__), "modes.json")
    with open(modes_path, "r", encoding="utf-8") as f:
        return json.load(f)

modes_data = load_modes()

preferred_language_instructions = {
    "es": "Prefiere responder en español salvo que el usuario cambie claramente de idioma.",
    "en": "Prefer responding in English unless the user clearly switches to another language."
}

def get_personality_prompt(mode="default", lang="es") -> str:
    """
    Retrieves a personality prompt dynamically from modes.json
    """
    base_prompt = modes_data.get(mode, modes_data["default"]).get(lang, modes_data["default"]["es"])
    language_instruction = preferred_language_instructions.get(lang, preferred_language_instructions["es"])

    return f"{base_prompt}\n\n{language_instruction}"

def get_available_modes():
    """
    Returns a list of all available modes loaded from modes.json
    """
    return list(modes_data.keys())

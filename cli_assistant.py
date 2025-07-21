#!/usr/bin/env python3

import sys
import os
import random
from dotenv import load_dotenv

# Asegurar imports desde raíz del proyecto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Cargar entorno
load_dotenv()

# Importaciones del asistente
from assistant.context import ContextManager
from assistant.commands.router import handle_command
from services.ai_provider import get_response
from assistant.utils.settings_manager import load_settings
from assistant.utils.constants import VOICE_COMMAND_PATTERNS, FIXED_COMMANDS, ACTIVATION_PHRASES

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

def main():
    # Si no hay argumentos, muestra una frase de activación y uso
    if len(sys.argv) < 2:
        frase = random.choice(ACTIVATION_PHRASES)
        print(f"NEXUS-X: {frase}")
        print("\nUso: nexus \"tu pregunta o comando\"")
        print("Ejemplos:")
        print("  nexus \"cambiar modo a creativo\"")
        print("  nexus \"/estado\"")
        sys.exit(0)

    # Preparar entorno y contexto
    default_mode, default_lang, _, _, _, _ = load_settings()
    ctx = ContextManager()
    ctx.set_mode("terminal") # Modo terminal por defecto
    ctx.set_lang("es") # Idioma español por defecto

    entrada = " ".join(sys.argv[1:]).strip()
    mapped_input = map_voice_phrase_to_command(entrada)

    # Procesamiento
    if ctx.get_pending_action():
        respuesta = handle_command(mapped_input, ctx=ctx)
    elif mapped_input.startswith("/"):
        respuesta = handle_command(mapped_input, ctx=ctx)
    else:
        name = ctx.identity_memory.get("name")
        interests = ctx.identity_memory.get("interests")
        respuesta = get_response(
            ctx.get_history(), mapped_input,
            mode=ctx.get_mode(), lang=ctx.get_lang(),
            max_tokens=500,
            extra_context=f"El usuario se llama {name}." if name else "",
            extra_interests=f"Tiene intereses en: {interests}." if interests else ""
        )

    print(f"NEXUS: {respuesta}")

if __name__ == "__main__":
    main()

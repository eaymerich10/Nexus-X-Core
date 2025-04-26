TEXTS = {
    "hello": {
        "es": "¡Hola! Soy NEXUS-X Core, tu asistente personal.",
        "en": "Hello! I'm NEXUS-X Core, your personal assistant."
    },
    "time": {
        "es": "La hora actual es",
        "en": "The current time is"
    },
    "mode_changed": {
        "es": "Modo cambiado a",
        "en": "Mode changed to"
    },
    "unknown_mode": {
        "es": "Modo desconocido",
        "en": "Unknown mode"
    },
    "language_changed": {
        "es": "Idioma cambiado a",
        "en": "Language changed to"
    },
    "unknown_language": {
        "es": "Idioma desconocido",
        "en": "Unknown language"
    },
    "provider_changed": {
        "es": "Proveedor de IA cambiado a",
        "en": "AI provider changed to"
    },
    "unknown_provider": {
        "es": "Proveedor de IA desconocido",
        "en": "Unknown AI provider"
    },
    "estado": {
        "es": "Estado consultado por el usuario",
        "en": "Status consulted by user"
    },
    "reiniciar": {
        "es": "♻️ Reiniciando subsistemas de NEXUS-X Core... Estado y contexto restaurados.",
        "en": "♻️ Rebooting NEXUS-X Core subsystems... State and context restored."
    },
    "available_modes": {
        "es": "Modos disponibles:",
        "en": "Available modes:"
    },
    "confirm_delete": {
    "es": "¿Estás seguro de que quieres borrar '{reminder}'? (sí/no)",
    "en": "Are you sure you want to delete '{reminder}'? (yes/no)"
    },
    "confirm_yes_no": {
    "es": "Por favor responde 'si' o 'no'.",
    "en": "Please answer 'yes' or 'no'."
    },
    "deletion_cancelled": {
    "es": "❎ Eliminación cancelada.",
    "en": "❎ Deletion cancelled."
    }
}
def get_text(key, lang="es") -> str:
    return TEXTS.get(key, {}).get(lang, TEXTS.get(key, {}).get("es", ""))

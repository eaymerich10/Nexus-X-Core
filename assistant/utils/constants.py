VOICE_COMMAND_PATTERNS = [
    ("cambiar modo a", "/modo {value}"),
    ("mi idioma es", "/lang {value}"),
    ("cambiar proveedor a", "/proveedor {value}"),
    ("recuerda", "/recordar {value}"),
    ("cambiar entrada a", "/entrada {value}"),
]

FIXED_COMMANDS = {
    "dime el estado": "/estado",
    "muéstrame el estado": "/estado",
    "reinicia": "/reiniciar",
    "reiniciar asistente": "/reiniciar",
    "modos disponibles": "/modos",
    "lista de modos": "/modos",
}

ACTIVATION_PHRASES = [
    "Activado",
]
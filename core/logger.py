import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "nexus.log")

# Crear el directorio de logs si no existe
os.makedirs(LOG_DIR, exist_ok=True)

# Configurar logger
logger = logging.getLogger("nexus")
logger.setLevel(logging.INFO)

# Evitar múltiples handlers si el módulo se importa más de una vez
if not logger.handlers:
    handler = RotatingFileHandler(LOG_FILE, maxBytes=200 * 1024, backupCount=3)
    formatter = logging.Formatter('%(asctime)s — %(levelname)s — %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Log de arranque (se puede comentar si lo haces desde core.py)
logger.info("[system] NEXUS-X Core logger initialized")

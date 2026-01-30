"""
Sistema de logging para el Chatbot Maskotas.
"""

import logging
import logging.handlers
from pathlib import Path
from config import LOGGING_CONFIG


def setup_logging():
    """Configura el sistema de logging del proyecto."""
    log_dir = Path(LOGGING_CONFIG["log_file"]).parent
    log_dir.mkdir(exist_ok=True)
    
    # Crear logger principal
    logger = logging.getLogger("maskotas_chatbot")
    logger.setLevel(LOGGING_CONFIG["level"])
    
    # Formato
    formatter = logging.Formatter(LOGGING_CONFIG["format"])
    
    # Handler para archivo
    file_handler = logging.handlers.RotatingFileHandler(
        LOGGING_CONFIG["log_file"],
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(module_name):
    """Obtiene un logger para un módulo específico."""
    return logging.getLogger(f"maskotas_chatbot.{module_name}")

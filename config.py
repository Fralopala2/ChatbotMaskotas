"""
Configuración centralizada para el Chatbot Maskotas.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env si existe
load_dotenv()

# Rutas
PROJECT_ROOT = Path(__file__).parent
SERVICE_ACCOUNT_KEY_PATH = PROJECT_ROOT / "chatbot-maskotas-72d44d6d1b83.json"
KNOWLEDGE_BASE_FILE = PROJECT_ROOT / "maskotas_knowledge_base.json"

# Firebase/Firestore
FIREBASE_CREDENTIALS_PATH = str(SERVICE_ACCOUNT_KEY_PATH)

# Google Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
AI_MODEL = "models/gemini-1.5-flash"

# Firestore Collections
FIRESTORE_COLLECTIONS = {
    "general_info": "informacion_general_clinica",
    "services": "servicios_veterinaria"
}

# Configuración del Chatbot
CHATBOT_CONFIG = {
    "name": "Maskotas Bot",
    "clinic_name": "Clínica Veterinaria Maskotas",
    "system_prompt": """Eres un asistente de la clínica veterinaria Maskotas. Tu objetivo es proporcionar 
información precisa y útil sobre nuestros servicios, horarios y cualquier otra consulta general. 
Prioriza la información proporcionada de nuestra base de datos. Si no encuentras la respuesta 
exacta en la base de datos, indica amablemente que no dispones de esa información en este 
momento o que necesitas más detalles. Sé amable, profesional y conciso."""
}

# Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "log_file": PROJECT_ROOT / "logs" / "chatbot.log"
}

def validate_config():
    """Valida que las configuraciones necesarias estén disponibles."""
    errors = []
    
    if not GOOGLE_API_KEY:
        errors.append("GOOGLE_API_KEY no está configurada en variables de entorno")
    
    if not SERVICE_ACCOUNT_KEY_PATH.exists():
        errors.append(f"Archivo de credenciales Firebase no encontrado en: {SERVICE_ACCOUNT_KEY_PATH}")
    
    if errors:
        raise RuntimeError("Errores de configuración:\n" + "\n".join(errors))

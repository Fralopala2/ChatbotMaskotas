"""
Test unitario básico para validar la estructura del proyecto.
Ejecuta con: python -m pytest test_chatbot.py -v
"""

import pytest
import json
from pathlib import Path
from config import (
    GOOGLE_API_KEY, 
    SERVICE_ACCOUNT_KEY_PATH,
    FIRESTORE_COLLECTIONS,
    CHATBOT_CONFIG
)


class TestConfiguration:
    """Tests para validar la configuración."""
    
    def test_google_api_key_configured(self):
        """Verifica que GOOGLE_API_KEY está configurada."""
        assert GOOGLE_API_KEY, "GOOGLE_API_KEY debe estar configurada en variables de entorno"
    
    def test_firebase_credentials_exist(self):
        """Verifica que el archivo de credenciales existe."""
        assert SERVICE_ACCOUNT_KEY_PATH.exists(), f"Archivo de credenciales no encontrado: {SERVICE_ACCOUNT_KEY_PATH}"
    
    def test_firestore_collections_configured(self):
        """Verifica que las colecciones están configuradas."""
        assert "general_info" in FIRESTORE_COLLECTIONS
        assert "services" in FIRESTORE_COLLECTIONS
        assert len(FIRESTORE_COLLECTIONS) > 0
    
    def test_chatbot_config_valid(self):
        """Verifica que la configuración del chatbot es válida."""
        assert "name" in CHATBOT_CONFIG
        assert "clinic_name" in CHATBOT_CONFIG
        assert "system_prompt" in CHATBOT_CONFIG
        assert len(CHATBOT_CONFIG["name"]) > 0


class TestDatabaseModule:
    """Tests para el módulo de base de datos."""
    
    def test_firestore_db_singleton(self):
        """Verifica que Firestore usa patrón Singleton."""
        from database import firestore_db, FirestoreDB
        
        db1 = FirestoreDB()
        db2 = FirestoreDB()
        
        assert db1 is db2, "FirestoreDB debería ser Singleton"


class TestAIModel:
    """Tests para el módulo de IA."""
    
    def test_gemini_ai_initialization(self):
        """Verifica que Gemini AI se inicializa correctamente."""
        from ai_model import gemini_ai
        
        assert gemini_ai.model_name is not None
        assert "gemini" in gemini_ai.model_name.lower()
    
    def test_input_validation_empty(self):
        """Verifica que entrada vacía es rechazada."""
        from ai_model import gemini_ai
        
        assert gemini_ai.validate_input("") is False
        assert gemini_ai.validate_input("   ") is False
    
    def test_input_validation_long(self):
        """Verifica que entrada muy larga es rechazada."""
        from ai_model import gemini_ai
        
        long_text = "a" * 2000
        assert gemini_ai.validate_input(long_text) is False
    
    def test_input_validation_valid(self):
        """Verifica que entrada válida es aceptada."""
        from ai_model import gemini_ai
        
        assert gemini_ai.validate_input("¿Cuál es tu horario?") is True


class TestChatbot:
    """Tests para el módulo principal del chatbot."""
    
    def test_chatbot_initialization(self):
        """Verifica que el chatbot se inicializa correctamente."""
        from chatbot import MaskotasChatbot
        
        chatbot = MaskotasChatbot()
        
        assert chatbot.name == CHATBOT_CONFIG["name"]
        assert chatbot.clinic_name == CHATBOT_CONFIG["clinic_name"]
        assert len(chatbot.system_prompt) > 0
    
    def test_context_building_empty(self):
        """Verifica que context vacío devuelve string vacío."""
        from chatbot import MaskotasChatbot
        
        chatbot = MaskotasChatbot()
        context = chatbot._build_context({"general_info": [], "services": []})
        
        assert context == ""


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

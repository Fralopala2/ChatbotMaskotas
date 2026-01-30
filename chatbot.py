"""
Chatbot principal para la Clínica Veterinaria Maskotas.
Orquesta las funciones de Firestore y Gemini AI.
"""

import json
from typing import Dict, List, Any
from database import firestore_db
from ai_model import gemini_ai
from config import CHATBOT_CONFIG, FIRESTORE_COLLECTIONS
from logger import get_logger

logger = get_logger("chatbot")


class MaskotasChatbot:
    """Chatbot principal que combina Firestore y Gemini AI."""
    
    def __init__(self):
        """Inicializa el chatbot."""
        self.name = CHATBOT_CONFIG["name"]
        self.clinic_name = CHATBOT_CONFIG["clinic_name"]
        self.system_prompt = CHATBOT_CONFIG["system_prompt"]
        logger.info(f"Chatbot '{self.name}' inicializado")
    
    def _search_knowledge_base(self, query: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Busca información relevante en la base de conocimientos.
        
        Args:
            query: Consulta del usuario
            
        Returns:
            Diccionario con resultados de búsqueda
        """
        logger.debug(f"Buscando en base de conocimientos: '{query}'")
        results = firestore_db.search_all_collections(query)
        
        total_results = sum(len(v) for v in results.values())
        logger.debug(f"Encontrados {total_results} resultado(s)")
        
        return results
    
    def _build_context(self, search_results: Dict[str, List[Dict[str, Any]]]) -> str:
        """
        Construye el contexto para el prompt del IA.
        
        Args:
            search_results: Resultados de búsqueda
            
        Returns:
            String con el contexto formateado
        """
        if not any(search_results.values()):
            return ""
        
        context = f"\n\nInformación relevante de {self.clinic_name}:\n"
        
        # Información general
        if search_results.get("general_info"):
            context += "\n📋 Información General:\n"
            for item in search_results["general_info"]:
                context += f"- {json.dumps(item, ensure_ascii=False, indent=2)}\n"
        
        # Servicios
        if search_results.get("services"):
            context += "\n🏥 Servicios:\n"
            for item in search_results["services"]:
                context += f"- {json.dumps(item, ensure_ascii=False, indent=2)}\n"
        
        return context.strip()
    
    def get_response(self, user_query: str) -> str:
        """
        Obtiene una respuesta del chatbot para la consulta del usuario.
        
        Args:
            user_query: Pregunta del usuario
            
        Returns:
            Respuesta del chatbot
        """
        # Validar entrada
        if not gemini_ai.validate_input(user_query):
            logger.warning("Entrada inválida del usuario")
            return "Por favor, escribe una pregunta válida."
        
        logger.info(f"Procesando consulta: '{user_query}'")
        
        # Buscar en base de datos
        search_results = self._search_knowledge_base(user_query)
        
        # Construir contexto
        context = self._build_context(search_results)
        
        # Construir prompt completo
        full_prompt = f"""{self.system_prompt}

{context}

Pregunta del usuario: {user_query}

Respuesta de {self.name}:"""
        
        # Obtener respuesta de IA
        response = gemini_ai.generate_response(full_prompt.strip())
        
        logger.info(f"Respuesta generada (longitud: {len(response)} caracteres)")
        
        return response
    
    def chat_interactive(self):
        """Inicia el chatbot en modo interactivo."""
        print(f"\n{'='*60}")
        print(f"🐾 Bienvenido al {self.name} 🐾")
        print(f"{'='*60}")
        print(f"Soy el asistente virtual de {self.clinic_name}")
        print("Escribe 'salir' para terminar la conversación.")
        print(f"{'='*60}\n")
        
        while True:
            try:
                user_input = input("Tu pregunta: ").strip()
                
                if user_input.lower() in ('salir', 'exit', 'quit'):
                    print(f"\n¡Gracias por usar {self.name}! ¡Hasta pronto! 🐾")
                    break
                
                if not user_input:
                    print("Por favor, escribe una pregunta.\n")
                    continue
                
                response = self.get_response(user_input)
                print(f"\n{self.name}: {response}\n")
                
            except KeyboardInterrupt:
                print(f"\n\n¡Hasta pronto! 🐾")
                break
            except Exception as e:
                logger.error(f"Error inesperado: {e}")
                print(f"Ocurrió un error. Por favor, intenta de nuevo.\n")


if __name__ == "__main__":
    try:
        chatbot = MaskotasChatbot()
        chatbot.chat_interactive()
    except Exception as e:
        logger.critical(f"Error crítico al inicializar chatbot: {e}")
        print(f"Error: No se pudo inicializar el chatbot. Revisa la configuración.")

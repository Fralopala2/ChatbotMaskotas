"""
Módulo para interactuar con Google Gemini AI.
Encapsula toda la lógica de IA generativa.
"""

from typing import Optional
import google.generativeai as genai
from config import GOOGLE_API_KEY, AI_MODEL
from logger import get_logger

logger = get_logger("ai_model")


class GeminiAI:
    """Gestor de interacciones con Google Gemini."""
    
    def __init__(self):
        """Inicializa la configuración de Gemini AI."""
        if not GOOGLE_API_KEY:
            error_msg = "GOOGLE_API_KEY no está configurada en variables de entorno"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model_name = AI_MODEL
        logger.info(f"Gemini AI inicializado con modelo: {self.model_name}")
    
    def generate_response(self, prompt: str) -> str:
        """
        Genera una respuesta usando Gemini AI.
        
        Args:
            prompt: El prompt para el modelo
            
        Returns:
            Respuesta del modelo como string
            
        Raises:
            Exception: Si hay error en la generación
        """
        try:
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            
            if response.candidates and len(response.candidates) > 0:
                generated_text = "".join(
                    part.text for part in response.candidates[0].content.parts
                )
                logger.debug("Respuesta generada correctamente")
                return generated_text
            
            # Respuesta bloqueada por políticas
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                block_reason = response.prompt_feedback.block_reason
                logger.warning(f"Respuesta bloqueada: {block_reason}")
                return f"No puedo generar una respuesta a esa solicitud ({block_reason})."
            
            logger.warning("No se generó contenido en la respuesta")
            return "No pude generar una respuesta válida. Intenta de nuevo."
            
        except Exception as e:
            logger.error(f"Error al generar respuesta de IA: {e}")
            return f"Error al procesar tu pregunta: {str(e)}"
    
    def validate_input(self, text: str, max_length: int = 1000) -> bool:
        """
        Valida la entrada del usuario.
        
        Args:
            text: Texto a validar
            max_length: Longitud máxima permitida
            
        Returns:
            True si es válida, False en caso contrario
        """
        if not text or not text.strip():
            return False
        
        if len(text) > max_length:
            logger.warning(f"Entrada excede longitud máxima: {len(text)} > {max_length}")
            return False
        
        return True


# Instancia global
gemini_ai = GeminiAI()

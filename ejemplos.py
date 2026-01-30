"""
Ejemplos de uso del Chatbot Maskotas v2.0

Este archivo contiene ejemplos prácticos de cómo usar los módulos
de forma programática, sin ejecutar la interfaz interactiva.
"""

# ============================================================
# EJEMPLO 1: Usar el chatbot en modo programático
# ============================================================

from chatbot import MaskotasChatbot

# Crear instancia del chatbot
chatbot = MaskotasChatbot()

# Obtener respuestas
respuesta = chatbot.get_response("¿Cuál es tu horario de atención?")
print(f"Bot: {respuesta}")

respuesta = chatbot.get_response("¿Qué servicios ofrecen?")
print(f"Bot: {respuesta}")


# ============================================================
# EJEMPLO 2: Acceder directamente a la base de datos
# ============================================================

from database import firestore_db

# Buscar en una colección específica
resultados = firestore_db.search_collection("servicios_veterinaria", "cirugía")
print(f"Servicios encontrados: {len(resultados)}")
for resultado in resultados:
    print(f"  - {resultado}")

# Buscar en todas las colecciones
todos_los_resultados = firestore_db.search_all_collections("horario")
print(f"Información sobre horario:")
for coleccion, items in todos_los_resultados.items():
    print(f"  {coleccion}: {len(items)} resultado(s)")


# ============================================================
# EJEMPLO 3: Usar el modelo de IA directamente
# ============================================================

from ai_model import gemini_ai

# Validar entrada
entrada_usuario = "¿Hola, cómo estás?"
if gemini_ai.validate_input(entrada_usuario):
    print("Entrada válida")
    
    # Generar respuesta personalizada
    prompt_personalizado = """Eres un veterinario experto.
    Pregunta del cliente: ¿Cuál es el mejor alimento para gatos?
    Respuesta:"""
    
    respuesta = gemini_ai.generate_response(prompt_personalizado)
    print(f"Respuesta del veterinario: {respuesta}")
else:
    print("Entrada inválida")


# ============================================================
# EJEMPLO 4: Subir datos nuevos a Firestore
# ============================================================

import json
from database import firestore_db

# Crear datos nuevos
nuevos_datos = {
    "servicios_veterinaria": [
        {
            "id": "servicio_5",
            "nombre": "Baño y Grooming",
            "descripcion": "Baño, secado y arreglo de mascotas",
            "precio": "$50"
        }
    ],
    "informacion_general_clinica": [
        {
            "tema": "emergencia",
            "contenido": "Atendemos emergencias 24/7 en nuestras instalaciones"
        }
    ]
}

# Subir datos
exito = firestore_db.upload_data(nuevos_datos)
if exito:
    print("Datos subidos correctamente")
else:
    print("Error al subir datos")


# ============================================================
# EJEMPLO 5: Usar logging en tu propio código
# ============================================================

from logger import get_logger

# Crear logger para tu módulo
logger = get_logger("mi_modulo_personalizado")

# Usar diferentes niveles
logger.debug("Información de debug")
logger.info("Operación completada")
logger.warning("Advertencia importante")
logger.error("Algo salió mal")

# Los logs se guardan en logs/chatbot.log


# ============================================================
# EJEMPLO 6: Crear un chatbot personalizado
# ============================================================

from chatbot import MaskotasChatbot
from database import firestore_db
from ai_model import gemini_ai
import json

class ChatbotPersonalizado(MaskotasChatbot):
    """Extensión del chatbot con funcionalidad personalizada."""
    
    def obtener_estadisticas(self):
        """Método personalizado para obtener estadísticas."""
        servicios = firestore_db.search_collection("servicios_veterinaria", "")
        info_general = firestore_db.search_collection("informacion_general_clinica", "")
        
        return {
            "total_servicios": len(servicios),
            "total_informacion": len(info_general)
        }
    
    def respuesta_especial(self, query):
        """Método personalizado para consultas especiales."""
        if "estadísticas" in query.lower():
            stats = self.obtener_estadisticas()
            return f"Tenemos {stats['total_servicios']} servicios y {stats['total_informacion']} datos de información."
        else:
            return self.get_response(query)

# Usar el chatbot personalizado
bot_personalizado = ChatbotPersonalizado()
respuesta = bot_personalizado.respuesta_especial("¿Cuáles son las estadísticas?")
print(f"Respuesta especial: {respuesta}")


# ============================================================
# EJEMPLO 7: Procesar múltiples preguntas
# ============================================================

preguntas = [
    "¿Dónde están ubicados?",
    "¿Cuál es su teléfono?",
    "¿Qué servicios ofrecen?",
    "¿Cuál es el horario?",
    "¿Cuánto cuesta una consulta?"
]

chatbot = MaskotasChatbot()

print("Procesando múltiples preguntas...")
for pregunta in preguntas:
    try:
        respuesta = chatbot.get_response(pregunta)
        print(f"\nP: {pregunta}")
        print(f"R: {respuesta[:100]}...")  # Primeros 100 caracteres
    except Exception as e:
        print(f"Error procesando '{pregunta}': {e}")


# ============================================================
# EJEMPLO 8: Análisis de entrada antes de procesar
# ============================================================

from logger import get_logger

logger = get_logger("analisis_entrada")

def procesar_con_analisis(chatbot, query):
    """Procesa una consulta con análisis previo."""
    
    # Validar
    if not gemini_ai.validate_input(query):
        logger.warning(f"Entrada inválida: {query}")
        return "Por favor, proporciona una pregunta válida"
    
    # Analizar longitud
    longitud = len(query)
    logger.info(f"Procesando consulta de {longitud} caracteres")
    
    # Buscar palabras clave
    palabras_clave = ["horario", "precio", "ubicación", "servicio"]
    palabras_encontradas = [p for p in palabras_clave if p in query.lower()]
    
    if palabras_encontradas:
        logger.debug(f"Palabras clave encontradas: {palabras_encontradas}")
    
    # Procesar
    respuesta = chatbot.get_response(query)
    logger.info(f"Respuesta generada ({len(respuesta)} caracteres)")
    
    return respuesta

# Usar la función
chatbot = MaskotasChatbot()
respuesta = procesar_con_analisis(chatbot, "¿Cuál es el horario y precio de consulta?")
print(f"Respuesta: {respuesta}")


# ============================================================
# EJEMPLO 9: Integración con bases de datos externas
# ============================================================

# Este ejemplo muestra cómo podrías agregar datos de otra fuente

def importar_datos_externos(archivo_csv):
    """
    Ejemplo: importar datos de un CSV y subirlos a Firestore.
    """
    import csv
    
    servicios_importados = []
    
    # Leer CSV (ejemplo simplificado)
    with open(archivo_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            servicios_importados.append({
                "id": row['id'],
                "nombre": row['nombre'],
                "descripcion": row['descripcion'],
                "precio": row['precio']
            })
    
    # Subir a Firestore
    datos = {
        "servicios_veterinaria": servicios_importados
    }
    
    return firestore_db.upload_data(datos)


# ============================================================
# EJEMPLO 10: Monitoreo y debugging
# ============================================================

from logger import setup_logging
import logging

# Configurar logging en DEBUG para ver todo
setup_logging()
logger = get_logger("debug")
logger.setLevel(logging.DEBUG)

logger.debug("Iniciando chatbot en modo DEBUG")

chatbot = MaskotasChatbot()

logger.debug("Chatbot inicializado")
logger.debug(f"Nombre: {chatbot.name}")
logger.debug(f"Clínica: {chatbot.clinic_name}")

respuesta = chatbot.get_response("Test")
logger.debug(f"Respuesta recibida: {len(respuesta)} caracteres")

print("\nVerifica logs/chatbot.log para ver los logs detallados")


# ============================================================
# Resumen de Ejemplos
# ============================================================

"""
Este archivo demuestra:

1. ✅ Uso básico del chatbot
2. ✅ Acceso directo a base de datos
3. ✅ Uso del modelo de IA
4. ✅ Subir datos a Firestore
5. ✅ Sistema de logging
6. ✅ Extensión del chatbot
7. ✅ Procesamiento por lotes
8. ✅ Análisis de entrada
9. ✅ Integración con datos externos
10. ✅ Debugging y monitoreo

Puedes ejecutar este archivo completo o copiar fragmentos
específicos a tu código.

Para ejecutar este archivo:
    python ejemplos.py
"""


if __name__ == "__main__":
    print("Este archivo contiene ejemplos de uso.")
    print("Copia los ejemplos que necesites a tu código.")
    print("\nEjemplos incluidos:")
    print("1. Uso del chatbot interactivo")
    print("2. Acceso a base de datos")
    print("3. Uso del modelo de IA")
    print("4. Subir datos")
    print("5. Logging")
    print("6. Chatbot personalizado")
    print("7. Procesamiento múltiple")
    print("8. Análisis de entrada")
    print("9. Importación de datos")
    print("10. Debugging")

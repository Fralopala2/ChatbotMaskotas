import firebase_admin
from firebase_admin import credentials, firestore
import google.generativeai as genai
import os
import json

# --- Configuración de Firestore ---
# ¡IMPORTANTE! Reemplaza esto con la ruta CORRECTA a tu archivo JSON de clave de servicio de Firebase.
# Por ejemplo: "./nombre-de-tu-clave-de-firebase.json"
SERVICE_ACCOUNT_KEY_PATH = "chatbot-maskotas-72d44d6d1b83.json" # <--- ¡ACTUALIZA ESTA RUTA!

try:
    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firestore inicializado correctamente.")
except Exception as e:
    print(f"Error al inicializar Firebase Admin: {e}")
    print("Asegúrate de que la ruta a tu archivo de credenciales de Firestore es correcta y que tienes conexión a internet.")
    exit()

# --- Configuración de Gemini AI ---
# Asegúrate de que esta variable de entorno esté configurada antes de ejecutar el script.
# Ejemplo (CMD): set GOOGLE_API_KEY="TU_CLAVE_GEMINI"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("ERROR: La variable de entorno 'GOOGLE_API_KEY' no está configurada.")
    print("Por favor, configúrala antes de ejecutar el script.")
    print("Para obtener tu clave: https://aistudio.google.com/app/apikey")
    exit()

genai.configure(api_key=GOOGLE_API_KEY)
# Usa el modelo que te funcionó: "models/gemini-1.5-flash" es una buena opción.
AI_MODEL = "models/gemini-1.5-flash"

print(f"Clave de API de Gemini leída (primeros 5): {GOOGLE_API_KEY[:5]}*****")
print(f"Usando el modelo AI: {AI_MODEL}")

# --- Funciones de Firestore para buscar datos ---
def get_firestore_data(collection_name, query_text):
    """
    Busca datos relevantes en una colección de Firestore basados en palabras clave simples.
    NOTA: Para un chatbot robusto, esta búsqueda debería ser más avanzada (ej. embeddings).
    """
    results = []
    docs = db.collection(collection_name).stream()
    for doc in docs:
        doc_data = doc.to_dict()
        # Convertimos todo el documento a una cadena para buscar palabras clave
        doc_string = json.dumps(doc_data, ensure_ascii=False).lower()
        if query_text.lower() in doc_string:
            results.append(doc_data)
    return results

# --- Función de IA Generativa ---
def get_ai_response(prompt):
    """
    Obtiene una respuesta del modelo de Gemini AI.
    """
    try:
        model = genai.GenerativeModel(AI_MODEL)
        response = model.generate_content(prompt)

        if response.candidates:
            generated_text = "".join(part.text for part in response.candidates[0].content.parts)
            return generated_text
        else:
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                return f"Respuesta bloqueada: {response.prompt_feedback.block_reason}"
            return "No se pudo generar una respuesta de IA."
    except Exception as e:
        return f"Error al generar respuesta de IA: {e}"

# --- Lógica principal del Chatbot ---
def chatbot_response(user_query):
    # 1. Buscar información relevante en Firestore
    firestore_info = []

    # Buscar en 'informacion_general_clinica'
    general_info = get_firestore_data("informacion_general_clinica", user_query)
    if general_info:
        firestore_info.extend(general_info)

    # Buscar en 'servicios_veterinaria'
    service_info = get_firestore_data("servicios_veterinaria", user_query)
    if service_info:
        firestore_info.extend(service_info)

    # --- DEBUGGING: Imprime la información recuperada de Firestore ---
    print(f"\n--- Información de Firestore recuperada para '{user_query}':")
    if firestore_info:
        for item in firestore_info:
            print(json.dumps(item, ensure_ascii=False, indent=2))
    else:
        print("Ninguna información relevante encontrada en Firestore.")
    print("---\n")
    # ---------------------------------------------------------------

    # 2. Construir el prompt para la IA
    # Rol del sistema
    system_prompt = "Eres un asistente de la clínica veterinaria Maskotas. Tu objetivo es proporcionar información precisa y útil sobre nuestros servicios, horarios y cualquier otra consulta general. Prioriza la información proporcionada de nuestra base de datos. Si no encuentras la respuesta exacta en la base de datos, indica amablemente que no dispones de esa información en este momento o que necesitas más detalles."

    context_str = ""
    if firestore_info:
        context_str = "\n\nInformación de la base de datos de Maskotas:\n"
        for item in firestore_info:
            context_str += "- " + json.dumps(item, ensure_ascii=False) + "\n"

    # Combinar el prompt del sistema, el contexto de Firestore y la pregunta del usuario
    # Formato de chat recomendado para modelos de instrucción como Gemini-1.5-flash
    full_prompt = f"""
    {system_prompt}

    {context_str}

    Pregunta del usuario: {user_query}

    Respuesta de Maskotas Bot:
    """
    # Limpiamos espacios extra
    full_prompt = full_prompt.strip()

    # 3. Obtener respuesta de la IA
    ai_response = get_ai_response(full_prompt)
    return ai_response

if __name__ == "__main__":
    print("\n¡Hola! Soy el Chatbot de la Clínica Veterinaria Maskotas.")
    print("Escribe 'salir' para terminar.")

    while True:
        user_input = input("\nTu pregunta: ")
        if user_input.lower() == 'salir':
            print("¡Hasta pronto!")
            break

        response = chatbot_response(user_input)
        print(f"Maskotas Bot: {response}")
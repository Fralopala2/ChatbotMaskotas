import google.generativeai as genai
import os

# Tu clave de API de Google Gemini se obtiene de la variable de entorno 'GOOGLE_API_KEY'.
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("ERROR: La variable de entorno 'GOOGLE_API_KEY' no está configurada.")
    print("Por favor, configúrala antes de ejecutar el script.")
    print("Para obtener tu clave: https://aistudio.google.com/app/apikey")
    exit()

# Configura la API de Google Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# *** ¡CAMBIADO A UN MODELO VÁLIDO ENCONTRADO EN LA LISTA! ***
MODEL = "models/gemini-1.5-flash" # Puedes probar con "models/gemini-1.5-flash-latest" si lo prefieres

def list_gemini_models():
    """Lista modelos disponibles y sus métodos soportados."""
    print("\nListando modelos disponibles y sus capacidades:")
    for m in genai.list_models():
        print(f"- {m.name} (Soporta: {m.supported_generation_methods})")

def query_gemini_model(prompt_text):
    """
    Envía una consulta al modelo de Google Gemini y devuelve la respuesta generada.
    """
    try:
        model = genai.GenerativeModel(MODEL) # Usa la variable MODEL definida arriba
        response = model.generate_content(prompt_text)

        if response.candidates:
            generated_text = "".join(part.text for part in response.candidates[0].content.parts)
            return generated_text
        else:
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                return f"Respuesta bloqueada: {response.prompt_feedback.block_reason}"
            return "No se pudo generar una respuesta."

    except Exception as e:
        return f"Error al conectar con la API de Gemini: {e}"

if __name__ == "__main__":
    # --- Debugging print para la clave (primeros 5 caracteres) ---
    print(f"Clave de API de Gemini leída (primeros 5): {GOOGLE_API_KEY[:5]}*****")

    # Paso 1: Listar los modelos disponibles (mantener para referencia si es necesario)
    # list_gemini_models() # Comentado para no listar cada vez

    # Ahora sí, la sección de generación de respuesta
    print(f"Usando el modelo: {MODEL}")
    prompt_query = "Eres un asistente de la clínica veterinaria Maskotas. ¿Cuál es el horario de atención de la clínica?"
    print(f"\nGenerando respuesta para: '{prompt_query}'")

    response_text = query_gemini_model(prompt_query)
    print(f"Respuesta del modelo: {response_text.strip()}")
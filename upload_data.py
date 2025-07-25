import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import os

# Ruta a tu archivo de clave de servicio descargado (¡cambia esto!)
# Asegúrate de que esta ruta es CORRECTA.
# Si el archivo JSON de tu clave está en la misma carpeta que este script,
# solo necesitas poner el nombre del archivo, por ejemplo: "nombre-de-tu-clave.json"
SERVICE_ACCOUNT_KEY_PATH ="chatbot-maskotas-72d44d6d1b83.json"

# Inicializa la aplicación de Firebase Admin
try:
    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
    firebase_admin.initialize_app(cred)
except Exception as e:
    print(f"Error al inicializar Firebase Admin: {e}")
    print("Asegúrate de que la ruta a tu archivo de credenciales es correcta.")
    exit()

db = firestore.client()

def upload_knowledge_base(json_file_path):
    """Sube la base de conocimiento desde un archivo JSON a Firestore."""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: El archivo '{json_file_path}' no fue encontrado.")
        return
    except json.JSONDecodeError:
        print(f"Error: El archivo '{json_file_path}' no es un JSON válido.")
        return

    # Subir servicios_veterinaria
    if "servicios_veterinaria" in data:
        print("Subiendo 'servicios_veterinaria'...")
        for service in data["servicios_veterinaria"]:
            doc_id = service.get("id") # Usamos el ID como ID de documento en Firestore
            if doc_id:
                doc_ref = db.collection("servicios_veterinaria").document(doc_id)
                doc_ref.set(service)
                print(f"  Documento '{doc_id}' subido a 'servicios_veterinaria'.")
            else:
                print(f"  Advertencia: Servicio sin 'id', se omitirá: {service.get('nombre', 'Desconocido')}")
        print("'servicios_veterinaria' subido exitosamente.")
    else:
        print("La sección 'servicios_veterinaria' no se encontró en el JSON.")

    # Subir informacion_general_clinica
    if "informacion_general_clinica" in data:
        print("Subiendo 'informacion_general_clinica'...")
        for info_item in data["informacion_general_clinica"]:
            # Usamos el campo 'tema' como ID del documento si existe, si no, generamos uno
            doc_id = info_item.get("tema")
            if doc_id:
                doc_ref = db.collection("informacion_general_clinica").document(doc_id)
                doc_ref.set(info_item)
                print(f"  Documento '{doc_id}' subido a 'informacion_general_clinica'.")
            else:
                doc_ref = db.collection("informacion_general_clinica").document() # Generar un ID automático
                doc_ref.set(info_item)
                print(f"  Documento generado subido a 'informacion_general_clinica'.")
        print("'informacion_general_clinica' subido exitosamente.")
    else:
        print("La sección 'informacion_general_clinica' no se encontró en el JSON.")

if __name__ == "__main__":
    knowledge_base_file = "maskotas_knowledge_base.json" # <--- Asegúrate de que este es el nombre de tu archivo JSON
    print(f"Intentando subir datos desde '{knowledge_base_file}' a Firestore...")
    upload_knowledge_base(knowledge_base_file)
    print("Proceso de subida de datos completado.")
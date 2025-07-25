# 🐶 Chatbot Maskotas 🐾

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Google Gemini API](https://img.shields.io/badge/Google_Gemini-API-4285F4?style=for-the-badge&logo=google)
![Google Cloud Firestore](https://img.shields.io/badge/Firestore-DB-FFCA28?style=for-the-badge&logo=google-cloud)
![Firebase Admin SDK](https://img.shields.io/badge/Firebase-Admin_SDK-FFCA28?style=for-the-badge&logo=firebase)

Un chatbot inteligente para la clínica veterinaria "Maskotas", diseñado para responder preguntas frecuentes sobre servicios, horarios y más, utilizando Firestore y Google Gemini.

## 🌟 Descripción

**Chatbot Maskotas** es una aplicación de consola en Python que actúa como asistente virtual para una clínica veterinaria. Automatiza respuestas a consultas comunes combinando Firestore (base de datos NoSQL) con la IA de Google Gemini para respuestas naturales y precisas.

## ✨ Funcionalidades

- Responde preguntas sobre horarios, servicios y contacto.
- Base de conocimientos dinámica en Firestore.
- Usa Google Gemini para respuestas naturales.
- Escalable para interfaces web o móvil.

## 🚀 Tecnologías

- **Python 3.x**
- **Google Gemini API** (`google-generativeai`)
- **Google Cloud Firestore** (`firebase-admin`)
- **Firebase Admin SDK**

## 🛠️ Configuración

### 1. Clonar Repositorio

```bash
git clone https://github.com/<tu_usuario>/ChatbotMaskotas.git
cd ChatbotMaskotas
```

### 2. Entorno Virtual

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
# O manualmente:
pip install firebase-admin google-generativeai
```

### 4. Configurar Credenciales

#### Firebase (Firestore)
- Descarga la clave JSON desde Firebase Console → Cuentas de servicio.
- Renombra a `tu-clave-de-servicio.json` y colócala en la raíz del proyecto.
- Actualiza la ruta en `chatbot_main.py`:

```python
SERVICE_ACCOUNT_KEY_PATH = "./tu-clave-de-servicio.json"
```

**Nota:** Asegúrate de que el archivo JSON esté en `.gitignore`.

#### Google Gemini API
- Obtén la clave desde [Google AI Studio](https://aistudio.google.com/app/apikey).
- Configura la variable de entorno:

```bash
# Windows CMD
set GOOGLE_API_KEY="TU_CLAVE_API_DE_GEMINI_AQUI"
# Windows PowerShell
$env:GOOGLE_API_KEY="TU_CLAVE_API_DE_GEMINI_AQUI"
# macOS/Linux
export GOOGLE_API_KEY="TU_CLAVE_API_DE_GEMINI_AQUI"
```

### 5. Subir Base de Conocimientos

```bash
python upload_data.py
```

### 6. Ejecutar Chatbot

```bash
python chatbot_main.py
```

Escribe `salir` para terminar.

## 📚 Estructura Firestore

- **informacion_general_clinica**: Horarios, dirección, contacto.
- **servicios_veterinaria**: Descripción de servicios.

Los documentos deben incluir palabras clave relevantes (ej. "dirección", "ubicación").

## 🗺️ Roadmap

- Búsqueda semántica con embeddings.
- Contexto de conversación.
- Interfaz web/móvil.
- Mejor manejo de errores.
- Despliegue en la nube.

## 📄 Licencia

Licencia MIT. Ver archivo `LICENSE`.

## ✉️ Contacto

Abre un issue o contacta a [pacoaldev@gmail.com].
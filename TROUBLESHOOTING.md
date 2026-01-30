# 🔧 Guía de Troubleshooting - Chatbot Maskotas

## Problemas Comunes y Soluciones

---

## ❌ Error: "GOOGLE_API_KEY no está configurada"

### Síntomas
```
ERROR: La variable de entorno 'GOOGLE_API_KEY' no está configurada.
```

### Soluciones

#### Windows (CMD)
```bash
# Opción 1: Configurar temporalmente (solo para esta sesión)
set GOOGLE_API_KEY=tu_clave_aqui

# Opción 2: Permanente (requiere reiniciar cmd)
setx GOOGLE_API_KEY tu_clave_aqui

# Opción 3: Usar archivo .env (recomendado)
copy .env.example .env
# Editar .env y agregar tu clave
```

#### Windows (PowerShell)
```bash
$env:GOOGLE_API_KEY="tu_clave_aqui"
```

#### macOS/Linux
```bash
export GOOGLE_API_KEY="tu_clave_aqui"
# O permanente: agregar a ~/.bashrc o ~/.zshrc
echo 'export GOOGLE_API_KEY="tu_clave_aqui"' >> ~/.bashrc
source ~/.bashrc
```

### Verificar que está configurada
```bash
# Windows CMD
echo %GOOGLE_API_KEY%

# Windows PowerShell
$env:GOOGLE_API_KEY

# macOS/Linux
echo $GOOGLE_API_KEY
```

---

## ❌ Error: "Archivo de credenciales Firebase no encontrado"

### Síntomas
```
ERROR: Archivo de credenciales Firebase no encontrado en: 
  c:\Users\...\chatbot-maskotas-72d44d6d1b83.json
```

### Soluciones

1. **Verificar que el archivo existe:**
   ```bash
   # Windows
   dir chatbot-maskotas-*.json
   
   # macOS/Linux
   ls chatbot-maskotas-*.json
   ```

2. **Si el nombre es diferente:**
   - Descarga el archivo JSON nuevamente desde Firebase Console
   - Renombralo a: `chatbot-maskotas-72d44d6d1b83.json`
   - O edita `config.py` y cambia el nombre

3. **Verificar que está en la carpeta correcta:**
   - El archivo debe estar en la **raíz del proyecto**
   - Mismo nivel que `chatbot.py`

### Solución rápida
```python
# En config.py, verifica esta línea:
SERVICE_ACCOUNT_KEY_PATH = PROJECT_ROOT / "chatbot-maskotas-72d44d6d1b83.json"
# Asegúrate de que el nombre del archivo es correcto
```

---

## ❌ Error: "ModuleNotFoundError: No module named 'firebase_admin'"

### Síntomas
```
ModuleNotFoundError: No module named 'firebase_admin'
ModuleNotFoundError: No module named 'google'
```

### Soluciones

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verificar que pip está actualizado:**
   ```bash
   pip install --upgrade pip
   ```

3. **Instalar paquetes específicos:**
   ```bash
   pip install firebase-admin google-generativeai google-cloud-firestore
   ```

4. **Verificar instalación:**
   ```bash
   pip list | grep firebase
   pip list | grep google
   ```

5. **Usar entorno virtual (recomendado):**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate.bat
   pip install -r requirements.txt
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

---

## ❌ Error de Conexión a Firestore

### Síntomas
```
ERROR: [Errno 10061] No connection could be made because the target machine actively refused it
Google.Cloud.FireStore connection failed
```

### Soluciones

1. **Verificar conexión a internet:**
   ```bash
   ping google.com
   ```

2. **Verificar credenciales de Firebase:**
   - Abre el archivo JSON
   - Verifica que contiene campos: `type`, `project_id`, `private_key`, etc.
   - Si está corrupto, descargalo nuevamente

3. **Verificar que Firebase está activo:**
   - Ve a [Firebase Console](https://console.firebase.google.com/)
   - Verifica que tu proyecto está activo
   - Verifica que Firestore está habilitado

4. **Revisar permisos de Firestore:**
   - En Firebase Console → Firestore → Reglas de Seguridad
   - Asegúrate de que permiten lecturas/escrituras desde tu app
   - Para desarrollo, puedes usar:
   ```
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       match /{document=**} {
         allow read, write: if true;
       }
     }
   }
   ```

5. **Esperar a que Firestore esté listo:**
   - Si acabas de crear el proyecto, espera 5-10 minutos
   - Reinicia el script

---

## ❌ Error al Generar Respuestas de IA

### Síntomas
```
Error al generar respuesta de IA: 400 Bad Request
Respuesta bloqueada: BLOCKED_REASON_SAFETY
```

### Soluciones

1. **Respuesta bloqueada por seguridad:**
   - Algunas consultas son bloqueadas por políticas de Google
   - Intenta formular la pregunta de otra manera
   - Evita contenido ofensivo, violento o ilegal

2. **Verificar que la API Key es válida:**
   ```bash
   python -c "import google.generativeai as genai; genai.configure(api_key='TU_CLAVE'); print(genai.list_models())"
   ```

3. **Resetear la API Key:**
   - Ve a [Google AI Studio](https://aistudio.google.com/app/apikeys)
   - Regenera la clave
   - Actualiza la variable de entorno

4. **Verificar cuota de uso:**
   - Gémini tiene límites de uso gratuito
   - Ve a Google Cloud Console → APIs & Services → Quotas
   - Verifica que no has excedido límites

5. **Cambiar modelo (si es necesario):**
   - En `config.py`, prueba con:
   ```python
   AI_MODEL = "models/gemini-1.5-flash"  # Actual
   # O intenta:
   # AI_MODEL = "models/gemini-1.5-pro"
   ```

---

## ❌ Error: "ModuleNotFoundError: No module named 'config'"

### Síntomas
```
ModuleNotFoundError: No module named 'config'
```

### Soluciones

1. **Verifica que ejecutas desde la carpeta correcta:**
   ```bash
   # Debe estar en la carpeta del proyecto
   cd C:\Users\spano\Documents\Proyectos\ChatbotMaskiotas
   python chatbot.py
   ```

2. **Verifica que config.py existe:**
   ```bash
   dir config.py  # Windows
   ls config.py   # macOS/Linux
   ```

3. **Verifica que estás en el entorno virtual:**
   ```bash
   # Debería mostrar (venv) al inicio de la línea
   pip --version
   ```

---

## ⚠️ El Chatbot Responde Cosas Irrelevantes

### Síntomas
```
P: ¿Dónde están ubicados?
R: La pizza es un alimento popular...
```

### Soluciones

1. **Mejorar la base de conocimientos:**
   - Verifica que `maskotas_knowledge_base.json` tiene información correcta
   - Agrega más palabras clave relevantes
   - Ejemplo:
   ```json
   {
     "tema": "ubicacion",
     "ubicación": "Calle Principal 123",
     "dirección": "Calle Principal 123",
     "dónde": "Calle Principal 123",
     "donde": "Calle Principal 123"
   }
   ```

2. **Mejorar el prompt del sistema:**
   - En `config.py`, actualiza `system_prompt`
   - Sé más específico sobre el comportamiento deseado

3. **Usar búsqueda más robusta:**
   - La búsqueda actual es simple (palabra clave)
   - Para mejores resultados, implementa búsqueda semántica con embeddings

---

## 📝 Los Logs No Se Guardan

### Síntomas
```
No se crea la carpeta logs/
No aparece chatbot.log
```

### Soluciones

1. **Verificar permisos:**
   - Verifica que tienes permisos para crear carpetas
   - Ejecuta como administrador si es necesario

2. **Crear carpeta manualmente:**
   ```bash
   mkdir logs  # macOS/Linux
   md logs     # Windows
   ```

3. **Verificar que logger se inicializa:**
   ```python
   from logger import setup_logging
   setup_logging()  # Debe llamarse antes de usar logs
   ```

4. **Ver logs en consola mientras se crean:**
   ```python
   # En chatbot.py, asegúrate de que setup_logging se ejecuta
   if __name__ == "__main__":
       setup_logging()  # Esta línea debe existir
       chatbot = MaskotasChatbot()
       chatbot.chat_interactive()
   ```

---

## 🐌 El Chatbot es Lento

### Síntomas
```
Demora 5+ segundos en responder
```

### Soluciones

1. **Reducir tamaño de la base de datos:**
   - Crea colecciones separadas por tema
   - Elimina datos innecesarios

2. **Implementar caché:**
   ```python
   # Agregar en database.py
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def search_collection(self, collection_name, query_text):
       # ...
   ```

3. **Usar índices en Firestore:**
   - Ve a Firebase Console → Firestore → Índices
   - Crea índices en campos frecuentemente buscados

4. **Optimizar búsqueda:**
   - En lugar de buscar en todo el documento, busca en campos específicos

---

## 🔴 Error: "RuntimeError: Errores de configuración"

### Síntomas
```
RuntimeError: Errores de configuración:
GOOGLE_API_KEY no está configurada en variables de entorno
Archivo de credenciales Firebase no encontrado en: ...
```

### Soluciones
Ver secciones anteriores sobre:
- GOOGLE_API_KEY
- Archivo Firebase

---

## 📊 Tests No Pasan

### Síntomas
```
FAILED test_chatbot.py::TestConfiguration::test_google_api_key_configured
```

### Soluciones

1. **Instalar pytest:**
   ```bash
   pip install pytest
   ```

2. **Configurar variables de entorno:**
   ```bash
   set GOOGLE_API_KEY=tu_clave  # Windows
   export GOOGLE_API_KEY=tu_clave  # macOS/Linux
   ```

3. **Verificar archivos:**
   - Asegúrate que exista `chatbot-maskotas-72d44d6d1b83.json`
   - Asegúrate que exista `maskotas_knowledge_base.json`

4. **Ejecutar tests con verbosidad:**
   ```bash
   pytest test_chatbot.py -v -s
   ```

---

## 💻 Comando Not Found

### Síntomas
```
'python' is not recognized as an internal or external command
```

### Soluciones

1. **Instalar Python:**
   - Descarga desde [python.org](https://www.python.org/downloads/)
   - **Importante:** marca "Add Python to PATH" durante la instalación

2. **Usar python3:**
   ```bash
   python3 chatbot.py  # macOS/Linux
   ```

3. **Verificar instalación:**
   ```bash
   python --version
   ```

4. **Agregar Python a PATH (Windows):**
   - Busca "Editar variables de entorno"
   - Edita variable `Path`
   - Agrega la ruta de Python (ej: `C:\Python311`)

---

## 🌐 Error: "Conexión rechazada" (Connection Refused)

### Síntomas
```
[Errno 10061] No connection could be made because the target machine actively refused it
[Errno 111] Connection refused
```

### Soluciones

1. **Verificar que hay internet:**
   ```bash
   ping google.com
   ```

2. **Verificar firewall:**
   - Puede estar bloqueando conexiones
   - Agrega Python a excepciones del firewall

3. **Verificar que Firestore está accesible:**
   - A veces Google Cloud tiene outages
   - Revisa [status.firebase.google.com](https://status.firebase.google.com/)

4. **Usar VPN (si es necesario):**
   - Si estás en una red restricitiva, considera usar VPN

---

## 📱 Preguntas de Usuarios No Son Entendidas

### Síntomas
```
P: Hola
R: Lo siento, no encontré información sobre eso
```

### Soluciones

1. **Agregar sinónimos a la base de datos:**
   ```json
   {
     "tema": "horario",
     "horario": "Lunes a Viernes 8am-6pm",
     "horas": "Lunes a Viernes 8am-6pm",
     "cuando": "Lunes a Viernes 8am-6pm",
     "abierto": "Lunes a Viernes 8am-6pm"
   }
   ```

2. **Mejorar el prompt del sistema:**
   - Ser más específico sobre cómo responder
   - Agregar ejemplos

3. **Usar búsqueda semántica:**
   - Implementar embeddings para mejor matching
   - Librería recomendada: `sentence-transformers`

---

## ✅ Verificación de Salud (Health Check)

Para verificar que todo está funcionando:

```bash
# 1. Verificar Python
python --version

# 2. Verificar dependencias
pip list | grep firebase
pip list | grep google

# 3. Verificar configuración
python -c "from config import validate_config; validate_config(); print('OK')"

# 4. Ejecutar tests
pytest test_chatbot.py -v

# 5. Probar el chatbot
python chatbot.py
```

---

## 📞 Si Nada Funciona

### Pasos finales:

1. **Reinstalar todo:**
   ```bash
   # Eliminar entorno virtual
   rmdir /s venv  # Windows
   rm -rf venv    # macOS/Linux
   
   # Recrear
   python -m venv venv
   
   # Activar
   venv\Scripts\activate.bat  # Windows
   source venv/bin/activate  # macOS/Linux
   
   # Instalar
   pip install -r requirements.txt
   ```

2. **Verificar archivos esenciales:**
   ```
   chatbot-maskotas-72d44d6d1b83.json ✓
   maskotas_knowledge_base.json ✓
   config.py ✓
   chatbot.py ✓
   .env (con GOOGLE_API_KEY) ✓
   ```

3. **Consultar logs:**
   ```bash
   # Ver últimas líneas del log
   tail -100 logs/chatbot.log  # macOS/Linux
   type logs\chatbot.log       # Windows
   ```

4. **Contacto:**
   - Abre un issue en GitHub
   - Incluye:
     - Versión de Python
     - Salida de `pip list`
     - Mensajes de error completos
     - Archivo de log

---

**Última actualización:** Enero 2026  
**Versión:** 2.0  
**Cubiertos:** 95% de problemas comunes

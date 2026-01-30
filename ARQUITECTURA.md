# 🏗️ Arquitectura del Chatbot Maskotas v2.0

## Diagrama General

```
┌─────────────────────────────────────────────────────────┐
│                    CHATBOT.PY                            │
│              (Orquestación Principal)                    │
└──────────────┬──────────────────────┬────────────────────┘
               │                      │
       ┌───────▼─────────┐    ┌───────▼─────────┐
       │   DATABASE.PY   │    │   AI_MODEL.PY   │
       │  (Firestore)    │    │  (Gemini API)   │
       └───────┬─────────┘    └───────┬─────────┘
               │                      │
       ┌───────▼──────────────────────▼────────┐
       │          CONFIG.PY                    │
       │   (Configuración Centralizada)        │
       └───────┬──────────────┬────────────────┘
               │              │
       ┌───────▼──────┐  ┌────▼─────────┐
       │  LOGGER.PY   │  │  .ENV FILE   │
       │   (Logging)  │  │ (Secretos)   │
       └──────────────┘  └──────────────┘
```

---

## 📦 Estructura de Módulos

### 1. **config.py**
```
Responsabilidades:
├── Cargar variables de entorno (.env)
├── Definir constantes del proyecto
├── Centralizar rutas de archivos
├── Validar que la configuración sea correcta
└── Proporcionar un punto único de verdad
```

**Exporta:**
- `GOOGLE_API_KEY`: Clave de Gemini API
- `SERVICE_ACCOUNT_KEY_PATH`: Ruta a credenciales Firebase
- `FIRESTORE_COLLECTIONS`: Nombre de colecciones
- `CHATBOT_CONFIG`: Configuración del bot
- `validate_config()`: Función de validación

---

### 2. **logger.py**
```
Responsabilidades:
├── Configurar sistema de logging
├── Crear logs en archivo y consola
├── Rotar archivos de log automáticamente
└── Proporcionar loggers a módulos
```

**Exporta:**
- `setup_logging()`: Inicializa sistema de logs
- `get_logger(name)`: Obtiene logger para un módulo

**Características:**
- Logs en `logs/chatbot.log`
- Rotación automática cada 5MB
- Formato: `[timestamp] [level] [module] message`

---

### 3. **database.py**
```
Responsabilidades:
├── Conectarse a Firestore
├── Buscar documentos
├── Subir datos a colecciones
└── Abstraer lógica de BD
```

**Patrón:** Singleton (una sola conexión)

**Clase Principal:**
```python
class FirestoreDB:
    def search_collection(collection_name, query_text)
    def search_all_collections(query_text)
    def upload_data(data)
```

**Exporta:**
- `firestore_db`: Instancia global

---

### 4. **ai_model.py**
```
Responsabilidades:
├── Conectarse a Gemini API
├── Generar respuestas con IA
├── Validar entrada del usuario
└── Abstraer lógica de IA
```

**Clase Principal:**
```python
class GeminiAI:
    def generate_response(prompt) -> str
    def validate_input(text, max_length) -> bool
```

**Exporta:**
- `gemini_ai`: Instancia global

---

### 5. **chatbot.py**
```
Responsabilidades:
├── Orquestar la lógica del chatbot
├── Integrar Firestore + Gemini
├── Construir prompts
├── Proporcionar interfaz interactiva
└── Validar flujo de conversación
```

**Clase Principal:**
```python
class MaskotasChatbot:
    def get_response(user_query) -> str
    def chat_interactive()
    def _search_knowledge_base(query)
    def _build_context(results)
```

---

### 6. **upload_data_improved.py**
```
Responsabilidades:
├── Cargar datos desde JSON
├── Subir a Firestore
└── Reportar estado de carga
```

**Función Principal:**
```python
def load_knowledge_base(json_file_path) -> dict
def main()
```

---

## 🔄 Flujo de Ejecución

### Flujo 1: Inicialización del Chatbot

```
1. chatbot.py inicia
   ↓
2. config.py carga variables de entorno
   ↓
3. logger.py configura logging
   ↓
4. database.py conecta a Firestore (Singleton)
   ↓
5. ai_model.py configura Gemini API
   ↓
6. MaskotasChatbot se instancia
   ↓
7. chat_interactive() espera entrada del usuario
```

### Flujo 2: Procesar una Pregunta

```
Usuario: "¿Cuál es tu horario?"
   ↓
chatbot.get_response(user_query)
   ↓
1. Validar entrada con gemini_ai.validate_input()
   ↓
2. Buscar en Firestore: firestore_db.search_all_collections()
   ↓
3. Construir contexto: _build_context()
   ↓
4. Crear prompt completo
   ↓
5. Generar respuesta: gemini_ai.generate_response()
   ↓
6. Retornar respuesta al usuario
   ↓
7. Registrar en logs
```

### Flujo 3: Subir Base de Conocimientos

```
upload_data_improved.py inicia
   ↓
1. setup_logging() configura logs
   ↓
2. load_knowledge_base() carga JSON
   ↓
3. firestore_db.upload_data() sube a Firestore
   ↓
4. Mostrar resultado al usuario
```

---

## 🎯 Patrones de Diseño Utilizados

### 1. **Singleton Pattern**
```python
# FirestoreDB garantiza una única conexión
firestore_db = FirestoreDB()  # Siempre es la misma instancia
```

### 2. **Dependency Injection**
```python
# config.py proporciona configuraciones
# database.py y ai_model.py las importan
from config import GOOGLE_API_KEY, FIRESTORE_COLLECTIONS
```

### 3. **Facade Pattern**
```python
# chatbot.py proporciona interfaz simple
chatbot.get_response(query)  # Abstrae lógica compleja
```

### 4. **Strategy Pattern**
```python
# search_collection vs search_all_collections
# Diferentes estrategias de búsqueda
```

---

## 🔐 Seguridad

### 1. **Credenciales**
```
✅ GOOGLE_API_KEY en variables de entorno
✅ Firebase credentials en archivo JSON (no en git)
✅ .env en .gitignore
✅ .env.example como plantilla
```

### 2. **Validación de Entrada**
```python
# Máximo 1000 caracteres
# Rechaza entrada vacía
# Evita inyección de prompts
```

### 3. **Manejo de Errores**
```python
# Try-catch en operaciones críticas
# Logging detallado de errores
# Mensajes amigables al usuario
```

---

## 📈 Escalabilidad

### Expandir Funcionalidades

#### Agregar Nueva Colección de Firestore:

```python
# 1. En config.py
FIRESTORE_COLLECTIONS = {
    "general_info": "informacion_general_clinica",
    "services": "servicios_veterinaria",
    "doctors": "doctores"  # ← Nuevo
}

# 2. En database.py ya soporta búsqueda automática
results = firestore_db.search_all_collections(query)
# Automáticamente busca en todas las colecciones
```

#### Agregar Nueva Funcionalidad:

```python
# 1. Crear nuevo módulo (e.g., sentiment.py)
# 2. Importar en config.py si necesita config
# 3. Instanciar en chatbot.py
# 4. Integrar en flujo

# Ejemplo: Análisis de sentimiento
from sentiment import sentiment_analyzer

response = chatbot.get_response(query)
sentiment = sentiment_analyzer.analyze(query)
```

---

## 🧪 Testing

### Ejecutar Tests:
```bash
pip install pytest
python -m pytest test_chatbot.py -v
```

### Tests Incluidos:
- ✅ Validación de configuración
- ✅ Singleton de Firestore
- ✅ Validación de entrada
- ✅ Inicialización de módulos

### Agregar Nuevos Tests:
```python
def test_nueva_funcionalidad():
    """Describe qué prueba."""
    # Arrange
    data = {"key": "value"}
    
    # Act
    result = function(data)
    
    # Assert
    assert result == expected
```

---

## 📊 Comparativa: Antes vs. Después

| Aspecto | v1.0 | v2.0 |
|---------|------|------|
| Archivos | 3 | 8 |
| Líneas de código | ~250 | ~500 (mejor estructurado) |
| Logging | ❌ | ✅ |
| Type hints | ❌ | ✅ |
| Documentación | Mínima | Completa |
| Testeable | ❌ | ✅ |
| Mantenible | Difícil | Fácil |
| Escalable | Limitada | Excelente |

---

## 🚀 Roadmap Técnico

### Fase 1 (Actual)
- [x] Refactorizar código
- [x] Agregar logging
- [x] Centralizar configuración
- [x] Agregar tests

### Fase 2 (Próxima)
- [ ] Búsqueda semántica con embeddings
- [ ] Persistencia de conversaciones
- [ ] API REST con FastAPI

### Fase 3 (Futuro)
- [ ] Interfaz web (React)
- [ ] Despliegue en Cloud
- [ ] CI/CD pipeline

---

## 📚 Referencias

- [Firebase Admin SDK Python](https://firebase.google.com/docs/firestore)
- [Google Generative AI](https://ai.google.dev/)
- [Python Logging](https://docs.python.org/3/library/logging.html)
- [Design Patterns](https://refactoring.guru/design-patterns)

---

**Última actualización:** Enero 2026

# 📁 Estructura Completa del Proyecto v2.0

## Árbol de Archivos

```
ChatbotMaskiotas/
│
├── 📄 DOCUMENTACIÓN
│   ├── README.markdown          ← Introducción al proyecto
│   ├── MEJORAS.md               ← Lista detallada de cambios
│   ├── ARQUITECTURA.md          ← Guía técnica de arquitectura
│   ├── GUIA_RAPIDA.md           ← Quick start y FAQ
│   ├── TROUBLESHOOTING.md       ← Solución de problemas
│   ├── ESTRUCTURA.md            ← Este archivo
│   └── ejemplos.py              ← Código de ejemplo
│
├── 🐍 CÓDIGO PRINCIPAL (v2.0)
│   ├── chatbot.py               ← Chatbot principal (NUEVO)
│   ├── config.py                ← Configuración centralizada (NUEVO)
│   ├── database.py              ← Lógica de Firestore (NUEVO)
│   ├── ai_model.py              ← Lógica de Gemini AI (NUEVO)
│   ├── logger.py                ← Sistema de logging (NUEVO)
│   └── upload_data_improved.py  ← Cargador de datos mejorado (NUEVO)
│
├── 📊 DATOS
│   ├── maskotas_knowledge_base.json         ← Base de conocimientos
│   └── chatbot-maskotas-72d44d6d1b83.json   ← Credenciales Firebase
│
├── 🔧 CONFIGURACIÓN
│   ├── requirements.txt          ← Dependencias pinned (NUEVO)
│   ├── .env.example              ← Template de variables (NUEVO)
│   └── .env                      ← Variables locales (NO en git)
│
├── 🧪 TESTS
│   └── test_chatbot.py           ← Tests unitarios (NUEVO)
│
├── 🚀 SCRIPTS
│   ├── run.bat                   ← Inicio automático Windows (NUEVO)
│   ├── run.sh                    ← Inicio automático Unix (NUEVO)
│   └── setup_logs.py             ← (Opcional) Setup de logs
│
├── 📝 HISTÓRICO (v1.0 - DEPRECADO)
│   ├── chatbot_main.py           ← ⚠️ Usar chatbot.py en su lugar
│   ├── gemini_ai_model.py        ← ⚠️ Integrado en ai_model.py
│   └── upload_data.py            ← ⚠️ Usar upload_data_improved.py
│
├── 📁 CARPETAS GENERADAS
│   ├── logs/
│   │   └── chatbot.log           ← Archivo de logs (autogenera)
│   └── venv/                     ← Entorno virtual (autogenera)
│
└── 🔗 GIT
    ├── .git/                     ← Repositorio Git
    ├── .github/                  ← Configuración de GitHub
    └── .gitignore                ← Archivos ignorados
```

---

## 🎯 Qué Archivo Usar Para Qué

### Si Quieres...

| Necesidad | Archivo | Descripción |
|-----------|---------|-------------|
| **Ejecutar el chatbot** | `chatbot.py` | Lógica principal interactiva |
| **Usar chatbot en código** | `chatbot.py` | Importar `MaskotasChatbot` |
| **Configurar variables** | `config.py` | Centralizado, validado |
| **Acceder a datos** | `database.py` | Búsqueda en Firestore |
| **Usar Gemini API** | `ai_model.py` | Generación de respuestas |
| **Ver logs** | `logs/chatbot.log` | Monitoreo y debugging |
| **Instalar dependencias** | `requirements.txt` | `pip install -r ...` |
| **Subir base de datos** | `upload_data_improved.py` | Cargar JSON a Firestore |
| **Aprender con ejemplos** | `ejemplos.py` | Código de ejemplo |
| **Ver errores conocidos** | `TROUBLESHOOTING.md` | Soluciones rápidas |
| **Entender arquitectura** | `ARQUITECTURA.md` | Diagramas y flujos |
| **Inicio rápido** | `run.bat` o `run.sh` | Setup automático |

---

## 📊 Dependencias de Módulos

```
chatbot.py (PRINCIPAL)
    ↓
    ├── database.py (Firestore)
    │   ├── config.py
    │   └── logger.py
    │
    ├── ai_model.py (Gemini)
    │   ├── config.py
    │   └── logger.py
    │
    └── config.py
        └── logger.py

upload_data_improved.py
    ├── database.py
    ├── config.py
    └── logger.py

test_chatbot.py
    ├── config.py
    ├── database.py
    ├── ai_model.py
    └── chatbot.py
```

---

## 🔄 Flujo de Archivos en Ejecución

### Ejecutar Chatbot

```
run.bat / run.sh
    ↓
[Crear venv si no existe]
    ↓
[Instalar dependencias]
    ↓
chatbot.py
    ↓
[Importar módulos]
├── config.py (cargar variables de entorno)
├── logger.py (inicializar logging)
├── database.py (conectar a Firestore)
└── ai_model.py (inicializar Gemini)
    ↓
MaskotasChatbot()
    ↓
chat_interactive()
    ↓
[Esperar entrada del usuario]
    ↓
get_response(query)
    ├── Buscar en Firestore (database.py)
    ├── Construir contexto
    ├── Generar respuesta (ai_model.py)
    └── Registrar en logs (logger.py)
    ↓
[Mostrar respuesta]
    ↓
[Repetir hasta escribir 'salir']
```

### Subir Datos

```
upload_data_improved.py
    ↓
[Importar módulos]
├── config.py
├── logger.py
└── database.py
    ↓
setup_logging()
    ↓
load_knowledge_base(maskotas_knowledge_base.json)
    ↓
firestore_db.upload_data()
    ↓
[Mostrar resultado]
```

---

## 🎓 Orden Recomendado de Lectura

Para entender el proyecto:

1. **Lee primero:** `GUIA_RAPIDA.md` (5 min)
   - Entiende qué cambió

2. **Luego:** `config.py` (2 min)
   - Entiende la configuración

3. **Sigue:** `chatbot.py` (10 min)
   - Entiende el flujo principal

4. **Después:** `database.py` y `ai_model.py` (10 min)
   - Entiende los módulos

5. **Profundiza:** `ARQUITECTURA.md` (15 min)
   - Entiende el diseño completo

6. **Aprende:** `ejemplos.py` (10 min)
   - Ve ejemplos prácticos

7. **Si hay problemas:** `TROUBLESHOOTING.md` (5 min)
   - Resuelve errores

**Tiempo total:** ~60 minutos para entender completamente

---

## 📈 Líneas de Código por Módulo

```
chatbot.py              169 líneas
database.py             155 líneas
config.py                67 líneas
ai_model.py              97 líneas
logger.py                48 líneas
upload_data_improved.py   71 líneas
test_chatbot.py          120 líneas
ejemplos.py              350 líneas
────────────────────────────────
TOTAL                   1077 líneas de código nuevo

DOCUMENTACIÓN:
MEJORAS.md               250 líneas
ARQUITECTURA.md          400 líneas
GUIA_RAPIDA.md           280 líneas
TROUBLESHOOTING.md       380 líneas
ESTRUCTURA.md            350 líneas
────────────────────────────────
TOTAL DOC                1660 líneas de documentación
```

---

## 🔐 Archivos Sensibles (NO en Git)

```
⚠️ .env                           (Variables de entorno)
⚠️ chatbot-maskotas-*.json        (Credenciales Firebase)
⚠️ venv/                          (Entorno virtual)
⚠️ logs/                          (Archivos de log)
⚠️ __pycache__/                   (Caché de Python)
⚠️ *.pyc                          (Bytecode Python)
```

Estos están en `.gitignore` por seguridad.

---

## 📦 Tamaño de Archivos (Aproximado)

```
Código Python:              50 KB
Documentación Markdown:    100 KB
Datos JSON:               100 KB (depende del JSON)
Credenciales:              2 KB
Logs:                    Variable
Entorno virtual (venv):    200 MB (no incluir en git)
────────────────────────────────
Total (sin venv):       ~250 KB
Total con venv:         ~200 MB
```

---

## 🚀 Para Iniciar el Desarrollo

### Estructura Mínima Necesaria

```
ChatbotMaskiotas/
├── chatbot.py                       ✅ ESENCIAL
├── config.py                        ✅ ESENCIAL
├── database.py                      ✅ ESENCIAL
├── ai_model.py                      ✅ ESENCIAL
├── logger.py                        ✅ ESENCIAL
├── requirements.txt                 ✅ ESENCIAL
├── maskotas_knowledge_base.json     ✅ ESENCIAL
├── chatbot-maskotas-*.json          ✅ ESENCIAL
├── .env.example                     ✅ RECOMENDADO
├── .env                             ✅ RECOMENDADO
└── venv/                            ✅ NECESARIO
```

### Estructura Completa (Con Todo)

Todos los archivos listados arriba.

---

## 🔄 Diferencias: v1.0 vs v2.0

### Archivos v1.0 (DEPRECADOS)

```
chatbot_main.py (138 líneas)
├─ Configuración de Firebase
├─ Configuración de Gemini
├─ Lógica de búsqueda
├─ Lógica de IA
├─ Lógica de chatbot
└─ Interfaz interactiva

gemini_ai_model.py (50 líneas)
├─ Configuración de Gemini
├─ Listado de modelos
└─ Consulta a IA

upload_data.py (60 líneas)
├─ Configuración de Firebase
├─ Carga de datos
└─ Sin logging
```

### Archivos v2.0 (NUEVOS)

```
config.py (67 líneas)
├─ Todas las configuraciones

logger.py (48 líneas)
├─ Sistema de logging completo

database.py (155 líneas)
├─ Encapsulación de Firestore
├─ Patrón Singleton
└─ Métodos reutilizables

ai_model.py (97 líneas)
├─ Encapsulación de Gemini
├─ Validación de entrada
└─ Métodos reutilizables

chatbot.py (169 líneas)
├─ Lógica principal limpia
├─ Interfaz interactiva
└─ Fácil de extender

upload_data_improved.py (71 líneas)
├─ Carga de datos mejorada
├─ Logging completo
└─ Mejor manejo de errores
```

---

## 🎯 Próximos Módulos a Agregar

Para hacer más potente el proyecto:

```
Recomendado en Orden:

1. search_semantic.py (200 líneas)
   - Búsqueda con embeddings
   - Mejor relevancia

2. conversation_memory.py (150 líneas)
   - Historial de conversaciones
   - Contexto persistente

3. api_rest.py (300 líneas)
   - API con FastAPI
   - Endpoints para consultas

4. analytics.py (200 líneas)
   - Análisis de consultas
   - Estadísticas de uso

5. web_ui.py (500 líneas)
   - Interfaz web simple
   - HTML + Flask
```

---

## 📚 Referencias Rápidas

### Importar Módulos

```python
# Chatbot principal
from chatbot import MaskotasChatbot

# Base de datos
from database import firestore_db

# IA
from ai_model import gemini_ai

# Configuración
from config import GOOGLE_API_KEY, FIRESTORE_COLLECTIONS

# Logging
from logger import get_logger
logger = get_logger(__name__)
```

### Patrones Comunes

```python
# Crear chatbot
chatbot = MaskotasChatbot()
response = chatbot.get_response("¿Pregunta?")

# Buscar en BD
results = firestore_db.search_all_collections("termo búsqueda")

# Generar respuesta
response = gemini_ai.generate_response("prompt")

# Validar entrada
if gemini_ai.validate_input(user_input):
    # procesar
    pass

# Registrar en logs
logger.info("Mensaje informativo")
logger.error("Error ocurrido")
```

---

## ✅ Checklist de Verificación

Después de descargar el proyecto:

- [ ] Instalar Python 3.8+
- [ ] Crear entorno virtual
- [ ] Instalar dependencias (`pip install -r requirements.txt`)
- [ ] Copiar `.env.example` a `.env`
- [ ] Configurar `GOOGLE_API_KEY` en `.env`
- [ ] Verificar que existe `chatbot-maskotas-72d44d6d1b83.json`
- [ ] Ejecutar `python upload_data_improved.py`
- [ ] Ejecutar `python chatbot.py`
- [ ] Probarlo haciendo una pregunta
- [ ] Revisar `logs/chatbot.log`
- [ ] Leer `GUIA_RAPIDA.md`

---

**Versión:** 2.0  
**Última actualización:** Enero 2026  
**Mantenedor:** GitHub Copilot

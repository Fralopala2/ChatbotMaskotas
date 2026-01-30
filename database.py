"""
Módulo para interactuar con Firestore.
Encapsula toda la lógica de base de datos.
"""

import json
from typing import List, Dict, Any
import firebase_admin
from firebase_admin import credentials, firestore
from config import FIREBASE_CREDENTIALS_PATH, FIRESTORE_COLLECTIONS
from logger import get_logger

logger = get_logger("database")


class FirestoreDB:
    """Gestor de conexión y operaciones con Firestore."""
    
    _instance = None
    
    def __new__(cls):
        """Implementa patrón singleton para la conexión a Firestore."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Inicializa la conexión a Firestore (solo una vez)."""
        if self._initialized:
            return
        
        try:
            cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
            self.db = firestore.client()
            self._initialized = True
            logger.info("Firestore inicializado correctamente")
        except FileNotFoundError:
            logger.error(f"Archivo de credenciales no encontrado: {FIREBASE_CREDENTIALS_PATH}")
            raise
        except Exception as e:
            logger.error(f"Error al inicializar Firebase: {e}")
            raise
    
    def search_collection(self, collection_name: str, query_text: str) -> List[Dict[str, Any]]:
        """
        Busca documentos en una colección basados en texto.
        NOTA: Esta es una búsqueda simple. Para mejor rendimiento, usar embeddings.
        
        Args:
            collection_name: Nombre de la colección
            query_text: Texto para buscar
            
        Returns:
            Lista de documentos que contienen el texto
        """
        try:
            results = []
            docs = self.db.collection(collection_name).stream()
            
            query_lower = query_text.lower()
            
            for doc in docs:
                doc_data = doc.to_dict()
                # Convertir documento a string para búsqueda
                doc_string = json.dumps(doc_data, ensure_ascii=False).lower()
                
                if query_lower in doc_string:
                    results.append(doc_data)
            
            logger.debug(f"Búsqueda en '{collection_name}' para '{query_text}': {len(results)} resultados")
            return results
            
        except Exception as e:
            logger.error(f"Error al buscar en Firestore: {e}")
            return []
    
    def search_all_collections(self, query_text: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Busca en todas las colecciones definidas.
        
        Args:
            query_text: Texto para buscar
            
        Returns:
            Diccionario con resultados por colección
        """
        results = {}
        
        for key, collection_name in FIRESTORE_COLLECTIONS.items():
            results[key] = self.search_collection(collection_name, query_text)
        
        return results
    
    def upload_data(self, data: Dict[str, List[Dict[str, Any]]]) -> bool:
        """
        Sube datos a Firestore desde un diccionario.
        
        Args:
            data: Diccionario con las colecciones y documentos
            
        Returns:
            True si fue exitoso, False en caso contrario
        """
        try:
            # Subir servicios
            if "servicios_veterinaria" in data:
                logger.info("Subiendo servicios_veterinaria...")
                for service in data["servicios_veterinaria"]:
                    doc_id = service.get("id")
                    if doc_id:
                        doc_ref = self.db.collection("servicios_veterinaria").document(doc_id)
                        doc_ref.set(service)
                        logger.debug(f"Servicio '{doc_id}' subido")
                    else:
                        logger.warning(f"Servicio sin ID: {service.get('nombre', 'Desconocido')}")
            
            # Subir información general
            if "informacion_general_clinica" in data:
                logger.info("Subiendo informacion_general_clinica...")
                for info_item in data["informacion_general_clinica"]:
                    doc_id = info_item.get("tema")
                    if doc_id:
                        doc_ref = self.db.collection("informacion_general_clinica").document(doc_id)
                        doc_ref.set(info_item)
                        logger.debug(f"Información '{doc_id}' subida")
                    else:
                        doc_ref = self.db.collection("informacion_general_clinica").document()
                        doc_ref.set(info_item)
                        logger.debug("Información con ID automático subida")
            
            logger.info("Datos subidos correctamente a Firestore")
            return True
            
        except Exception as e:
            logger.error(f"Error al subir datos a Firestore: {e}")
            return False


# Instancia global
firestore_db = FirestoreDB()

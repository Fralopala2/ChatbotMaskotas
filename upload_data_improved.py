"""
Script mejorado para subir la base de conocimientos a Firestore.
"""

import json
import sys
from pathlib import Path
from database import firestore_db
from config import KNOWLEDGE_BASE_FILE
from logger import setup_logging, get_logger

logger = get_logger("upload_data")


def load_knowledge_base(json_file_path: str) -> dict:
    """
    Carga la base de conocimientos desde un archivo JSON.
    
    Args:
        json_file_path: Ruta al archivo JSON
        
    Returns:
        Diccionario con los datos cargados
        
    Raises:
        FileNotFoundError: Si el archivo no existe
        json.JSONDecodeError: Si el JSON no es válido
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Base de conocimientos cargada desde: {json_file_path}")
        return data
    except FileNotFoundError:
        logger.error(f"Archivo no encontrado: {json_file_path}")
        raise
    except json.JSONDecodeError:
        logger.error(f"JSON inválido en: {json_file_path}")
        raise


def main():
    """Función principal."""
    print("\n" + "="*60)
    print("📚 Subidor de Base de Conocimientos - Clínica Maskotas")
    print("="*60 + "\n")
    
    try:
        # Cargar datos
        logger.info("Iniciando carga de datos...")
        data = load_knowledge_base(str(KNOWLEDGE_BASE_FILE))
        
        # Subir a Firestore
        success = firestore_db.upload_data(data)
        
        if success:
            print("✅ Base de conocimientos subida exitosamente a Firestore")
            logger.info("Proceso de carga completado correctamente")
        else:
            print("❌ Error al subir la base de conocimientos")
            logger.error("Proceso de carga falló")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Error durante la carga: {e}")
        sys.exit(1)


if __name__ == "__main__":
    setup_logging()
    main()

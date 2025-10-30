import os
import sqlite3
import shutil
from datetime import datetime

def reset_database_completely():
    """Eliminar y recrear completamente la base de datos"""
    
    print("🗑️  RESETEANDO BASE DE DATOS COMPLETAMENTE...")
    print("=" * 50)
    
    db_path = "data/test_results.db"
    
    # 1. Crear backup de la base de datos actual
    if os.path.exists(db_path):
        backup_path = f"data/test_results_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy2(db_path, backup_path)
        print(f"📦 Backup creado: {backup_path}")
    
    # 2. Eliminar la base de datos existente
    try:
        if os.path.exists(db_path):
            os.remove(db_path)
            print("✅ Base de datos eliminada completamente")
        else:
            print("⚠️  Base de datos no existía")
    except Exception as e:
        print(f"❌ Error eliminando base de datos: {e}")
        return False
    
    # 3. Recrear la base de datos desde cero
    try:
        from utils.database import DatabaseManager
        db = DatabaseManager()  # Esto creará la base de datos nueva
        print("✅ Base de datos recreada con estructura nueva")
        
        # Verificar que está vacía
        results = db.get_test_results()
        print(f"📊 Registros en nueva BD: {len(results)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error recreando base de datos: {e}")
        return False

def clean_allure_results():
    """Limpiar resultados de Allure"""
    print("\n🧹 LIMPIANDO ALLURE-RESULTS...")
    
    allure_dir = "allure-results"
    if os.path.exists(allure_dir):
        try:
            shutil.rmtree(allure_dir)  # Eliminar carpeta completa
            os.makedirs(allure_dir)     # Recrear vacía
            print("✅ Carpeta allure-results limpiada completamente")
        except Exception as e:
            print(f"❌ Error limpiando allure-results: {e}")
    else:
        os.makedirs(allure_dir)
        print("✅ Carpeta allure-results creada")

def clean_screenshots():
    """Limpiar screenshots"""
    print("\n📸 LIMPIANDO SCREENSHOTS...")
    
    screenshots_dir = "screenshots"
    if os.path.exists(screenshots_dir):
        try:
            shutil.rmtree(screenshots_dir)  # Eliminar carpeta completa
            os.makedirs(screenshots_dir)    # Recrear vacía
            print("✅ Carpeta screenshots limpiada completamente")
        except Exception as e:
            print(f"❌ Error limpiando screenshots: {e}")
    else:
        os.makedirs(screenshots_dir)
        print("✅ Carpeta screenshots creada")

def verify_clean_state():
    """Verificar que todo está limpio"""
    print("\n🔍 VERIFICANDO ESTADO LIMPIO...")
    
    # Verificar base de datos
    db_path = "data/test_results.db"
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM test_results")
        count = cursor.fetchone()[0]
        conn.close()
        print(f"📊 Base de datos: {count} registros")
    else:
        print("❌ Base de datos no existe")
    
    # Verificar allure-results
    allure_dir = "allure-results"
    if os.path.exists(allure_dir):
        files_count = len(os.listdir(allure_dir))
        print(f"📁 Allure-results: {files_count} archivos")
    else:
        print("❌ Allure-results no existe")
    
    # Verificar screenshots
    screenshots_dir = "screenshots"
    if os.path.exists(screenshots_dir):
        screenshots_count = len(os.listdir(screenshots_dir))
        print(f"📸 Screenshots: {screenshots_count} archivos")
    else:
        print("❌ Screenshots no existe")

if __name__ == "__main__":
    print("🚀 INICIANDO LIMPIEZA COMPLETA...")
    
    # Ejecutar limpieza
    reset_database_completely()
    clean_allure_results()
    clean_screenshots()
    
    # Verificar estado
    verify_clean_state()
    
    print("\n🎯 ¡LIMPIEZA COMPLETADA!")
    print("💡 Ahora ejecuta: pytest tests/test_case_4.py -v -s --alluredir=allure-results")
import os
import shutil
import glob
from datetime import datetime

def clean_everything():
    """Limpiar absolutamente todo: BD, backups, allure, screenshots"""
    
    print("🧹 LIMPIEZA COMPLETA DEL PROYECTO")
    print("=" * 50)
    
    # 1. Limpiar backups de base de datos
    print("1️⃣  LIMPIANDO BACKUPS DE BD...")
    backup_files = glob.glob("data/test_results_backup_*.db")
    for backup_file in backup_files:
        try:
            os.remove(backup_file)
            print(f"   ✅ Eliminado: {backup_file}")
        except Exception as e:
            print(f"   ❌ Error eliminando {backup_file}: {e}")
    
    print(f"   📊 Backups eliminados: {len(backup_files)}")
    
    # 2. Limpiar base de datos principal
    print("\n2️⃣  LIMPIANDO BASE DE DATOS PRINCIPAL...")
    db_files = [
        "data/test_results.db",
        "data/test_results.db-journal"  # Archivo temporal de SQLite
    ]
    
    for db_file in db_files:
        if os.path.exists(db_file):
            try:
                os.remove(db_file)
                print(f"   ✅ Eliminado: {db_file}")
            except Exception as e:
                print(f"   ❌ Error eliminando {db_file}: {e}")
        else:
            print(f"   ⚠️  No existe: {db_file}")
    
    # 3. Limpiar allure-results
    print("\n3️⃣  LIMPIANDO ALLURE-RESULTS...")
    allure_dir = "allure-results"
    if os.path.exists(allure_dir):
        try:
            shutil.rmtree(allure_dir)
            print(f"   ✅ Eliminado: {allure_dir}/")
        except Exception as e:
            print(f"   ❌ Error eliminando {allure_dir}: {e}")
    else:
        print(f"   ⚠️  No existe: {allure_dir}/")
    
    # 4. Limpiar screenshots
    print("\n4️⃣  LIMPIANDO SCREENSHOTS...")
    screenshots_dir = "screenshots"
    if os.path.exists(screenshots_dir):
        try:
            shutil.rmtree(screenshots_dir)
            print(f"   ✅ Eliminado: {screenshots_dir}/")
        except Exception as e:
            print(f"   ❌ Error eliminando {screenshots_dir}: {e}")
    else:
        print(f"   ⚠️  No existe: {screenshots_dir}/")
    
    # 5. Limpiar reportes HTML
    print("\n5️⃣  LIMPIANDO REPORTES HTML...")
    html_reports = glob.glob("reports/*.html")
    for html_file in html_reports:
        try:
            os.remove(html_file)
            print(f"   ✅ Eliminado: {html_file}")
        except Exception as e:
            print(f"   ❌ Error eliminando {html_file}: {e}")
    
    print(f"   📊 Reportes HTML eliminados: {len(html_reports)}")
    
    # 6. Recrear estructura necesaria
    print("\n6️⃣  CREANDO ESTRUCTURA NUEVA...")
    folders_to_create = ["data", "allure-results", "screenshots", "reports"]
    
    for folder in folders_to_create:
        try:
            os.makedirs(folder, exist_ok=True)
            print(f"   ✅ Creado: {folder}/")
        except Exception as e:
            print(f"   ❌ Error creando {folder}: {e}")
    
    # 7. Verificación final
    print("\n7️⃣  VERIFICACIÓN FINAL:")
    verify_clean_state()
    
    print("\n🎯 ¡LIMPIEZA COMPLETADA!")
    print("💡 Ahora tienes un proyecto completamente limpio")

def verify_clean_state():
    """Verificar que todo está limpio"""
    print("   🔍 Verificando estado...")
    
    # Verificar data/
    data_files = os.listdir("data") if os.path.exists("data") else []
    data_count = len([f for f in data_files if f.endswith('.db')])
    print(f"   📊 Archivos .db en data/: {data_count}")
    
    # Verificar allure-results/
    allure_files = os.listdir("allure-results") if os.path.exists("allure-results") else []
    print(f"   📁 Archivos en allure-results/: {len(allure_files)}")
    
    # Verificar screenshots/
    screenshot_files = os.listdir("screenshots") if os.path.exists("screenshots") else []
    print(f"   📸 Archivos en screenshots/: {len(screenshot_files)}")
    
    # Verificar reports/
    report_files = os.listdir("reports") if os.path.exists("reports") else []
    html_reports = [f for f in report_files if f.endswith('.html')]
    print(f"   📄 Reportes HTML en reports/: {len(html_reports)}")
    
    total_files = data_count + len(allure_files) + len(screenshot_files) + len(html_reports)
    print(f"   🎯 TOTAL archivos de datos: {total_files}")
    
    if total_files == 0:
        print("   ✅ ¡PROYECTO COMPLETAMENTE LIMPIO!")
    else:
        print("   ⚠️  Aún hay archivos de datos")

if __name__ == "__main__":
    clean_everything()
    
    print("\n" + "=" * 50)
    print("🚀 INSTRUCCIONES PARA PRUEBAS FRESCAS:")
    print("=" * 50)
    print("1. Ejecutar pruebas: pytest tests/test_case_4.py -v -s --alluredir=allure-results")
    print("2. Verificar BD: python -c \"from utils.database import DatabaseManager; db = DatabaseManager(); print(f'Registros: {len(db.get_test_results())}')\"")
    print("3. Generar reporte: C:\\allure\\allure-2.35.1\\bin\\allure.bat serve allure-results")
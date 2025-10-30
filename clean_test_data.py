import os
import sqlite3
import shutil

def clean_all_test_data():
    """Limpiar todos los datos de pruebas anteriores"""
    
    print("🧹 LIMPIANDO DATOS DE PRUEBAS ANTERIORES...")
    print("=" * 50)
    
    # 1. Limpiar base de datos
    print("1️⃣  LIMPIANDO BASE DE DATOS...")
    db_path = "data/test_results.db"
    
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Eliminar todos los registros pero mantener la estructura
            cursor.execute("DELETE FROM test_results")
            cursor.execute("DELETE FROM test_stats")
            
            # Reiniciar los autoincrementos
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='test_results'")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='test_stats'")
            
            conn.commit()
            conn.close()
            
            print("✅ Base de datos limpiada - Todos los registros eliminados")
            
            # Verificar que está vacía
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM test_results")
            count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM test_stats") 
            stats_count = cursor.fetchone()[0]
            conn.close()
            
            print(f"   📊 Registros en test_results: {count}")
            print(f"   📊 Registros en test_stats: {stats_count}")
            
        except Exception as e:
            print(f"❌ Error limpiando base de datos: {e}")
    else:
        print("⚠️  Base de datos no encontrada, se creará nueva")
    
    # 2. Limpiar carpeta de allure-results
    print("\n2️⃣  LIMPIANDO ALLURE-RESULTS...")
    allure_dir = "allure-results"
    
    if os.path.exists(allure_dir):
        try:
            # Eliminar todo el contenido pero mantener la carpeta
            for filename in os.listdir(allure_dir):
                file_path = os.path.join(allure_dir, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"❌ Error eliminando {file_path}: {e}")
            
            print("✅ Carpeta allure-results limpiada")
            print(f"   📁 Archivos en allure-results: {len(os.listdir(allure_dir))}")
            
        except Exception as e:
            print(f"❌ Error limpiando allure-results: {e}")
    else:
        print("⚠️  Carpeta allure-results no encontrada, se creará nueva")
    
    # 3. Limpiar screenshots (opcional)
    print("\n3️⃣  LIMPIANDO SCREENSHOTS...")
    screenshots_dir = "screenshots"
    
    if os.path.exists(screenshots_dir):
        try:
            # Eliminar solo los archivos .png, mantener la carpeta
            png_files = [f for f in os.listdir(screenshots_dir) if f.endswith('.png')]
            for filename in png_files:
                file_path = os.path.join(screenshots_dir, filename)
                os.unlink(file_path)
            
            print(f"✅ Screenshots limpiados - {len(png_files)} archivos eliminados")
            print(f"   📸 Archivos en screenshots: {len(os.listdir(screenshots_dir))}")
            
        except Exception as e:
            print(f"❌ Error limpiando screenshots: {e}")
    else:
        print("⚠️  Carpeta screenshots no encontrada, se creará nueva")
    
    # 4. Verificación final
    print("\n4️⃣  VERIFICACIÓN FINAL:")
    print("   ✅ Base de datos: lista para nuevos registros")
    print("   ✅ Allure-results: lista para nuevos reportes") 
    print("   ✅ Screenshots: lista para nuevas capturas")
    print("\n🎯 Ahora puedes ejecutar pruebas frescas:")
    print("   pytest tests/test_case_4.py -v -s --alluredir=allure-results")

if __name__ == "__main__":
    clean_all_test_data()
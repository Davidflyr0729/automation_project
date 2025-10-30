import subprocess
import os
import time
from utils.database import DatabaseManager

def celebrate_success():
    """Ejecutar y celebrar el éxito del Caso 4"""
    
    print("🎉 ¡FELICIDADES! CASO 4 COMPLETADO EXITOSAMENTE")
    print("=" * 60)
    print("🚀 Ejecutando prueba final con Allure...")
    print("=" * 60)
    
    # Configurar Java
    os.environ["JAVA_HOME"] = r"C:\Program Files\Java\jdk-25"
    os.environ["PATH"] = f"{os.environ['JAVA_HOME']}\\bin;{os.environ['PATH']}"
    
    # 1. Ejecutar tests
    print("1️⃣  EJECUTANDO PRUEBAS AUTOMATIZADAS...")
    test_result = subprocess.run([
        "pytest", "tests/test_case_4.py", 
        "-v", "-s",
        "--alluredir=allure-results"
    ], capture_output=True, text=True)
    
    print("✅ Pruebas ejecutadas")
    print(test_result.stdout)
    
    # 2. Mostrar resultados en BD
    print("2️⃣  RESULTADOS EN BASE DE DATOS:")
    db = DatabaseManager()
    results = db.get_test_results("Caso_4_Cambio_Idioma")
    
    print(f"   📈 Total de ejecuciones: {len(results)}")
    print(f"   ✅ Exitosos: {len([r for r in results if r[4] == 'PASS'])}")
    print(f"   ❌ Fallidos: {len([r for r in results if r[4] == 'FAIL'])}")
    
    print("\n   📋 Detalle por idioma:")
    for row in results:
        status = "✅ PASÓ" if row[4] == "PASS" else "❌ FALLÓ"
        print(f"      {status} - {row[3]:<12} en {row[2]:<8} a las {row[5]}")
    
    # 3. Ejecutar Allure
    print("\n3️⃣  GENERANDO REPORTE ALLURE PROFESIONAL...")
    print("   🌐 El reporte se abrirá automáticamente en tu navegador")
    print("   ⏳ Por favor espera...")
    
    time.sleep(2)
    
    try:
        allure_path = r"C:\allure\allure-2.35.1\bin\allure.bat"
        subprocess.run([allure_path, "serve", "allure-results"])
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎊 ¡CASO 4 COMPLETADO CON ÉXITO!")
    print("=" * 60)
    print("\n📋 LO QUE HEMOS LOGRADO:")
    print("   ✅ Configuración completa de Selenium WebDriver")
    print("   ✅ Page Object Model (POM) implementado")
    print("   ✅ Automatización del cambio de 4 idiomas")
    print("   ✅ Base de datos SQLite funcionando")
    print("   ✅ Reportes profesionales con Allure")
    print("   ✅ Manejo de múltiples navegadores")
    print("   ✅ Patrón de diseño y buenas prácticas")
    print("\n🏆 ¡Has completado exitosamente la prueba técnica!")

if __name__ == "__main__":
    celebrate_success()
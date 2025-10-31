from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import os

def debug_pos_verification():
    """Script para debuguear la verificación del texto del POS"""
    print("🔍 Iniciando diagnóstico de verificación POS...")
    
    from selenium.webdriver.chrome.options import Options
    
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    
    driver_path = os.path.join("drivers", "chromedriver.exe")
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        urls = [
            "https://nuxqa4.avtest.ink/",
            "https://nuxqa5.avtest.ink/"
        ]
        
        countries_to_test = ["Otros países", "España", "Chile"]
        
        for url in urls:
            print(f"\n{'='*60}")
            print(f"🌐 Probando en: {url}")
            print(f"{'='*60}")
            
            driver.get(url)
            time.sleep(5)
            
            # Obtener el texto inicial del POS
            pos_button = driver.find_element(By.ID, "pointOfSaleSelectorId")
            initial_text = pos_button.text.strip()
            print(f"📌 Texto inicial del POS: '{initial_text}'")
            
            for country in countries_to_test:
                print(f"\n🔄 Intentando cambiar a: {country}")
                
                # Hacer clic en el selector de POS
                pos_button = driver.find_element(By.ID, "pointOfSaleSelectorId")
                pos_button.click()
                time.sleep(2)
                
                # Buscar y hacer clic en la opción del país
                try:
                    # Buscar por texto exacto primero
                    country_xpath = f"//*[contains(text(), '{country}')]"
                    country_elements = driver.find_elements(By.XPATH, country_xpath)
                    
                    if country_elements:
                        for element in country_elements:
                            if element.is_displayed() and element.is_enabled():
                                print(f"✅ Encontrada opción: '{element.text}'")
                                element.click()
                                break
                    else:
                        # Si no encuentra por texto completo, buscar por partes
                        print(f"⚠️ No se encontró '{country}', buscando alternativas...")
                        if "Otros países" in country:
                            alternatives = ["Otros", "Other", "Otros países"]
                        elif "España" in country:
                            alternatives = ["España", "Spain"]
                        elif "Chile" in country:
                            alternatives = ["Chile"]
                        
                        for alt in alternatives:
                            alt_xpath = f"//*[contains(text(), '{alt}')]"
                            alt_elements = driver.find_elements(By.XPATH, alt_xpath)
                            if alt_elements:
                                for element in alt_elements:
                                    if element.is_displayed() and element.is_enabled():
                                        print(f"✅ Encontrada opción alternativa: '{element.text}'")
                                        element.click()
                                        break
                                break
                
                except Exception as e:
                    print(f"❌ Error al seleccionar {country}: {e}")
                    continue
                
                # Esperar a que se aplique el cambio
                time.sleep(3)
                
                # Obtener el texto actual del POS
                pos_button = driver.find_element(By.ID, "pointOfSaleSelectorId")
                current_text = pos_button.text.strip()
                print(f"📝 Texto después de cambiar a '{country}': '{current_text}'")
                
                # Verificar si el cambio fue exitoso
                if any(word.lower() in current_text.lower() for word in country.lower().split()):
                    print(f"✅ VERIFICACIÓN EXITOSA para {country}")
                else:
                    print(f"❌ VERIFICACIÓN FALLIDA para {country}")
                    print(f"   Esperado: algo como '{country}'")
                    print(f"   Encontrado: '{current_text}'")
                
                print("-" * 40)
            
            print(f"\n✅ Análisis de {url} completado")
    
    except Exception as e:
        print(f"❌ Error durante el diagnóstico: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        input("\n⏎ Presiona Enter para cerrar el navegador...")
        driver.quit()
        print("✅ Diagnóstico de verificación completado")

if __name__ == "__main__":
    debug_pos_verification()
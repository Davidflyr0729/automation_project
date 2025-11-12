import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Debug Detallado Login")
class TestDebugLoginDetailed:
    
    def test_debug_login_detailed(self, driver):
        """Debug detallado del proceso de login"""
        
        print("\n" + "="*60)
        print("🔍 INICIANDO DEBUG DETALLADO DEL LOGIN")
        print("="*60)
        
        with allure.step("1. Navegar a la página principal"):
            driver.get("https://nuxqa3.avtest.ink/es/")
            time.sleep(3)
            print("✅ Página principal cargada")
            print(f"📍 URL: {driver.current_url}")
            
        with allure.step("2. Tomar captura inicial"):
            allure.attach(
                driver.get_screenshot_as_png(),
                name="debug_1_pagina_principal",
                attachment_type=allure.attachment_type.PNG
            )
            
        with allure.step("3. Buscar botón de login"):
            try:
                login_button = driver.find_element(By.ID, "auth-component")
                print(f"✅ Botón encontrado: '{login_button.text}'")
                print(f"📍 Visible: {login_button.is_displayed()}")
                print(f"📍 Habilitado: {login_button.is_enabled()}")
                print(f"📍 Ubicación: {login_button.location}")
                print(f"📍 Tamaño: {login_button.size}")
            except Exception as e:
                print(f"❌ No se pudo encontrar el botón: {e}")
                return
                
        with allure.step("4. Hacer clic en el botón"):
            login_button.click()
            print("✅ Clic realizado en 'Iniciar sesión'")
            time.sleep(5)  # Esperar generosamente
            
        with allure.step("5. Verificar estado después del clic"):
            print(f"📍 URL después del clic: {driver.current_url}")
            
        with allure.step("6. Buscar iframes"):
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            print(f"🔍 Iframes encontrados: {len(iframes)}")
            
            for i, iframe in enumerate(iframes):
                print(f"\n--- Iframe {i+1} ---")
                print(f"📍 ID: {iframe.get_attribute('id')}")
                print(f"📍 Clase: {iframe.get_attribute('class')}")
                print(f"📍 SRC: {iframe.get_attribute('src')}")
                print(f"📍 Visible: {iframe.is_displayed()}")
                print(f"📍 Tamaño: {iframe.size}")
                
        with allure.step("7. Probar cada iframe"):
            for i, iframe in enumerate(iframes):
                print(f"\n🎯 PROBANDO IFRAME {i+1}")
                try:
                    # Cambiar al iframe
                    driver.switch_to.frame(iframe)
                    print(f"  ✅ Cambiado al iframe {i+1}")
                    
                    # Buscar elementos dentro del iframe
                    elementos_buscar = [
                        ("u-username", "Campo usuario"),
                        ("u-password", "Campo contraseña"),
                        ("Login-confirm", "Botón login")
                    ]
                    
                    for id_elemento, nombre in elementos_buscar:
                        try:
                            elemento = driver.find_element(By.ID, id_elemento)
                            print(f"  ✅ {nombre} ENCONTRADO en iframe {i+1}")
                            print(f"     📍 Visible: {elemento.is_displayed()}")
                            print(f"     📍 Habilitado: {elemento.is_enabled()}")
                            print(f"     📍 Tipo: {elemento.get_attribute('type')}")
                            print(f"     📍 Placeholder: {elemento.get_attribute('placeholder')}")
                            
                            # Intentar interactuar
                            try:
                                elemento.click()
                                print(f"  ✅ CLIC exitoso en {nombre}")
                                time.sleep(1)
                                
                                # Intentar enviar texto
                                if id_elemento == "u-username":
                                    elemento.send_keys("21734198706")
                                    valor = elemento.get_attribute('value')
                                    print(f"  ✅ TEXTO INGRESADO: '{valor}'")
                                    
                            except Exception as e:
                                print(f"  ❌ Error interactuando con {nombre}: {e}")
                                
                        except Exception as e:
                            print(f"  ❌ {nombre} NO encontrado en iframe {i+1}")
                    
                    # Volver al contexto principal
                    driver.switch_to.default_content()
                    print(f"  🔄 Vuelto al contexto principal desde iframe {i+1}")
                    
                except Exception as e:
                    print(f"  ❌ Error en iframe {i+1}: {e}")
                    driver.switch_to.default_content()
                    
        with allure.step("8. Buscar elementos en contexto principal"):
            print("\n🔍 BUSCANDO ELEMENTOS EN CONTEXTO PRINCIPAL:")
            elementos_principales = [
                ("u-username", "Campo usuario"),
                ("u-password", "Campo contraseña"), 
                ("Login-confirm", "Botón login"),
                ("auth-component", "Botón principal login")
            ]
            
            for id_elemento, nombre in elementos_principales:
                try:
                    elementos = driver.find_elements(By.ID, id_elemento)
                    if elementos:
                        print(f"✅ {nombre} encontrado en contexto principal: {len(elementos)} elementos")
                        for elem in elementos:
                            print(f"   📍 Visible: {elem.is_displayed()}")
                            print(f"   📍 Texto: '{elem.text}'")
                    else:
                        print(f"❌ {nombre} NO encontrado en contexto principal")
                except Exception as e:
                    print(f"⚠️ Error buscando {nombre}: {e}")
                    
        with allure.step("9. Tomar captura final"):
            allure.attach(
                driver.get_screenshot_as_png(),
                name="debug_final_estado",
                attachment_type=allure.attachment_type.PNG
            )
            
        with allure.step("10. Debug completado"):
            print("\n" + "="*60)
            print("🎉 DEBUG COMPLETADO")
            print("📊 Revisa los logs para entender el problema")
            print("="*60)
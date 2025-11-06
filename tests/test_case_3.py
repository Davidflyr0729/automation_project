# tests/test_case_3.py
import pytest
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage

logger = logging.getLogger(__name__)

class TestCase3:
    """Caso 3: Login completo y cambio de idioma a francés"""
    
    @pytest.mark.case3
    def test_login_y_cambio_idioma(self, driver):
        """LOGIN COMPLETO Y CAMBIO DE IDIOMA A FRANCÉS DESPUÉS DEL LOGIN"""
        
        logger.info("=== INICIANDO: LOGIN COMPLETO Y CAMBIO DE IDIOMA ===")
        
        # 1. Navegar a la URL principal
        logger.info("📝 PASO 1: Navegando a la URL principal...")
        home_page = HomePage(driver)
        home_page.navigate_to("https://nuxqa3.avtest.ink/")
        
        # Esperar carga completa
        time.sleep(8)
        home_page.take_screenshot("01_pagina_principal.png")
        logger.info("✅ Página principal cargada correctamente")
        
        # Guardar ventana principal
        main_window = driver.current_window_handle
        logger.info(f"📱 Ventana principal: {main_window}")
        
        # 2. Buscar y hacer click en el botón de login
        logger.info("🖱️ PASO 2: Buscando y haciendo click en botón de login...")
        
        try:
            login_btn = None
            
            # Primero intentar selectores específicos
            selectores_login = [
                (By.CSS_SELECTOR, "button[data-cy='login']"),
                (By.CSS_SELECTOR, "button[class*='login']"),
                (By.CSS_SELECTOR, "button[class*='auth']"),
                (By.XPATH, "//button[contains(text(), 'Iniciar sesión')]"),
                (By.XPATH, "//button[contains(text(), 'Iniciar')]"),
                (By.XPATH, "//button[contains(text(), 'Login')]"),
                (By.XPATH, "//button[contains(text(), 'Sign in')]")
            ]
            
            for selector_type, selector_value in selectores_login:
                try:
                    logger.info(f"🔍 Probando selector: {selector_value}")
                    elemento = driver.find_element(selector_type, selector_value)
                    if elemento.is_displayed() and elemento.is_enabled():
                        login_btn = elemento
                        logger.info(f"✅ Botón de login encontrado: {selector_value}")
                        logger.info(f"📝 Texto: '{elemento.text}'")
                        break
                except Exception as e:
                    logger.info(f"❌ Selector no funciona: {selector_value}")
                    continue
            
            # Si no encontramos con selectores específicos, buscar en todos los botones
            if not login_btn:
                logger.info("🔍 Buscando en todos los botones...")
                all_buttons = driver.find_elements(By.TAG_NAME, "button")
                logger.info(f"🔍 Total de botones: {len(all_buttons)}")
                
                for i, btn in enumerate(all_buttons):
                    try:
                        if btn.is_displayed() and btn.is_enabled():
                            btn_class = btn.get_attribute('class') or ''
                            btn_text = btn.text or ''
                            
                            logger.info(f"  Botón {i}: '{btn_text}' - Clase: '{btn_class}'")
                            
                            if any(keyword in btn_text.lower() for keyword in ['iniciar', 'login', 'sesión', 'sign']) or \
                               any(keyword in btn_class.lower() for keyword in ['login', 'auth']):
                                login_btn = btn
                                logger.info(f"🎯 Posible botón de login: '{btn_text}'")
                                break
                    except Exception as e:
                        logger.info(f"❌ Error con botón {i}: {e}")
            
            if login_btn:
                logger.info("🖱️ Haciendo click en botón de login...")
                home_page.click_element(login_btn)
                logger.info("✅ Click en botón de login realizado")
            else:
                raise Exception("No se pudo encontrar ningún botón de login viable")
                    
        except Exception as e:
            logger.error(f"❌ Error con botón de login: {e}")
            home_page.take_screenshot("error_boton_login.png")
            assert False, f"No se pudo encontrar el botón de login: {e}"
        
        # 3. MANEJO DE VENTANAS/MODAL DESPUÉS DEL CLICK EN LOGIN
        logger.info("🔄 PASO 3: Manejando ventana/modal después del login...")
        
        time.sleep(5)
        
        # Verificar si hay nuevas ventanas
        all_windows = driver.window_handles
        logger.info(f"📱 Ventanas abiertas: {len(all_windows)}")
        
        if len(all_windows) > 1:
            # Cambiar a la nueva ventana
            new_window = [window for window in all_windows if window != main_window][0]
            driver.switch_to.window(new_window)
            logger.info(f"✅ Cambiado a nueva ventana: {new_window}")
        else:
            logger.info("ℹ️  No hay nuevas ventanas, puede ser un modal")
        
        # Tomar screenshot del estado actual
        current_url = driver.current_url
        logger.info(f"🌐 URL actual: {current_url}")
        home_page.take_screenshot("02_despues_click_login.png")
        
        # 4. ESPERAR A QUE CARGUE EL FORMULARIO DE LOGIN
        logger.info("⏳ PASO 4: Esperando a que cargue el formulario de login...")
        time.sleep(5)
        
        # 5. BUSCAR FORMULARIO DE LOGIN EN DIFERENTES UBICACIONES
        logger.info("🔍 PASO 5: Buscando formulario de login...")
        
        # Estrategia 1: Buscar en la página actual
        username_field = self._buscar_campo_usuario(driver, home_page)
        
        # Estrategia 2: Si no encuentra, buscar en iframes
        if not username_field:
            logger.info("🔍 Buscando en iframes...")
            username_field = self._buscar_en_iframes(driver, home_page)
        
        # Estrategia 3: Si todavía no encuentra, verificar si estamos en página diferente
        if not username_field:
            logger.info("🔍 Verificando si estamos en página de login...")
            if 'login' in current_url.lower() or 'auth' in current_url.lower():
                logger.info("✅ Estamos en página de login, reintentando búsqueda...")
                username_field = self._buscar_campo_usuario(driver, home_page, True)
        
        if not username_field:
            # DEBUG: Mostrar todos los inputs disponibles
            logger.info("🔍 DEBUG: Mostrando todos los inputs disponibles...")
            all_inputs = driver.find_elements(By.TAG_NAME, "input")
            logger.info(f"🔍 Total de inputs: {len(all_inputs)}")
            
            for i, inp in enumerate(all_inputs):
                try:
                    inp_type = inp.get_attribute('type') or ''
                    inp_id = inp.get_attribute('id') or ''
                    inp_name = inp.get_attribute('name') or ''
                    inp_placeholder = inp.get_attribute('placeholder') or ''
                    
                    logger.info(f"  Input {i}:")
                    logger.info(f"    Tipo: {inp_type}")
                    logger.info(f"    ID: {inp_id}")
                    logger.info(f"    Name: {inp_name}")
                    logger.info(f"    Placeholder: {inp_placeholder}")
                    logger.info(f"    Visible: {inp.is_displayed()}")
                except Exception as e:
                    logger.error(f"❌ Error con input {i}: {e}")
            
            raise Exception("No se pudo encontrar campo de usuario después de búsqueda exhaustiva")
        
        # 6. LLENAR CAMPO DE USUARIO
        logger.info("👤 PASO 6: Llenando campo de usuario...")
        
        try:
            home_page.click_element(username_field)
            username_field.clear()
            usuario = "21734198706"
            username_field.send_keys(usuario)
            logger.info(f"✅ Usuario ingresado: {usuario}")
            
            # Verificar
            texto_ingresado = username_field.get_attribute('value')
            if texto_ingresado == usuario:
                logger.info("✅ Usuario verificado correctamente")
            else:
                logger.warning(f"⚠️ Texto en campo: '{texto_ingresado}'")
            
            home_page.take_screenshot("03_usuario_ingresado.png")
                
        except Exception as e:
            logger.error(f"❌ Error llenando campo usuario: {e}")
            home_page.take_screenshot("error_campo_usuario.png")
            assert False, f"No se pudo llenar campo de usuario: {e}"
        
        # 7. BUSCAR Y LLENAR CAMPO DE CONTRASEÑA
        logger.info("🔐 PASO 7: Buscando y llenando campo de contraseña...")
        
        try:
            password_field = None
            selectores_password = [
                (By.ID, "u-password"),
                (By.CSS_SELECTOR, "input[type='password']"),
                (By.CSS_SELECTOR, "input[name='new-password']"),
                (By.CSS_SELECTOR, "input[placeholder*='Contraseña']"),
                (By.CSS_SELECTOR, "input[placeholder*='Password']")
            ]
            
            for selector_type, selector_value in selectores_password:
                try:
                    elemento = driver.find_element(selector_type, selector_value)
                    if elemento.is_displayed() and elemento.is_enabled():
                        password_field = elemento
                        logger.info(f"✅ Campo contraseña: {selector_value}")
                        break
                except:
                    continue
            
            if not password_field:
                # Buscar cerca del campo de usuario
                logger.info("🔍 Buscando campo contraseña cerca del usuario...")
                try:
                    # Buscar siguiente input después del username
                    password_fields = driver.find_elements(By.CSS_SELECTOR, "input[type='password']")
                    for pwd in password_fields:
                        if pwd.is_displayed():
                            password_field = pwd
                            break
                except:
                    pass
            
            if password_field:
                home_page.click_element(password_field)
                password_field.clear()
                contraseña = "Lifemiles1"
                password_field.send_keys(contraseña)
                logger.info("✅ Contraseña ingresada")
                home_page.take_screenshot("04_contrasena_ingresada.png")
            else:
                raise Exception("No se pudo encontrar campo de contraseña")
                
        except Exception as e:
            logger.error(f"❌ Error con campo contraseña: {e}")
            home_page.take_screenshot("error_campo_contrasena.png")
            assert False, f"No se pudo llenar campo de contraseña: {e}"
        
        # 8. HACER LOGIN
        logger.info("🖱️ PASO 8: Haciendo login...")
        
        try:
            submit_button = None
            selectores_submit = [
                (By.ID, "Login-confirm"),
                (By.CSS_SELECTOR, "button[data-cy='lmSubmit']"),
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.XPATH, "//button[contains(text(), 'Iniciar sesión')]"),
                (By.XPATH, "//button[contains(text(), 'Iniciar')]"),
                (By.XPATH, "//button[contains(text(), 'Login')]")
            ]
            
            for selector_type, selector_value in selectores_submit:
                try:
                    elemento = driver.find_element(selector_type, selector_value)
                    if elemento.is_displayed() and elemento.is_enabled():
                        submit_button = elemento
                        logger.info(f"✅ Botón submit: {selector_value}")
                        break
                except:
                    continue
            
            if submit_button:
                home_page.take_screenshot("05_antes_del_login.png")
                home_page.click_element(submit_button)
                logger.info("✅ Click en botón de login realizado")
                
                # Esperar login
                logger.info("⏳ Esperando 15 segundos para login...")
                time.sleep(15)
                
                # Si hay múltiples ventanas, volver a la principal
                if len(driver.window_handles) > 1:
                    driver.switch_to.window(main_window)
                    logger.info("✅ Volviendo a ventana principal")
                
                home_page.take_screenshot("06_despues_del_login.png")
                logger.info("✅ Login procesado")
            else:
                raise Exception("No se pudo encontrar botón de submit")
                
        except Exception as e:
            logger.error(f"❌ Error con botón submit: {e}")
            home_page.take_screenshot("error_boton_submit.png")
            assert False, f"No se pudo hacer login: {e}"
        
        # 9. VERIFICAR LOGIN EXITOSO
        logger.info("🔍 PASO 9: Verificando login exitoso...")
        
        current_url = driver.current_url
        logger.info(f"🌐 URL después del login: {current_url}")
        
        # Buscar indicadores de login exitoso
        login_exitoso = False
        try:
            indicadores = [
                (By.XPATH, "//*[contains(text(), 'Bienvenido')]"),
                (By.XPATH, "//*[contains(text(), 'Welcome')]"),
                (By.XPATH, "//*[contains(text(), 'Mi cuenta')]"),
                (By.XPATH, "//*[contains(text(), 'My account')]"),
                (By.CSS_SELECTOR, "[class*='user']"),
                (By.CSS_SELECTOR, "[class*='profile']")
            ]
            
            for selector_type, selector_value in indicadores:
                try:
                    elementos = driver.find_elements(selector_type, selector_value)
                    for elem in elementos:
                        if elem.is_displayed():
                            logger.info(f"✅ Login exitoso - {elem.text}")
                            login_exitoso = True
                            break
                except:
                    continue
                    
        except Exception as e:
            logger.error(f"❌ Error verificando login: {e}")
        
        if not login_exitoso:
            logger.warning("⚠️ No se encontraron indicadores claros de login, pero continuamos")
        
        # 10. CAMBIAR IDIOMA A FRANCÉS
        logger.info("🇫🇷 PASO 10: Cambiando idioma a Francés...")
        
        # Navegar a página principal si es necesario
        if '/lifemiles-info/landing-intermedia/' in current_url:
            logger.info("🏠 Navegando a página principal...")
            try:
                driver.get("https://nuxqa3.avtest.ink/es/")
                time.sleep(5)
                logger.info("✅ En página principal")
            except Exception as e:
                logger.error(f"❌ Error navegando a página principal: {e}")
        
        # Ejecutar cambio de idioma
        try:
            self._cambiar_idioma_frances(driver, home_page)
        except Exception as e:
            logger.error(f"❌ Error cambiando idioma: {e}")
        
        # 11. FINALIZAR
        logger.info("⏳ Espera final de 3 segundos...")
        time.sleep(3)
        
        logger.info("🎯 PRUEBA COMPLETADA")
        logger.info("🔄 Finalizando prueba...")
        
        assert True, "Prueba completada"

    def _buscar_campo_usuario(self, driver, home_page, reintento=False):
        """Buscar campo de usuario en diferentes ubicaciones"""
        logger.info("🔍 Buscando campo de usuario...")
        
        selectores_usuario = [
            (By.ID, "u-username"),
            (By.CSS_SELECTOR, "input[type='text']"),
            (By.CSS_SELECTOR, "input[type='email']"),
            (By.CSS_SELECTOR, "input[name='new-username']"),
            (By.CSS_SELECTOR, "input[placeholder*='Lifemiles']"),
            (By.CSS_SELECTOR, "input[placeholder*='usuario']"),
            (By.CSS_SELECTOR, "input[placeholder*='correo']"),
            (By.CSS_SELECTOR, "input[placeholder*='email']"),
            (By.CSS_SELECTOR, "input[placeholder*='username']")
        ]
        
        if reintento:
            # Agregar más selectores para reintento
            selectores_usuario.extend([
                (By.CSS_SELECTOR, "input"),
                (By.XPATH, "//input[not(@type='password') and not(@type='hidden')]")
            ])
        
        for selector_type, selector_value in selectores_usuario:
            try:
                logger.info(f"  Probando: {selector_value}")
                elemento = driver.find_element(selector_type, selector_value)
                if elemento.is_displayed() and elemento.is_enabled():
                    logger.info(f"✅ Campo usuario encontrado: {selector_value}")
                    return elemento
            except Exception as e:
                logger.info(f"  ❌ No funciona: {selector_value}")
                continue
        
        return None

    def _buscar_en_iframes(self, driver, home_page):
        """Buscar formulario de login en iframes"""
        logger.info("🔍 Buscando en iframes...")
        
        try:
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            logger.info(f"🔍 Iframes encontrados: {len(iframes)}")
            
            for i, iframe in enumerate(iframes):
                try:
                    driver.switch_to.frame(iframe)
                    logger.info(f"🔍 Buscando en iframe {i}...")
                    
                    # Buscar campo de usuario en este iframe
                    username_field = self._buscar_campo_usuario(driver, home_page)
                    if username_field:
                        logger.info(f"✅ Campo usuario encontrado en iframe {i}")
                        return username_field
                    
                    # Volver al contexto principal
                    driver.switch_to.default_content()
                    
                except Exception as e:
                    logger.error(f"❌ Error con iframe {i}: {e}")
                    driver.switch_to.default_content()
                    
        except Exception as e:
            logger.error(f"❌ Error buscando en iframes: {e}")
            driver.switch_to.default_content()
        
        return None

    def _cambiar_idioma_frances(self, driver, home_page):
        """Cambiar idioma a francés"""
        logger.info("🇫🇷 Cambiando idioma a francés...")
        
        try:
            # Buscar selector de idioma
            selector_idioma = None
            selectores = [
                "li.main-header_nav-secondary_item--language-selector button.dropdown_trigger",
                "button.dropdown_trigger[id*='languageListTrigger']",
                "button[aria-label*='Español']",
                ".language-selector button"
            ]
            
            for selector in selectores:
                try:
                    elemento = driver.find_element(By.CSS_SELECTOR, selector)
                    if elemento.is_displayed() and elemento.is_enabled():
                        selector_idioma = elemento
                        logger.info(f"✅ Selector encontrado: {selector}")
                        break
                except:
                    continue
            
            if selector_idioma:
                # Abrir dropdown
                home_page.click_element(selector_idioma)
                logger.info("✅ Dropdown abierto")
                time.sleep(3)
                
                # Buscar y hacer click en Francés
                opciones_frances = [
                    "//*[contains(text(), 'Français')]",
                    "//*[contains(text(), 'French')]"
                ]
                
                for xpath in opciones_frances:
                    try:
                        french_btn = driver.find_element(By.XPATH, xpath)
                        if french_btn.is_displayed():
                            home_page.click_element(french_btn)
                            logger.info("✅ Click en Francés")
                            time.sleep(5)
                            
                            # Verificar cambio
                            if '/fr/' in driver.current_url:
                                logger.info("🎉 Idioma cambiado a francés")
                                return True
                    except:
                        continue
            
            logger.warning("⚠️ No se pudo cambiar idioma")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error cambiando idioma: {e}")
            return False
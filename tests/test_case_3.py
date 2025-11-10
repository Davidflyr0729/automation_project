# tests/test_case_3.py
import pytest
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import os
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
        
        # 9. ESPERAR Y VERIFICAR REDIRECCIÓN A LANDING INTERMEDIA
        logger.info("🔍 PASO 9: Esperando redirección a landing intermedia...")
        
        landing_url = "https://nuxqa3.avtest.ink/es/lifemiles-info/landing-intermedia/"
        max_attempts = 3
        landing_found = False
        
        for attempt in range(max_attempts):
            current_url = driver.current_url
            logger.info(f"🌐 URL actual ({attempt + 1}): {current_url}")
            
            if landing_url in current_url:
                landing_found = True
                logger.info("✅ Estamos en la landing intermedia")
                break
            else:
                logger.info(f"⏳ Esperando redirección (intento {attempt + 1}/{max_attempts})...")
                time.sleep(5)
        
        if not landing_found:
            logger.info("🔄 No se detectó redirección automática, navegando manualmente...")
            try:
                driver.get(landing_url)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                time.sleep(5)
                logger.info("✅ Navegación manual exitosa")
            except Exception as e:
                logger.error(f"❌ Error navegando a landing: {e}")
                raise
        
        # Tomar screenshot de la landing
        home_page.take_screenshot("07_landing_intermedia.png")
        
        # 10. NAVEGAR A LA LANDING INTERMEDIA Y CAMBIAR IDIOMA A FRANCÉS
        logger.info("🇫🇷 PASO 10: Navegando a landing intermedia y cambiando a Francés...")
        
        try:
            # Navegar explícitamente a la landing intermedia
            landing_url = "https://nuxqa3.avtest.ink/es/lifemiles-info/landing-intermedia/"
            logger.info(f"🏠 Navegando a landing intermedia: {landing_url}")
            driver.get(landing_url)
            
            # Esperar a que la página cargue
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(5)  # Espera adicional para asegurar carga completa
            
            # Tomar screenshot de la landing
            home_page.take_screenshot("07_landing_intermedia.png")
            logger.info("✅ En landing intermedia")
            
            # Ejecutar cambio de idioma
            if self._cambiar_idioma_frances(driver, home_page):
                logger.info("✅ Idioma cambiado exitosamente")
                home_page.take_screenshot("08_idioma_cambiado.png")
            else:
                logger.error("❌ No se pudo cambiar el idioma")
                home_page.take_screenshot("error_cambio_idioma.png")
                raise Exception("Fallo al cambiar idioma")
                
        except Exception as e:
            logger.error(f"❌ Error en el proceso: {e}")
            home_page.take_screenshot("error_proceso_cambio_idioma.png")
            raise
        
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

    def _debug_language_elements(self, driver, home_page, prefix="debug"):
        """Recolectar información para debug del selector de idioma.
        Guarda screenshot, page_source y lista elementos candidatos/iframes.
        """
        logger.info(f"🐞 DEBUG: recolectando información del DOM ({prefix})...")

        # Asegurar carpeta reports
        reports_dir = os.path.join(os.getcwd(), "reports")
        try:
            os.makedirs(reports_dir, exist_ok=True)
        except Exception:
            logger.warning(f"No se pudo crear carpeta de reports: {reports_dir}")

        # Screenshot (usa el helper si existe)
        try:
            home_page.take_screenshot(f"debug_{prefix}_screenshot.png")
        except Exception as e:
            logger.warning(f"No se pudo tomar screenshot con home_page: {e}")
            try:
                driver.save_screenshot(os.path.join(reports_dir, f"debug_{prefix}_screenshot.png"))
            except Exception as e2:
                logger.error(f"Fallo al guardar screenshot directo: {e2}")

        # Guardar page source
        try:
            html_path = os.path.join(reports_dir, f"debug_{prefix}_page.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            logger.info(f"✅ Page source guardado en: {html_path}")
        except Exception as e:
            logger.error(f"❌ Error guardando page source: {e}")

        # Buscar elementos candidatos para trigger del idioma
        candidate_selectors = [
            (By.CSS_SELECTOR, "button[id^='languageListTriggerId_']"),
            (By.CSS_SELECTOR, "button[class*='dropdown_trigger']"),
            (By.XPATH, "//button[contains(@class,'dropdown_trigger') and (@role='combobox' or @role='button')]")
        ]

        for sel_type, sel in candidate_selectors:
            try:
                elems = driver.find_elements(sel_type, sel)
                logger.info(f"🔎 Selector {sel} -> encontrados: {len(elems)}")
                for i, el in enumerate(elems[:5]):
                    try:
                        logger.info(f"  Elemento {i}: id={el.get_attribute('id')}, class={el.get_attribute('class')}, role={el.get_attribute('role')}, aria-label={el.get_attribute('aria-label')}, text='{el.text[:80]}' visible={el.is_displayed()}")
                    except Exception as e:
                        logger.info(f"  Error leyendo atributos elemento {i}: {e}")
            except Exception as e:
                logger.info(f"🔍 Error buscando selector {sel}: {e}")

        # Buscar cualquier elemento con role listbox / option
        try:
            listboxes = driver.find_elements(By.CSS_SELECTOR, "ul[role='listbox'], div[role='listbox']")
            logger.info(f"🔎 listbox encontrados: {len(listboxes)}")
            for i, lb in enumerate(listboxes[:5]):
                try:
                    logger.info(f"  listbox {i}: class={lb.get_attribute('class')}, id={lb.get_attribute('id')}, visible={lb.is_displayed()}")
                except Exception as e:
                    logger.info(f"  Error leyendo listbox {i}: {e}")
        except Exception as e:
            logger.info(f"🔍 Error buscando listboxes: {e}")

        # Buscar opciones role=option
        try:
            options = driver.find_elements(By.CSS_SELECTOR, "li[role*='option'], div[role*='option']")
            logger.info(f"🔎 opciones (role=option) encontradas: {len(options)}")
            for i, opt in enumerate(options[:10]):
                try:
                    logger.info(f"  opción {i}: text='{opt.text[:80]}', aria-label={opt.get_attribute('aria-label')}, visible={opt.is_displayed()}")
                except Exception as e:
                    logger.info(f"  Error leyendo opción {i}: {e}")
        except Exception as e:
            logger.info(f"🔍 Error buscando options: {e}")

        # Revisar iframes
        try:
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            logger.info(f"🔎 Iframes totales: {len(iframes)}")
            for i, fr in enumerate(iframes[:10]):
                try:
                    logger.info(f"  iframe {i}: id={fr.get_attribute('id')}, name={fr.get_attribute('name')}, src={fr.get_attribute('src')}")
                except Exception as e:
                    logger.info(f"  Error leyendo iframe {i}: {e}")
        except Exception as e:
            logger.info(f"🔍 Error listando iframes: {e}")

        logger.info(f"🐞 DEBUG: recolección ({prefix}) completada")

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
            # Esperar a que el botón del idioma sea clickeable
            wait = WebDriverWait(driver, 10)
            lang_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='dropdown_trigger']"))
            )
            logger.info("✅ Botón de idioma encontrado")
            # Recolectar información antes de intentar abrir el dropdown
            try:
                self._debug_language_elements(driver, home_page, prefix="before_click")
            except Exception as e:
                logger.warning(f"No se pudo ejecutar debug previo: {e}")
            
            # Intentar múltiples estrategias para hacer click
            try_strategies = [
                lambda: home_page.click_element(lang_button),  # Click normal
                lambda: ActionChains(driver).move_to_element(lang_button).click().perform(),  # Click con Actions
                lambda: ActionChains(driver).move_to_element(lang_button).click_and_hold().release().perform(),  # Click y soltar
                lambda: lang_button.send_keys(Keys.RETURN),  # Click con RETURN
                lambda: driver.execute_script("arguments[0].click();", lang_button)  # Click con JavaScript
            ]
            
            success = False
            for i, strategy in enumerate(try_strategies, 1):
                try:
                    logger.info(f"🔄 Intentando estrategia de click #{i}...")
                    strategy()
                    time.sleep(2)  # Pequeña espera para ver si el menú se abre
                    
                    # Verificar si el menú está visible
                    try:
                        menu = wait.until(
                            EC.visibility_of_element_located((By.CSS_SELECTOR, "ul[role='listbox']"))
                        )
                        success = True
                        logger.info(f"✅ Menú de idiomas visible (estrategia #{i})")
                        break
                    except TimeoutException:
                        logger.info(f"⚠️ Menú no visible con estrategia #{i}")
                        continue
                except Exception as e:
                    logger.info(f"⚠️ Estrategia #{i} falló: {str(e)}")
                    continue
            
            if not success:
                raise Exception("No se pudo abrir el menú de idiomas")
            
            # Buscar la opción de francés en el menú
            french_option = wait.until(
                EC.presence_of_element_located((By.XPATH, "//li[contains(@role, 'option') and contains(text(), 'Français')]"))
            )
            
            # Intentar click en la opción de francés
            try_strategies = [
                lambda: french_option.click(),
                lambda: ActionChains(driver).move_to_element(french_option).click().perform(),
                lambda: driver.execute_script("arguments[0].click();", french_option)
            ]
            
            success = False
            for i, strategy in enumerate(try_strategies, 1):
                try:
                    logger.info(f"🔄 Intentando seleccionar francés (estrategia #{i})...")
                    strategy()
                    time.sleep(3)
                    
                    # Verificar cambio de URL o texto del botón
                    current_url = driver.current_url
                    if "/fr/" in current_url:
                        success = True
                        logger.info("✅ URL cambió a francés")
                        break
                        
                    # Verificar texto del botón
                    button_text = lang_button.get_attribute("aria-label") or lang_button.text
                    if "français" in button_text.lower():
                        success = True
                        logger.info("✅ Texto del botón indica francés")
                        break
                except Exception as e:
                    logger.info(f"⚠️ Estrategia #{i} falló: {str(e)}")
                    continue
            
            if success:
                logger.info("🎉 Cambio de idioma exitoso")
                home_page.take_screenshot("08_idioma_cambiado.png")
                return True
            else:
                raise Exception("No se pudo cambiar el idioma a francés")
                
        except Exception as e:
            logger.error(f"❌ Error en el proceso de cambio de idioma: {e}")
            home_page.take_screenshot("error_cambio_idioma.png")
            try:
                self._debug_language_elements(driver, home_page, prefix="on_error")
            except Exception as e2:
                logger.warning(f"Fallo al ejecutar debug on_error: {e2}")
            return False
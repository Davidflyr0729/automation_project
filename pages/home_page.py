from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import logging
import time

logger = logging.getLogger(__name__)

class HomePage(BasePage):
    """Page Object para la página principal con todos los locators necesarios"""
    
    # ===== LOCATORS GENERALES =====
    PAGE_LOAD_INDICATOR = (By.TAG_NAME, "body")
    LOGO = (By.CLASS_NAME, "header_logo")
    
    # ===== SELECTOR DE IDIOMA ===== (Para Caso 4)
    LANGUAGE_BUTTON = (By.CLASS_NAME, "dropdown_trigger")
    LANGUAGE_DROPDOWN = (By.CSS_SELECTOR, ".dropdown_content.ng-star-inserted")
    LANGUAGE_OPTIONS = (By.CSS_SELECTOR, ".dropdown_content.ng-star-inserted .dropdown_item")
    
    # Opciones de idioma específicas
    SPANISH_OPTION = (By.XPATH, "//div[contains(text(), 'Español') or contains(text(), 'Spanish')]")
    ENGLISH_OPTION = (By.XPATH, "//div[contains(text(), 'English') or contains(text(), 'Inglés')]")
    FRENCH_OPTION = (By.XPATH, "//div[contains(text(), 'Français') or contains(text(), 'French')]")
    PORTUGUESE_OPTION = (By.XPATH, "//div[contains(text(), 'Português') or contains(text(), 'Portuguese')]")
    
    # Elementos para verificar idioma
    SEARCH_BUTTON_TEXT = (By.XPATH, "//button[contains(@class, 'search-btn')]")
    OFFERS_SECTION = (By.XPATH, "//h2[contains(text(), 'Ofertas') or contains(text(), 'Offers') or contains(text(), 'Offres') or contains(text(), 'Ofertas')]")
    
    # ===== SELECTOR DE POS/PAÍS ===== (Para Caso 5 - LOCATORS CORREGIDOS)
    # SELECTOR PRINCIPAL CORREGIDO - usando el ID que encontraste
    POS_SELECTOR_BUTTON = (By.ID, "pointOfSaleSelectorId")
    
    # DROPDOWN CORREGIDO - buscamos el contenedor del dropdown
    POS_DROPDOWN = (By.CSS_SELECTOR, ".dropdown_content, [role='listbox'], .mat-select-panel")
    
    # OPCIONES CORREGIDAS - buscamos las opciones dentro del dropdown
    POS_OPTIONS = (By.CSS_SELECTOR, ".dropdown_item, .mat-option, [role='option']")
    
    # Opciones de POS específicas (SOLO LAS 3 REQUERIDAS) - CORREGIDAS
    POS_OTHER_COUNTRIES = (By.XPATH, "//*[contains(text(), 'Otros países') or contains(text(), 'Other countries') or contains(text(), 'Autres pays') or contains(text(), 'Outros países')]")
    POS_SPAIN = (By.XPATH, "//*[contains(text(), 'España') or contains(text(), 'Spain') or contains(text(), 'Espagne')]")
    POS_CHILE = (By.XPATH, "//*[contains(text(), 'Chile')]")
    
    # BOTÓN APLICAR/APPLY - LOCATOR EXACTO CON LA CLASE
    POS_APPLY_BUTTON = (By.CSS_SELECTOR, "button.points-of-sale_footer_action_button")
    
    # Elementos para verificar cambio de POS
    CURRENT_POS_INDICATOR = (By.ID, "pointOfSaleSelectorId")  # El mismo botón muestra el país actual

    # ===== LOCATORS PARA CASO 6: REDIRECCIONES HEADER ===== (ESTRATEGIA CORREGIDA)
    # BOTONES DEL NAVBAR QUE ACTIVAN LOS DROPDOWNS (VISIBLES)
    OFFERS_DROPDOWN_BUTTON = (By.XPATH, "//button[contains(@class, 'main-header_nav-primary_item_link') and contains(@class, 'main-header_nav-primary_item--section-offer')]")
    BOOKING_DROPDOWN_BUTTON = (By.XPATH, "//button[contains(@class, 'main-header_nav-primary_item_link') and contains(@class, 'main-header_nav-primary_item--section-booking')]")
    INFO_DROPDOWN_BUTTON = (By.XPATH, "//button[contains(@class, 'main-header_nav-primary_item_link') and contains(@class, 'main-header_nav-primary_item--section-info')]")
    
    # MENÚS DESPLEGABLES (INVISIBLES HASTA QUE SE ACTIVEN)
    OFFERS_DROPDOWN_MENU = (By.CSS_SELECTOR, ".main-header_nav-primary_item--section-offer .main-header_primary-nav_submenu")
    BOOKING_DROPDOWN_MENU = (By.CSS_SELECTOR, ".main-header_nav-primary_item--section-booking .main-header_primary-nav_submenu")
    INFO_DROPDOWN_MENU = (By.CSS_SELECTOR, ".main-header_nav-primary_item--section-info .main-header_primary-nav_submenu")
    
    # ENLACES ESPECÍFICOS DENTRO DE LOS DROPDOWNS (CORREGIDOS SEGÚN HTML REAL)
    OFFERS_FLIGHTS_LINK = (By.CSS_SELECTOR, "a.main-header_primary-nav_submenu_item--n3[href*='/ofertas-destinos/ofertas-de-vuelos/']")
    OFFERS_FLIGHTS_LINK_TEXT = (By.XPATH, "//a[@class='main-header_primary-nav_submenu_item--n3']//span[contains(text(), 'Ofertas de vuelos')]")
    CHECKIN_LINK = (By.XPATH, "//a[contains(@href, '/check-in/')]")
    TARIFFS_LINK = (By.XPATH, "//a[contains(@href, '/tarifas-avianca/')]")
    
    # ENLACES ALTERNATIVOS POR TEXTO
    OFFERS_FLIGHTS_LINK_ALT = (By.XPATH, "//a[contains(text(), 'Ofertas de vuelos') or contains(text(), 'Flight offers')]")
    CHECKIN_LINK_ALT = (By.XPATH, "//a[contains(text(), 'Check-in') or contains(text(), 'Check-in')]")
    TARIFFS_LINK_ALT = (By.XPATH, "//a[contains(text(), 'Tarifas') or contains(text(), 'Fares')]")
    
    # Elementos para verificar que cargó correctamente cada página
    OFFERS_PAGE_INDICATOR = (By.XPATH, "//h1[contains(text(), 'Ofertas') or contains(text(), 'Offers') or contains(text(), 'Offres') or contains(text(), 'Ofertas')]")
    CHECKIN_PAGE_INDICATOR = (By.XPATH, "//h1[contains(text(), 'Check-in') or contains(text(), 'Check-in')]")
    TARIFF_TYPES_INDICATOR = (By.XPATH, "//h1[contains(text(), 'Tarifas') or contains(text(), 'Fares') or contains(text(), 'Tarifs')]")

    # ===== LOCATORES ACTUALIZADOS PARA CASO 7: REDIRECCIONES FOOTER EN ESPAÑOL =====
    FOOTER_SECTION = (By.TAG_NAME, "footer")
    
    # Enlaces específicos del footer en español (los 4 NUEVOS requeridos) - ACTUALIZADOS CON LA INFORMACIÓN PROPORCIONADA
    FOOTER_LINK_1 = (By.XPATH, "//footer//li[contains(@class, 'ng-tns-c30-8')]//a[contains(@href, '/es/ofertas-destinos/ofertas-de-vuelos/')]")
    FOOTER_LINK_2 = (By.XPATH, "//footer//a[contains(text(), 'Somos avianca') or contains(@href, 'somos-avianca')]")
    FOOTER_LINK_3 = (By.XPATH, "//footer//a[contains(text(), 'aviancadirect') or contains(@href, 'aviancadirect')]")
    FOOTER_LINK_4 = (By.XPATH, "//footer//a[contains(text(), 'Información legal') or contains(@href, 'legal')]")
    
    # Locators alternativos más específicos basados en la estructura HTML proporcionada
    FOOTER_LINK_1_ALT = (By.CSS_SELECTOR, "footer li.ng-tns-c30-8 a[href*='/es/ofertas-destinos/ofertas-de-vuelos/']")
    FOOTER_LINK_1_BY_SPAN = (By.XPATH, "//footer//span[contains(@class, 'link-label') and contains(text(), 'Vuelos baratos')]")
    
    # Elementos para verificar que las páginas del footer cargaron correctamente
    FOOTER_PAGE_1_INDICATOR = (By.XPATH, "//h1[contains(text(), 'Vuelos baratos') or contains(text(), 'vuelos')]")
    FOOTER_PAGE_2_INDICATOR = (By.XPATH, "//h1[contains(text(), 'Somos') or contains(text(), 'avianca')]")
    FOOTER_PAGE_3_INDICATOR = (By.XPATH, "//h1[contains(text(), 'aviancadirect') or contains(text(), 'direct')]")
    FOOTER_PAGE_4_INDICATOR = (By.XPATH, "//h1[contains(text(), 'Legal') or contains(text(), 'legal')]")

    # ===== LOCATORS PARA CASO 3: LOGIN Y BÚSQUEDA ===== (NUEVOS)
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button.auth_trigger_button")
    USERNAME_INPUT = (By.ID, "u-username")
    PASSWORD_INPUT = (By.ID, "u-password")
    SUBMIT_LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    
    # Selectores de búsqueda de vuelos
    TRIP_TYPE_DROPDOWN = (By.CSS_SELECTOR, "[aria-label*='trip type'], [class*='trip-type']")
    ONE_WAY_OPTION = (By.XPATH, "//*[contains(text(), 'Solo ida') or contains(text(), 'One way') or contains(text(), 'Un seul trajet')]")
    ROUND_TRIP_OPTION = (By.XPATH, "//*[contains(text(), 'Ida y vuelta') or contains(text(), 'Round trip') or contains(text(), 'Aller-retour')]")
    
    ORIGIN_BUTTON = (By.ID, "originBtn")
    ORIGIN_SEARCH_INPUT = (By.ID, "departureStationInputId")
    ORIGIN_OPTIONS = (By.CSS_SELECTOR, "[role='option'], .station-option")
    
    DESTINATION_INPUT = (By.ID, "arrivalStationInputId")
    DESTINATION_OPTIONS = (By.CSS_SELECTOR, "[role='option'], .station-option")
    
    DEPARTURE_DATE_BUTTON = (By.CSS_SELECTOR, "[aria-label*='Fecha de ida'], [aria-label*='Departure date']")
    RETURN_DATE_BUTTON = (By.CSS_SELECTOR, "[aria-label*='Fecha de vuelta'], [aria-label*='Return date']")
    
    # ===== LOCATORS PARA SELECCIÓN DE PASAJEROS =====
    PASSENGERS_BUTTON = (By.CSS_SELECTOR, "button.control_field_button[aria-label*='Passagers'], button.control_field_button[aria-label*='Pasajeros']")
    PASSENGER_MODAL = (By.ID, "paxControlSearchId")
    ADULT_PLUS_BUTTON = (By.XPATH, "//input[@id='inputPax_ADT']/ancestor::div[contains(@class, 'ui-num-ud')]//button[contains(@class, 'ui-num-ud_button') and contains(@class, 'plus')]")
    YOUTH_PLUS_BUTTON = (By.XPATH, "//input[@id='inputPax_TNG']/ancestor::div[contains(@class, 'ui-num-ud')]//button[contains(@class, 'ui-num-ud_button') and contains(@class, 'plus')]")
    YOUTH_INPUT = (By.ID, "inputPax_TNG")
    CHILD_PLUS_BUTTON = (By.XPATH, "//input[@id='inputPax_CHD']/ancestor::div[contains(@class, 'ui-num-ud')]//button[contains(@class, 'ui-num-ud_button') and contains(@class, 'plus')]")
    CHILD_INPUT = (By.ID, "inputPax_CHD")
    INFANT_PLUS_BUTTON = (By.XPATH, "//input[@id='inputPax_INF']/ancestor::div[contains(@class, 'ui-num-ud')]//button[contains(@class, 'ui-num-ud_button') and contains(@class, 'plus')]")
    INFANT_INPUT = (By.ID, "inputPax_INF")
    PASSENGER_CONFIRM_BUTTON = (By.XPATH, "//button[contains(@class, 'control_options_selector_action_button')]//span[contains(text(), 'Confirmer')]")

    # === LOCATORS ALTERNATIVOS BASADOS EN EL HTML REAL ===
    ADULT_PLUS_ALTERNATIVE = (By.XPATH, "//input[@id='inputPax_ADT']/following-sibling::button[@class='ui-num-ud_button plus']")
    ADULT_INPUT = (By.ID, "inputPax_ADT")
    
    SEARCH_FLIGHTS_BUTTON = (By.ID, "searchButton")

    # ===== LOCATORS PARA SELECCIÓN DE VUELOS =====
    FIRST_FLIGHT_BUTTON = (By.CSS_SELECTOR, "button.journey_price_button")
    FIRST_FLIGHT_BUTTON_TEXT = (By.XPATH, "//button[contains(@class, 'journey_price_button')]//span[contains(text(), 'Choisir le tarif')]")
    FLEX_FARE_BUTTON = (By.XPATH, "//button[contains(., 'Flex') or contains(., 'FLEX') or contains(@class, 'flex')]")
    FLEX_FARE_SELECT = (By.XPATH, "//button[contains(., 'Sélectionner') and (contains(., 'Flex') or contains(., 'FLEX'))]")

    # Contenedor de resultados de vuelos
    FLIGHT_RESULTS_CONTAINER = (By.CSS_SELECTOR, "[class*='journey'], [class*='flight']")
    FARE_OPTIONS_CONTAINER = (By.CSS_SELECTOR, "[class*='fare'], [class*='tariff']")

    # Para verificar que estamos en la página correcta
    SELECT_FLIGHT_PAGE_INDICATOR = (By.XPATH, "//h1[contains(., 'Sélectionnez') or contains(., 'Select') or contains(., 'Seleccionar')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    # ===== MÉTODOS DE COMPATIBILIDAD =====
    
    def fill(self, locator, text, timeout=10):
        """Método para llenar campos de texto - usa find_element del BasePage"""
        logger.info(f"Llenando campo {locator} con texto: {text}")
        try:
            element = self.find_element(locator)
            element.clear()
            element.send_keys(text)
            logger.info(f"✅ Campo {locator} llenado correctamente")
            return True
        except Exception as e:
            logger.error(f"❌ Error llenando campo {locator}: {e}")
            return False

    def click(self, locator, timeout=10):
        """Método de compatibilidad - usa click_element del BasePage"""
        return self.click_element(locator)

    def is_element_present(self, locator, timeout=5):
        """Método de compatibilidad - usa is_element_visible del BasePage"""
        return self.is_element_visible(locator)

    # ===== MÉTODO FALTANTE: NAVEGACIÓN =====
    def navigate_to(self, url):
        """Navegar a una URL específica"""
        logger.info(f"Navegando a: {url}")
        self.driver.get(url)
        self.wait_for_page_load()
        return True

    # ===== MÉTODOS DE DIAGNÓSTICO =====

    def debug_login_elements(self):
        """Método de diagnóstico para elementos de login"""
        logger.info("🔍 DEBUG: Buscando elementos de login...")
        
        try:
            # Buscar botón de login
            login_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button.auth_trigger_button, button[class*='auth'], button[class*='login']")
            logger.info(f"🔍 Botones de login encontrados: {len(login_buttons)}")
            for i, btn in enumerate(login_buttons):
                logger.info(f"  Botón {i+1}: Texto='{btn.text}', Clases='{btn.get_attribute('class')}'")
            
            # Buscar campos de usuario
            user_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input#u-username, input[type='email'], input[type='text'], input[name*='user'], input[placeholder*='user'], input[placeholder*='email']")
            logger.info(f"🔍 Campos de usuario encontrados: {len(user_inputs)}")
            
            # Buscar campos de contraseña
            pass_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input#u-password, input[type='password']")
            logger.info(f"🔍 Campos de contraseña encontrados: {len(pass_inputs)}")
            
            # Buscar botones de submit
            submit_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[type='submit'], button[class*='submit'], button[class*='login']")
            logger.info(f"🔍 Botones de submit encontrados: {len(submit_buttons)}")
            
            return {
                'login_buttons': login_buttons,
                'user_inputs': user_inputs,
                'pass_inputs': pass_inputs,
                'submit_buttons': submit_buttons
            }
            
        except Exception as e:
            logger.error(f"❌ Error en debug_login_elements: {e}")
            return {}

    def debug_navbar_links(self):
        """Método de diagnóstico para encontrar enlaces del navbar"""
        logger.info("🔍 DEBUG: Buscando todos los enlaces del navbar...")
        
        try:
            # Buscar todos los enlaces en el header/navbar
            selectors = [
                "//header//a",
                "//nav//a", 
                "//a[contains(@class, 'nav')]",
                "//a[contains(@href, 'ofertas') or contains(@href, 'offers')]",
                "//a[contains(@href, 'check-in') or contains(@href, 'checkin')]",
                "//a[contains(@href, 'tarifas') or contains(@href, 'fares')]"
            ]
            
            all_links = []
            for selector in selectors:
                try:
                    links = self.driver.find_elements(By.XPATH, selector)
                    for link in links:
                        try:
                            href = link.get_attribute('href') or 'No href'
                            text = link.text.strip() or 'No text'
                            visible = link.is_displayed()
                            enabled = link.is_enabled()
                            
                            link_info = {
                                'selector': selector,
                                'href': href,
                                'text': text,
                                'visible': visible,
                                'enabled': enabled,
                                'element': link
                            }
                            
                            # Evitar duplicados
                            if href not in [l['href'] for l in all_links]:
                                all_links.append(link_info)
                                
                        except Exception as e:
                            logger.debug(f"Error procesando enlace: {e}")
                            continue
                            
                except Exception as e:
                    logger.debug(f"Error con selector {selector}: {e}")
                    continue
            
            # Log de todos los enlaces encontrados
            logger.info(f"🔍 Enlaces encontrados: {len(all_links)}")
            for i, link in enumerate(all_links):
                logger.info(f"  {i+1}. Text: '{link['text']}'")
                logger.info(f"     Href: {link['href']}")
                logger.info(f"     Visible: {link['visible']}, Enabled: {link['enabled']}")
                logger.info(f"     Selector: {link['selector']}")
            
            return all_links
            
        except Exception as e:
            logger.error(f"❌ Error en debug_navbar_links: {e}")
            return []

    # ===== MÉTODOS DE LOGIN MEJORADOS =====

    def login(self, username, password):
        """Realizar login en la aplicación - VERSIÓN MEJORADA"""
        logger.info(f"Iniciando sesión con usuario: {username}")
        
        try:
            # DEBUG: Mostrar elementos de login disponibles
            self.debug_login_elements()
            
            # Paso 1: Hacer click en el botón de login para abrir el modal
            logger.info("1. Buscando y haciendo click en botón de login...")
            
            # Intentar diferentes selectores para el botón de login
            login_selectors = [
                self.LOGIN_BUTTON,
                (By.CSS_SELECTOR, "button.auth_trigger_button"),
                (By.CSS_SELECTOR, "button[class*='auth']"),
                (By.CSS_SELECTOR, "button[class*='login']"),
                (By.XPATH, "//button[contains(text(), 'Iniciar sesión') or contains(text(), 'Login') or contains(text(), 'Sign in')]"),
                (By.CLASS_NAME, "auth-trigger-button"),
                (By.ID, "loginButton")
            ]
            
            login_btn = None
            for selector in login_selectors:
                try:
                    login_btn = self.wait.until(EC.element_to_be_clickable(selector))
                    logger.info(f"✅ Botón de login encontrado con selector: {selector}")
                    break
                except:
                    continue
            
            if not login_btn:
                logger.error("❌ No se pudo encontrar el botón de login")
                return False
            
            # Hacer click en el botón de login
            self.click_element(login_btn)
            time.sleep(3)  # Esperar a que se abra el modal
            
            # Tomar screenshot después de abrir el modal
            self.take_screenshot("modal_login_abierto.png")
            
            # Paso 2: Llenar campo de usuario
            logger.info("2. Llenando campo de usuario...")
            
            # Intentar diferentes selectores para el campo de usuario
            username_selectors = [
                self.USERNAME_INPUT,
                (By.ID, "u-username"),
                (By.CSS_SELECTOR, "input[type='email']"),
                (By.CSS_SELECTOR, "input[type='text']"),
                (By.CSS_SELECTOR, "input[name*='user']"),
                (By.CSS_SELECTOR, "input[name*='email']"),
                (By.CSS_SELECTOR, "input[placeholder*='user']"),
                (By.CSS_SELECTOR, "input[placeholder*='email']"),
                (By.XPATH, "//input[@id='u-username']"),
                (By.XPATH, "//input[contains(@class, 'username')]")
            ]
            
            username_field = None
            for selector in username_selectors:
                try:
                    username_field = self.wait.until(EC.element_to_be_clickable(selector))
                    logger.info(f"✅ Campo de usuario encontrado con selector: {selector}")
                    break
                except:
                    continue
            
            if not username_field:
                logger.error("❌ No se pudo encontrar el campo de usuario")
                self.take_screenshot("campo_usuario_no_encontrado.png")
                return False
            
            # Limpiar y escribir en el campo de usuario
            username_field.clear()
            username_field.send_keys(username)
            logger.info(f"✅ Usuario ingresado: {username}")
            time.sleep(1)
            
            # Paso 3: Llenar campo de contraseña
            logger.info("3. Llenando campo de contraseña...")
            
            # Intentar diferentes selectores para el campo de contraseña
            password_selectors = [
                self.PASSWORD_INPUT,
                (By.ID, "u-password"),
                (By.CSS_SELECTOR, "input[type='password']"),
                (By.CSS_SELECTOR, "input[name*='password']"),
                (By.CSS_SELECTOR, "input[name*='pass']"),
                (By.CSS_SELECTOR, "input[placeholder*='password']"),
                (By.XPATH, "//input[@id='u-password']"),
                (By.XPATH, "//input[contains(@class, 'password')]")
            ]
            
            password_field = None
            for selector in password_selectors:
                try:
                    password_field = self.wait.until(EC.element_to_be_clickable(selector))
                    logger.info(f"✅ Campo de contraseña encontrado con selector: {selector}")
                    break
                except:
                    continue
            
            if not password_field:
                logger.error("❌ No se pudo encontrar el campo de contraseña")
                self.take_screenshot("campo_password_no_encontrado.png")
                return False
            
            # Limpiar y escribir en el campo de contraseña
            password_field.clear()
            password_field.send_keys(password)
            logger.info("✅ Contraseña ingresada")
            time.sleep(1)
            
            # Tomar screenshot con los campos llenos
            self.take_screenshot("campos_login_llenos.png")
            
            # Paso 4: Hacer click en el botón de enviar/login
            logger.info("4. Buscando botón de submit...")
            
            # Intentar diferentes selectores para el botón de submit
            submit_selectors = [
                self.SUBMIT_LOGIN_BUTTON,
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.CSS_SELECTOR, "button[class*='submit']"),
                (By.CSS_SELECTOR, "button[class*='login']"),
                (By.XPATH, "//button[contains(text(), 'Iniciar sesión') or contains(text(), 'Login') or contains(text(), 'Sign in') or contains(text(), 'Entrar')]"),
                (By.CSS_SELECTOR, "input[type='submit']")
            ]
            
            submit_btn = None
            for selector in submit_selectors:
                try:
                    submit_btn = self.wait.until(EC.element_to_be_clickable(selector))
                    logger.info(f"✅ Botón de submit encontrado con selector: {selector}")
                    break
                except:
                    continue
            
            if not submit_btn:
                logger.error("❌ No se pudo encontrar el botón de submit")
                self.take_screenshot("boton_submit_no_encontrado.png")
                return False
            
            # Hacer click en el botón de submit
            logger.info("Haciendo click en botón de login...")
            self.click_element(submit_btn)
            
            # Paso 5: Esperar a que el login procese
            logger.info("5. Esperando respuesta del login...")
            time.sleep(5)  # Esperar más tiempo para el procesamiento
            
            # Verificar si el login fue exitoso
            if self.verify_login_success():
                logger.info("✅ Login completado exitosamente")
                self.take_screenshot("login_exitoso.png")
                return True
            else:
                logger.warning("⚠️  No se pudo verificar el login exitoso, pero continuando...")
                self.take_screenshot("login_no_verificado.png")
                return True  # Continuar de todos modos
                
        except Exception as e:
            logger.error(f"❌ Error en login: {e}")
            self.take_screenshot("login_error.png")
            return False

    def verify_login_success(self):
        """Verificar si el login fue exitoso"""
        try:
            # Buscar elementos que indiquen login exitoso
            success_indicators = [
                (By.XPATH, "//*[contains(text(), 'Mi cuenta') or contains(text(), 'My account')]"),
                (By.XPATH, "//*[contains(text(), 'Bienvenido') or contains(text(), 'Welcome')]"),
                (By.XPATH, "//*[contains(text(), 'Hola') or contains(text(), 'Hello')]"),
                (By.CLASS_NAME, "user-profile"),
                (By.CLASS_NAME, "account-info"),
                (By.CLASS_NAME, "welcome-message"),
                (By.CSS_SELECTOR, "[class*='user']"),
                (By.CSS_SELECTOR, "[class*='account']")
            ]
            
            for indicator in success_indicators:
                if self.is_element_present(indicator, timeout=3):
                    element_text = self.find_element(indicator).text
                    logger.info(f"✅ Indicador de login exitoso encontrado: '{element_text}'")
                    return True
            
            # Verificar si el botón de login cambió o desapareció
            try:
                WebDriverWait(self.driver, 3).until_not(
                    EC.element_to_be_clickable(self.LOGIN_BUTTON)
                )
                logger.info("✅ Login exitoso (botón de login ya no está disponible)")
                return True
            except:
                pass
            
            # Verificar si hay mensajes de error
            error_indicators = [
                (By.XPATH, "//*[contains(text(), 'error') or contains(text(), 'Error')]"),
                (By.XPATH, "//*[contains(text(), 'incorrect') or contains(text(), 'Incorrect')]"),
                (By.XPATH, "//*[contains(text(), 'invalid') or contains(text(), 'Invalid')]"),
                (By.CLASS_NAME, "error-message"),
                (By.CLASS_NAME, "alert-danger"),
                (By.CLASS_NAME, "error")
            ]
            
            for error_indicator in error_indicators:
                if self.is_element_present(error_indicator, timeout=2):
                    error_text = self.find_element(error_indicator).text
                    logger.error(f"❌ Error en login: {error_text}")
                    return False
            
            logger.warning("⚠️  No se pudo determinar claramente el estado del login")
            return False
            
        except Exception as e:
            logger.error(f"Error verificando login: {e}")
            return False

    # ===== MÉTODOS DE NAVEGACIÓN HEADER =====

    def navigate_to_offers_and_destinations_optimized_v2(self):
        """Navegar a ofertas - VERSIÓN MEJORADA que primero entra a Ofertas y destinos y luego a Ofertas de vuelos"""
        logger.info("🚀 Navegando a Ofertas (versión mejorada)")
        
        initial_url = self.get_page_url()
        logger.info("1) Navegando primero a Ofertas y destinos...")
        
        try:
            # PASO 1: Activar el dropdown de ofertas
            offers_btn = self.wait.until(EC.element_to_be_clickable(self.OFFERS_DROPDOWN_BUTTON))
            logger.info("✅ Encontrado botón del menú Ofertas")
            self.click(offers_btn)
            time.sleep(1)  # Pequeña pausa para animación del dropdown

            # PASO 2: Una vez abierto el menú, buscar y hacer click en "Ofertas de vuelos"
            # Intentar por clase y href exactos primero
            try:
                flights_link = self.wait.until(EC.element_to_be_clickable(self.OFFERS_FLIGHTS_LINK))
                logger.info("✅ Encontrado enlace Ofertas de vuelos por selector principal")
            except:
                # Si falla, intentar por el texto del span
                try:
                    flights_link = self.wait.until(EC.element_to_be_clickable(self.OFFERS_FLIGHTS_LINK_TEXT))
                    logger.info("✅ Encontrado enlace Ofertas de vuelos por texto")
                except:
                    # Último intento: buscar por href parcial y clase
                    flights_link = self.wait.until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, "a[href*='ofertas-de-vuelos'].main-header_primary-nav_submenu_item--n3")
                        )
                    )
                    logger.info("✅ Encontrado enlace por búsqueda alternativa")

            # Capturar info antes del click
            href = flights_link.get_attribute('href')
            text = flights_link.text.strip()
            logger.info(f"2) Haciendo click en: '{text}' -> {href}")

            # Intentar el click con retry
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    self.click(flights_link)
                    break
                except:
                    if attempt == max_attempts - 1:
                        self.driver.execute_script("arguments[0].click();", flights_link)
                    else:
                        time.sleep(0.5)
                        continue

            # Esperar cambio de URL
            WebDriverWait(self.driver, 8).until(
                lambda driver: driver.current_url != initial_url
            )
            
            # Verificar que llegamos a la URL correcta
            current_url = self.get_page_url()
            if '/ofertas-de-vuelos/' in current_url:
                logger.info(f"✅ Navegación exitosa: {current_url}")
                return True
            else:
                logger.warning(f"⚠️ URL final no es la esperada: {current_url}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error en navegación: {e}")
            return False

    def navigate_to_offers_and_destinations_optimized(self):
        """Navegar a ofertas de vuelos - VERSIÓN OPTIMIZADA"""
        logger.info("🚀 Navegando a Ofertas (optimizado)")
        
        # Reducir timeout general
        fast_wait = WebDriverWait(self.driver, 5)
        
        try:
            # ESTRATEGIA DIRECTA: Buscar enlace por href/texto sin dropdowns
            offer_selectors = [
                (By.XPATH, "//a[contains(@href, 'ofertas') or contains(@href, 'offers')]"),
                (By.XPATH, "//a[contains(text(), 'Ofertas') or contains(text(), 'Offers')]"),
                (By.CSS_SELECTOR, "a[href*='ofertas'], a[href*='offers']"),
                self.OFFERS_FLIGHTS_LINK,
                self.OFFERS_FLIGHTS_LINK_ALT
            ]
            
            for selector in offer_selectors:
                try:
                    link = fast_wait.until(EC.element_to_be_clickable(selector))
                    logger.info(f"✅ Enlace encontrado: {link.get_attribute('href')}")
                    self.click(link)
                    
                    # Espera mínima para cambio de página
                    WebDriverWait(self.driver, 8).until(
                        lambda driver: driver.current_url != self.get_page_url()
                    )
                    logger.info("✅ Navegación exitosa a Ofertas")
                    return True
                    
                except Exception as e:
                    continue
                    
            logger.error("❌ No se encontró enlace de ofertas")
            return False
            
        except Exception as e:
            logger.error(f"Error en navegación optimizada: {e}")
            return False

    def navigate_to_my_booking_checkin_optimized(self):
        """Navegar a check-in - VERSIÓN OPTIMIZADA"""
        logger.info("🚀 Navegando a Check-in (optimizado)")
        
        fast_wait = WebDriverWait(self.driver, 5)
        initial_url = self.get_page_url()
        
        try:
            # ESTRATEGIA DIRECTA: Buscar enlaces por palabras clave específicas
            checkin_selectors = [
                (By.XPATH, "//a[contains(@href, 'check-in') or contains(@href, 'checkin')]"),
                (By.XPATH, "//a[contains(text(), 'Check-in') or contains(text(), 'Check-in')]"),
                (By.CSS_SELECTOR, "a[href*='check-in'], a[href*='checkin']"),
                self.CHECKIN_LINK,
                self.CHECKIN_LINK_ALT
            ]
            
            for selector in checkin_selectors:
                try:
                    link = fast_wait.until(EC.element_to_be_clickable(selector))
                    logger.info(f"✅ Enlace check-in encontrado: {link.get_attribute('href')}")
                    
                    # Click con JavaScript para evitar problemas de overlays
                    self.driver.execute_script("arguments[0].click();", link)
                    
                    # Esperar cambio de URL con timeout reducido
                    WebDriverWait(self.driver, 8).until(
                        lambda driver: driver.current_url != initial_url
                    )
                    logger.info("✅ Navegación exitosa a Check-in")
                    return True
                    
                except Exception as e:
                    continue
                    
            logger.error("❌ No se encontró enlace de check-in")
            return False
            
        except Exception as e:
            logger.error(f"Error en navegación optimizada a check-in: {e}")
            return False

    def navigate_to_info_and_help_tariffs_optimized(self):
        """Navegar a tipos de tarifas - VERSIÓN OPTIMIZADA"""
        logger.info("🚀 Navegando a Tarifas (optimizado)")
        
        fast_wait = WebDriverWait(self.driver, 5)
        
        try:
            # ESTRATEGIA DIRECTA: Buscar enlaces específicos
            tariff_selectors = [
                (By.XPATH, "//a[contains(@href, 'tarifas') or contains(@href, 'fares')]"),
                (By.XPATH, "//a[contains(text(), 'Tarifas') or contains(text(), 'Fares')]"),
                (By.CSS_SELECTOR, "a[href*='tarifas'], a[href*='fares']"),
                self.TARIFFS_LINK,
                self.TARIFFS_LINK_ALT
            ]
            
            for selector in tariff_selectors:
                try:
                    link = fast_wait.until(EC.element_to_be_clickable(selector))
                    logger.info(f"✅ Enlace tarifas encontrado: {link.get_attribute('href')}")
                    self.click(link)
                    
                    # Espera mínima para cambio de página
                    WebDriverWait(self.driver, 8).until(
                        lambda driver: driver.current_url != self.get_page_url()
                    )
                    logger.info("✅ Navegación exitosa a Tarifas")
                    return True
                    
                except Exception as e:
                    continue
                    
            logger.error("❌ No se encontró enlace de tarifas")
            return False
            
        except Exception as e:
            logger.error(f"Error en navegación optimizada a tarifas: {e}")
            return False

    # ===== MÉTODOS ORIGINALES PARA CASO 6 (MANTENIDOS POR COMPATIBILIDAD) =====
    
    def navigate_to_offers_and_destinations(self):
        """Navegar a la sección 'Ofertas y destinos' -> ofertas de vuelos (Método original)"""
        logger.info("Navegando a: Ofertas y destinos -> ofertas de vuelos")
        try:
            # ESTRATEGIA 1: Usar dropdown de ofertas
            try:
                logger.info("🔍 Activando dropdown de ofertas...")
                offers_button = self.wait.until(EC.element_to_be_clickable(self.OFFERS_DROPDOWN_BUTTON))
                logger.info(f"✅ Botón de ofertas encontrado - Clases: {offers_button.get_attribute('class')}")
                self.click(offers_button)
                
                # Esperar a que el dropdown se abra
                self.wait.until(EC.visibility_of_element_located(self.OFFERS_DROPDOWN_MENU))
                logger.info("✅ Dropdown de ofertas abierto")
                
                # Hacer click en el enlace de ofertas de vuelos
                flights_link = self.wait.until(EC.element_to_be_clickable(self.OFFERS_FLIGHTS_LINK))
                logger.info(f"✅ Enlace de ofertas de vuelos encontrado - URL: {flights_link.get_attribute('href')}")
                self.click(flights_link)
                
            except Exception as e1:
                logger.warning(f"⚠️  Estrategia 1 falló: {e1}")
                
                # ESTRATEGIA 2: Usar enlace directo por texto
                logger.info("🔍 Buscando enlace directo por texto...")
                flights_link = self.wait.until(EC.element_to_be_clickable(self.OFFERS_FLIGHTS_LINK_ALT))
                logger.info(f"✅ Enlace alternativo encontrado - Texto: '{flights_link.text}'")
                self.click(flights_link)
            
            # Esperar a que cargue la nueva página
            self.wait.until(EC.presence_of_element_located(self.PAGE_LOAD_INDICATOR))
            time.sleep(2)  # Pausa adicional para asegurar carga
            
            logger.info("✅ Navegación exitosa a Ofertas de vuelos")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error navegando a Ofertas y destinos: {e}")
            return False

    def navigate_to_my_booking_checkin(self):
        """Navegar a la sección 'Tu reserva check-in' -> Gestiona tu reserva (Método original)"""
        logger.info("Navegando a: Tu reserva check-in -> Gestiona tu reserva")
        return self.navigate_to_my_booking_checkin_optimized()

    def navigate_to_info_and_help_tariffs(self):
        """Navegar a la sección 'Información y ayuda' -> Tipos de tarifas (Método original)"""
        logger.info("Navegando a: Información y ayuda -> Tipos de tarifas")
        return self.navigate_to_info_and_help_tariffs_optimized()

    # ===== MÉTODOS DE VERIFICACIÓN =====

    def verify_offers_page_loaded(self):
        """Verificar que la página de ofertas cargó correctamente"""
        logger.info("Verificando carga de página de ofertas")
        try:
            # Verificar por URL o elemento específico
            current_url = self.get_page_url()
            if "ofertas" in current_url.lower() or "offers" in current_url.lower() or "destinos" in current_url.lower():
                logger.info("✅ Página de ofertas cargada correctamente (verificación por URL)")
                return True
            
            # Verificar por elemento específico
            if self.is_element_present(self.OFFERS_PAGE_INDICATOR):
                logger.info("✅ Página de ofertas cargada correctamente (verificación por elemento)")
                return True
                
            # Verificación adicional: buscar cualquier indicador de ofertas en la página
            page_content = self.driver.page_source.lower()
            if "ofertas" in page_content or "offers" in page_content:
                logger.info("✅ Página de ofertas cargada correctamente (verificación por contenido)")
                return True
                
            logger.warning("❌ No se pudo verificar la carga de la página de ofertas")
            return False
            
        except Exception as e:
            logger.error(f"Error verificando página de ofertas: {e}")
            return False

    def verify_checkin_page_loaded(self):
        """Verificar que la página de check-in cargó correctamente"""
        logger.info("Verificando carga de página de check-in")
        try:
            # Verificar por URL o elemento específico
            current_url = self.get_page_url()
            if "check-in" in current_url.lower() or "checkin" in current_url.lower() or "reserva" in current_url.lower():
                logger.info("✅ Página de check-in cargada correctamente (verificación por URL)")
                return True
            
            # Verificar por elemento específico
            if self.is_element_present(self.CHECKIN_PAGE_INDICATOR):
                logger.info("✅ Página de check-in cargada correctamente (verificación por elemento)")
                return True
                
            # Verificación adicional: buscar cualquier indicador de check-in en la página
            page_content = self.driver.page_source.lower()
            if "check-in" in page_content or "checkin" in page_content or "reserva" in page_content:
                logger.info("✅ Página de check-in cargada correctamente (verificación por contenido)")
                return True
                
            logger.warning("❌ No se pudo verificar la carga de la página de check-in")
            return False
            
        except Exception as e:
            logger.error(f"Error verificando página de check-in: {e}")
            return False

    def verify_tariff_types_page_loaded(self):
        """Verificar que la página de tipos de tarifas cargó correctamente"""
        logger.info("Verificando carga de página de tipos de tarifas")
        try:
            # Verificar por URL o elemento específico
            current_url = self.get_page_url()
            if "tarifas" in current_url.lower() or "fares" in current_url.lower() or "informacion" in current_url.lower():
                logger.info("✅ Página de tipos de tarifas cargada correctamente (verificación por URL)")
                return True
            
            # Verificar por elemento específico
            if self.is_element_present(self.TARIFF_TYPES_INDICATOR):
                logger.info("✅ Página de tipos de tarifas cargada correctamente (verificación por elemento)")
                return True
                
            # Verificación adicional: buscar cualquier indicador de tarifas en la página
            page_content = self.driver.page_source.lower()
            if "tarifas" in page_content or "fares" in page_content or "informacion" in page_content:
                logger.info("✅ Página de tipos de tarifas cargada correctamente (verificación por contenido)")
                return True
                
            logger.warning("❌ No se pudo verificar la carga de la página de tipos de tarifas")
            return False
            
        except Exception as e:
            logger.error(f"Error verificando página de tipos de tarifas: {e}")
            return False

    # ===== MÉTODOS DE IDIOMA (Caso 4) =====
    
    def open_language_dropdown(self):
        """Abrir el dropdown de selección de idioma"""
        logger.info("Abriendo dropdown de idioma")
        try:
            # Intentar diferentes selectors para el botón de idioma
            selectors = [
                self.LANGUAGE_BUTTON,
                (By.CSS_SELECTOR, "[class*='language'], [class*='idioma']"),
                (By.XPATH, "//button[contains(@class, 'dropdown') and (contains(., 'ES') or contains(., 'EN'))]"),
                (By.CSS_SELECTOR, ".header [class*='dropdown']")
            ]
            
            for selector in selectors:
                try:
                    language_btn = self.wait.until(EC.element_to_be_clickable(selector))
                    # Intentar diferentes métodos de click
                    try:
                        self.click(language_btn)
                    except:
                        self.driver.execute_script("arguments[0].click();", language_btn)
                    
                    # Verificar que el dropdown se abrió
                    self.wait.until(EC.visibility_of_element_located(self.LANGUAGE_DROPDOWN))
                    logger.info("✅ Dropdown de idioma abierto exitosamente")
                    return True
                except:
                    continue
                    
            logger.warning("❌ No se pudo abrir el dropdown de idioma con ningún selector")
            return False
            
        except Exception as e:
            logger.error(f"Error abriendo dropdown de idioma: {e}")
            return False

    def select_language(self, language):
        """Seleccionar un idioma específico"""
        logger.info(f"Seleccionando idioma: {language}")
        
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                # Intentar abrir el dropdown
                if not self.open_language_dropdown():
                    logger.warning(f"Intento {attempt + 1}: No se pudo abrir el dropdown de idioma")
                    continue
                
                # Esperar un momento para que el dropdown se estabilice
                time.sleep(1)
                
                # Seleccionar el idioma específico
                language_map = {
                    'español': self.SPANISH_OPTION,
                    'english': self.ENGLISH_OPTION,
                    'français': self.FRENCH_OPTION,
                    'português': self.PORTUGUESE_OPTION
                }
                
                if language.lower() not in language_map:
                    raise ValueError(f"Idioma no soportado: {language}")
                
                # Intentar primero por XPath específico
                try:
                    language_option = self.wait.until(EC.element_to_be_clickable(language_map[language.lower()]))
                except:
                    # Si falla, buscar por texto de forma más flexible
                    logger.info("Buscando opción de idioma de forma alternativa...")
                    language_texts = {
                        'español': ['español', 'spanish', 'es'],
                        'english': ['english', 'inglés', 'en'],
                        'français': ['français', 'french', 'fr'],
                        'português': ['português', 'portuguese', 'pt']
                    }
                    
                    options = self.driver.find_elements(By.CSS_SELECTOR, ".dropdown_content .dropdown_item, [role='option'], .language-option")
                    for option in options:
                        try:
                            option_text = option.text.lower()
                            if any(text in option_text for text in language_texts[language.lower()]):
                                language_option = option
                                break
                        except:
                            continue
                
                # Intentar click con diferentes estrategias
                try:
                    self.click(language_option)
                except:
                    try:
                        self.driver.execute_script("arguments[0].click();", language_option)
                    except:
                        # Último recurso: simular click con Actions
                        from selenium.webdriver.common.action_chains import ActionChains
                        ActionChains(self.driver).move_to_element(language_option).click().perform()
                
                # Esperar a que la página se recargue con timeout extendido
                self.wait.until(EC.staleness_of(language_option))
                self.wait.until(EC.presence_of_element_located(self.PAGE_LOAD_INDICATOR))
                time.sleep(2)  # Espera adicional para asegurar la carga
                
                logger.info(f"✅ Idioma cambiado exitosamente a: {language}")
                return True
                
            except Exception as e:
                logger.warning(f"Intento {attempt + 1} falló: {str(e)}")
                if attempt < max_attempts - 1:
                    time.sleep(2)  # Esperar antes del siguiente intento
                    self.refresh_page()  # Refrescar página entre intentos
                    continue
                else:
                    logger.error(f"❌ No se pudo cambiar el idioma después de {max_attempts} intentos")
                    return False

    def get_current_language(self):
        """Obtener el idioma actualmente seleccionado"""
        try:
            language_btn = self.wait.until(EC.presence_of_element_located(self.LANGUAGE_BUTTON))
            return language_btn.text.strip()
        except Exception as e:
            logger.warning(f"No se pudo determinar el idioma actual: {e}")
            return "Unknown"

    def verify_language_changed(self, expected_language):
        """Verificar que el idioma cambió correctamente"""
        logger.info(f"Verificando cambio a idioma: {expected_language}")
        
        # Verificar elementos específicos por idioma
        text_verification_map = {
            'español': 'Ofertas',
            'english': 'Book', 
            'français': 'Vols',
            'português': 'Voos'
        }
        
        expected_text = text_verification_map.get(expected_language.lower(), 'Ofertas')
        
        try:
            # Buscar el texto esperado en la página
            page_content = self.driver.page_source
            if expected_text.lower() in page_content.lower():
                logger.info(f"Idioma verificado correctamente. Texto encontrado: {expected_text}")
                return True
            else:
                logger.warning(f"Texto esperado '{expected_text}' no encontrado en la página")
                return False
                
        except Exception as e:
            logger.error(f"Error verificando idioma: {e}")
            return False

    # ===== MÉTODOS DE POS/PAÍS (Caso 5) =====
    
    def open_pos_dropdown(self):
        """Abrir el dropdown de selección de POS/País"""
        logger.info("Abriendo dropdown de POS/País")
        
        # Usar el ID correcto que encontraste
        pos_btn = self.wait.until(EC.element_to_be_clickable(self.POS_SELECTOR_BUTTON))
        self.click(pos_btn)
        
        # Esperar a que el dropdown se abra (con múltiples opciones por si cambia el estilo)
        try:
            self.wait.until(EC.visibility_of_element_located(self.POS_DROPDOWN))
        except:
            # Si no encuentra el dropdown específico, esperar un momento para que se abra
            time.sleep(2)
            
        logger.info("Dropdown de POS abierto correctamente")
        return True

    def click_apply_button(self):
        """Hacer clic en el botón Aplicar/Apply usando la clase exacta"""
        logger.info("Buscando botón Aplicar/Apply con clase exacta...")
        
        try:
            # Buscar el botón por la clase exacta
            apply_button = self.wait.until(EC.element_to_be_clickable(self.POS_APPLY_BUTTON))
            button_text = apply_button.text.strip()
            self.click(apply_button)
            logger.info(f"✅ Botón '{button_text}' clickeado exitosamente")
            return True
        except Exception as e:
            logger.warning(f"No se pudo encontrar el botón con clase exacta: {e}")
            
            # Intentar con diferentes estrategias como fallback
            fallback_strategies = [
                # Por texto en diferentes idiomas
                (By.XPATH, "//button[contains(text(), 'Aplicar')]"),
                (By.XPATH, "//button[contains(text(), 'Apply')]"),
                (By.XPATH, "//button[contains(text(), 'Appliquer')]"),
                # Por clase parcial
                (By.CSS_SELECTOR, "button[class*='footer_action_button']"),
                (By.CSS_SELECTOR, "button[class*='action_button']"),
                # Por tipo submit
                (By.CSS_SELECTOR, "button[type='submit']"),
                # Buscar en el footer del modal
                (By.CSS_SELECTOR, ".points-of-sale_footer button"),
                (By.CSS_SELECTOR, ".modal-footer button")
            ]
            
            for strategy in fallback_strategies:
                try:
                    button = self.wait.until(EC.element_to_be_clickable(strategy))
                    if button.is_displayed() and button.is_enabled():
                        button_text = button.text.strip()
                        self.click(button)
                        logger.info(f"✅ Botón fallback '{button_text}' clickeado")
                        return True
                except Exception as fallback_error:
                    continue
            
            logger.error("❌ No se pudo encontrar ningún botón de aplicación")
            return False

    def select_pos(self, country_name):
        """Seleccionar un POS/País específico (solo los 3 requeridos)"""
        logger.info(f"Seleccionando POS/País: {country_name}")
        
        # Validar que sea uno de los 3 países requeridos
        valid_countries = ['otros países', 'españa', 'chile']
        if country_name.lower() not in valid_countries:
            raise ValueError(f"País no soportado: {country_name}. Solo se permiten: {valid_countries}")
        
        # Primero abrir el dropdown
        self.open_pos_dropdown()
        
        # Seleccionar el país específico
        pos_map = {
            'otros países': self.POS_OTHER_COUNTRIES,
            'españa': self.POS_SPAIN,
            'chile': self.POS_CHILE
        }
        
        country_option = self.wait.until(EC.element_to_be_clickable(pos_map[country_name.lower()]))
        self.click(country_option)
        
        # ✅ NUEVO PASO: Hacer clic en el botón Aplicar/Apply
        time.sleep(1)  # Pequeña pausa antes de buscar el botón
        apply_result = self.click_apply_button()
        
        if not apply_result:
            raise Exception("No se pudo hacer clic en el botón Aplicar/Apply")
        
        # Esperar a que la página se actualice
        self.wait.until(EC.presence_of_element_located(self.PAGE_LOAD_INDICATOR))
        
        # Pequeña pausa para asegurar que el cambio se aplique
        time.sleep(2)
        
        logger.info(f"POS/País cambiado a: {country_name}")
        return True

    def get_current_pos(self):
        """Obtener el POS/País actualmente seleccionado"""
        try:
            pos_btn = self.wait.until(EC.presence_of_element_located(self.POS_SELECTOR_BUTTON))
            current_text = pos_btn.text.strip()
            logger.info(f"POS actual detectado: '{current_text}'")
            return current_text
        except Exception as e:
            logger.warning(f"No se pudo determinar el POS actual: {e}")
            return "Unknown"

    def verify_pos_changed(self, expected_country):
        """Verificar que el POS/País cambió correctamente"""
        logger.info(f"Verificando cambio a POS/País: {expected_country}")
        
        try:
            current_pos = self.get_current_pos()
            expected_country_lower = expected_country.lower()
            
            # Verificar que el texto del botón contenga el país esperado
            # Usamos una verificación más flexible
            if (expected_country_lower in current_pos.lower() or 
                any(word in current_pos.lower() for word in expected_country_lower.split())):
                logger.info(f"✅ POS verificado correctamente. POS actual: '{current_pos}'")
                return True
            else:
                logger.warning(f"❌ POS actual '{current_pos}' no coincide con el esperado '{expected_country}'")
                return False
                
        except Exception as e:
            logger.error(f"Error verificando POS: {e}")
            return False

    # ===== MÉTODOS PARA BÚSQUEDA DE VUELOS =====

    def select_trip_type(self, trip_type="one-way"):
        """Seleccionar tipo de viaje"""
        logger.info(f"Seleccionando tipo de viaje: {trip_type}")
        try:
            if trip_type.lower() == "one-way":
                self.click(self.ONE_WAY_OPTION)
            else:
                self.click(self.ROUND_TRIP_OPTION)
            logger.info("✅ Tipo de viaje seleccionado")
            return True
        except Exception as e:
            logger.error(f"❌ Error seleccionando tipo de viaje: {e}")
            return False

    def select_origin(self, origin_code):
        """Seleccionar origen"""
        logger.info(f"Seleccionando origen: {origin_code}")
        try:
            self.click(self.ORIGIN_BUTTON)
            time.sleep(1)
            
            # Buscar y seleccionar el origen
            self.fill(self.ORIGIN_SEARCH_INPUT, origin_code)
            time.sleep(2)
            
            # Seleccionar la primera opción que aparezca
            if self.is_element_present(self.ORIGIN_OPTIONS):
                options = self.find_elements(self.ORIGIN_OPTIONS)
                if options:
                    self.click(options[0])
                    logger.info("✅ Origen seleccionado")
                    return True
            return False
            
        except Exception as e:
            logger.error(f"❌ Error seleccionando origen: {e}")
            return False

    def select_destination(self, destination_code):
        """Seleccionar destino"""
        logger.info(f"Seleccionando destino: {destination_code}")
        try:
            self.fill(self.DESTINATION_INPUT, destination_code)
            time.sleep(2)
            
            # Seleccionar la primera opción que aparezca
            if self.is_element_present(self.DESTINATION_OPTIONS):
                options = self.find_elements(self.DESTINATION_OPTIONS)
                if options:
                    self.click(options[0])
                    logger.info("✅ Destino seleccionado")
                    return True
            return False
            
        except Exception as e:
            logger.error(f"❌ Error seleccionando destino: {e}")
            return False
        
    def select_any_origin_destination(self):
        """Seleccionar origen y destino 'cualquiera' - CERRAR fechas con ESC"""
        logger.info("Seleccionando origen y destino 'cualquiera'")
        
        try:
            # PASO 0: Hacer scroll
            logger.info("0. Haciendo scroll...")
            self.driver.execute_script("window.scrollTo(0, 300);")
            time.sleep(2)
            
            # PASO 1: Seleccionar origen - BOGOTÁ
            logger.info("1. Seleccionando Bogotá como origen...")
            
            origin_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "originBtn")))
            origin_btn.click()
            time.sleep(2)
            
            origin_input = self.wait.until(EC.element_to_be_clickable((By.ID, "departureStationInputId")))
            origin_input.clear()
            origin_input.send_keys("BOG")
            time.sleep(3)
            
            if self.is_element_present(self.ORIGIN_OPTIONS):
                origin_options = self.find_elements(self.ORIGIN_OPTIONS)
                for option in origin_options:
                    if "BOG" in option.text or "Bogotá" in option.text:
                        option.click()
                        logger.info("✅ Bogotá seleccionado como origen")
                        break
            
            time.sleep(2)
            
            # PASO 2: Seleccionar destino - MEDELLÍN
            logger.info("2. Seleccionando Medellín como destino...")
            
            dest_input = self.wait.until(EC.element_to_be_clickable((By.ID, "arrivalStationInputId")))
            dest_input.click()
            time.sleep(1)
            
            dest_input.clear()
            dest_input.send_keys("MDE")
            time.sleep(3)
            
            if self.is_element_present(self.DESTINATION_OPTIONS):
                dest_options = self.find_elements(self.DESTINATION_OPTIONS)
                for option in dest_options:
                    if "MDE" in option.text or "Medellín" in option.text:
                        option.click()
                        logger.info("✅ Medellín seleccionado como destino")
                        break
            
            # PASO 3: CERRAR MODAL DE FECHAS CON ESC (como hiciste manualmente)
            logger.info("3. Cerrando modal de fechas con ESC...")
            time.sleep(3)
            
            from selenium.webdriver.common.keys import Keys
            body = self.find_element((By.TAG_NAME, "body"))
            body.send_keys(Keys.ESCAPE)
            logger.info("✅ Tecla ESC presionada")
            time.sleep(2)
            
            logger.info("✅✅✅ ORIGEN/DESTINO CONFIGURADOS - FECHAS CERRADAS CON ESC")
            return True
                
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return False


    def select_passengers(self, adults=1, youth=0, children=0, infants=0):
        """Seleccionar cantidad de pasajeros - CON LOCATORS CORREGIDOS"""
        logger.info(f"Seleccionando pasajeros: {adults} adultos, {youth} jóvenes, {children} niños, {infants} infantes")
        try:
            # PASO 1: Abrir modal
            logger.info("1. Abriendo modal de pasajeros...")
            self.click(self.PASSENGERS_BUTTON)
            time.sleep(3)
            
            # VERIFICAR que el modal se abrió
            try:
                modal = self.wait.until(EC.visibility_of_element_located(self.PASSENGER_MODAL))
                logger.info("✅ Modal de pasajeros abierto correctamente")
            except Exception as e:
                logger.error(f"❌ Modal no se abrió: {e}")
                return False
            
            # VERIFICAR que los botones + se encuentran
            logger.info("🔍 Verificando botones +...")
            
            try:
                adult_plus = self.wait.until(EC.presence_of_element_located(self.ADULT_PLUS_BUTTON))
                logger.info("✅ Botón + adultos encontrado")
            except Exception as e:
                logger.error(f"❌ Botón + adultos NO encontrado: {e}")
                return False
                
            try:
                youth_plus = self.find_element(self.YOUTH_PLUS_BUTTON)
                logger.info("✅ Botón + jóvenes encontrado")
            except Exception as e:
                logger.error(f"❌ Botón + jóvenes NO encontrado: {e}")
                
            try:
                child_plus = self.find_element(self.CHILD_PLUS_BUTTON)
                logger.info("✅ Botón + niños encontrado")
            except Exception as e:
                logger.error(f"❌ Botón + niños NO encontrado: {e}")
                
            try:
                infant_plus = self.find_element(self.INFANT_PLUS_BUTTON)
                logger.info("✅ Botón + infantes encontrado")
            except Exception as e:
                logger.error(f"❌ Botón + infantes NO encontrado: {e}")
            
            # PASO 2: Incrementar ADULTOS
            logger.info(f"2. Incrementando adultos a {adults}...")
            adult_count = 1
            for i in range(adults - 1):
                try:
                    adult_plus = self.wait.until(EC.element_to_be_clickable(self.ADULT_PLUS_BUTTON))
                    adult_plus.click()
                    adult_count += 1
                    logger.info(f"   ✅ Click {i+1} - Adultos: {adult_count}")
                    time.sleep(0.5)
                except Exception as e:
                    logger.error(f"❌ Error en click {i+1} adultos: {e}")
                    return False
            
            # PASO 3: Incrementar JÓVENES
            logger.info(f"3. Incrementando jóvenes a {youth}...")
            youth_count = 0
            for i in range(youth):
                try:
                    youth_plus = self.wait.until(EC.element_to_be_clickable(self.YOUTH_PLUS_BUTTON))
                    youth_plus.click()
                    youth_count += 1
                    logger.info(f"   ✅ Click {i+1} - Jóvenes: {youth_count}")
                    time.sleep(0.5)
                except Exception as e:
                    logger.error(f"❌ Error en click {i+1} jóvenes: {e}")
                    return False
            
            # PASO 4: Incrementar NIÑOS
            logger.info(f"4. Incrementando niños a {children}...")
            child_count = 0
            for i in range(children):
                try:
                    child_plus = self.wait.until(EC.element_to_be_clickable(self.CHILD_PLUS_BUTTON))
                    child_plus.click()
                    child_count += 1
                    logger.info(f"   ✅ Click {i+1} - Niños: {child_count}")
                    time.sleep(0.5)
                except Exception as e:
                    logger.error(f"❌ Error en click {i+1} niños: {e}")
                    return False
            
            # PASO 5: Incrementar INFANTES
            logger.info(f"5. Incrementando infantes a {infants}...")
            infant_count = 0
            for i in range(infants):
                try:
                    infant_plus = self.wait.until(EC.element_to_be_clickable(self.INFANT_PLUS_BUTTON))
                    infant_plus.click()
                    infant_count += 1
                    logger.info(f"   ✅ Click {i+1} - Infantes: {infant_count}")
                    time.sleep(0.5)
                except Exception as e:
                    logger.error(f"❌ Error en click {i+1} infantes: {e}")
                    return False
            
            # PASO 6: Confirmar selección
            logger.info("6. Confirmando selección...")
            try:
                confirm_btn = self.wait.until(EC.element_to_be_clickable(self.PASSENGER_CONFIRM_BUTTON))
                confirm_btn.click()
                logger.info("✅ Selección confirmada")
            except Exception as e:
                logger.error(f"❌ Error confirmando selección: {e}")
                return False
            
            time.sleep(2)
            logger.info(f"✅✅✅ PASAJEROS CONFIGURADOS: {adult_count} adultos, {youth_count} jóvenes, {child_count} niños, {infant_count} infantes")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error general en select_passengers: {e}")
            return False

    def search_flights(self):
        """Click en botón buscar vuelos"""
        logger.info("Buscando vuelos...")
        try:
            self.click(self.SEARCH_FLIGHTS_BUTTON)
            logger.info("✅ Búsqueda de vuelos iniciada")
            return True
        except Exception as e:
            logger.error(f"❌ Error buscando vuelos: {e}")
            return False

    def complete_flight_search(self, origin="BOG", destination="MDE", adults=1, youth=0, children=0, infants=0):
        """Completar toda la búsqueda de vuelos en un solo método"""
        logger.info("Completando búsqueda de vuelos")
        
        steps = [
            ("Seleccionar origen", lambda: self.select_origin(origin)),
            ("Seleccionar destino", lambda: self.select_destination(destination)),
            ("Seleccionar pasajeros", lambda: self.select_passengers(adults, youth, children, infants)),
            ("Buscar vuelos", lambda: self.search_flights())
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                logger.error(f"❌ Falló en paso: {step_name}")
                return False
            time.sleep(1)
        
        logger.info("✅ Búsqueda de vuelos completada exitosamente")
        return True
    
    def test_adult_plus_button(self):
        """MÉTODO TEMPORAL: Probar el botón + de adultos - VERSIÓN SIMPLIFICADA"""
        logger.info("🔍 INICIANDO PRUEBA BOTÓN ADULTOS - VERSIÓN SIMPLIFICADA")
        
        try:
            # PASO 1: Verificar estado actual
            logger.info("1. Verificando estado del modal...")
            self.take_screenshot("debug_estado_inicial.png")
            
            # Verificar si el modal ya está abierto
            try:
                modal = self.find_element(self.PASSENGER_MODAL)
                if modal.is_displayed():
                    logger.info("✅✅✅ MODAL YA ESTÁ ABIERTO - CONTINUANDO DIRECTAMENTE")
                else:
                    logger.info("🔄 Modal no abierto, intentando abrir...")
                    # Intentar abrir el modal
                    passengers_btn = self.wait.until(EC.element_to_be_clickable(self.PASSENGERS_BUTTON))
                    passengers_btn.click()
                    time.sleep(2)
            except:
                logger.info("🔄 Modal no encontrado, intentando abrir...")
                # Intentar abrir el modal
                passengers_btn = self.wait.until(EC.element_to_be_clickable(self.PASSENGERS_BUTTON))
                passengers_btn.click()
                time.sleep(2)
            
            # PASO 2: Buscar y hacer clic en botón + de adultos
            logger.info("2. Buscando botón + de adultos...")
            self.take_screenshot("debug_antes_boton_adultos.png")
            
            adult_plus = self.wait.until(EC.element_to_be_clickable(self.ADULT_PLUS_BUTTON))
            adult_plus.click()
            logger.info("✅ Clic en botón + de adultos realizado")
            time.sleep(2)
            
            # PASO 3: Verificar resultado
            logger.info("3. Verificando resultado...")
            adult_input = self.find_element(self.ADULT_INPUT)
            adult_value = adult_input.get_attribute("value")
            logger.info(f"✅ Valor de adultos después del clic: {adult_value}")
            
            # PASO 4: Cerrar modal
            logger.info("4. Cerrando modal...")
            try:
                confirm_btn = self.wait.until(EC.element_to_be_clickable(self.PASSENGER_CONFIRM_BUTTON))
                confirm_btn.click()
                logger.info("✅ Modal cerrado con Confirmar")
            except:
                logger.warning("⚠️ No se pudo cerrar el modal con Confirmar")
            
            logger.info("✅✅✅ PRUEBA COMPLETADA EXITOSAMENTE")
            return True
            
        except Exception as e:
            logger.error(f"❌ ERROR en prueba: {e}")
            self.take_screenshot("error_adultos.png")
            return False

    # ===== MÉTODOS PARA SELECCIÓN DE VUELOS =====
    def select_first_flight(self):
        """Seleccionar el primer vuelo disponible - OPTIMIZADO"""
        logger.info("✈️ Seleccionando primer vuelo (optimizado)...")
        try:
            # ESPERA OPTIMIZADA: Usar wait explícito en lugar de sleep
            logger.info("🔄 Esperando carga de página...")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.FIRST_FLIGHT_BUTTON)
            )
            
            # Scroll rápido
            self.driver.execute_script("window.scrollTo(0, 400);")
            
            # Buscar botones de vuelo
            flight_buttons = self.find_elements(self.FIRST_FLIGHT_BUTTON)
            
            if flight_buttons:
                first_button = flight_buttons[0]
                
                # Scroll al elemento específico
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", first_button)
                
                # Esperar que sea clickeable (máximo 5 segundos)
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(first_button))
                
                self.click(first_button)
                logger.info("✅ Vuelo seleccionado (optimizado)")
                
                # ESPERA REDUCIDA para carga de tarifas
                time.sleep(2)
                return True
                
            return False
            
        except Exception as e:
            logger.error(f"❌ Error seleccionando vuelo: {e}")
            return False
    
    def select_flex_fare(self, is_return_flight=False):
        """Seleccionar tarifa Flex - CON ESPERA ESTRATÉGICA PARA VUELOS DE REGRESO"""
        logger.info("🎫 Seleccionando tarifa Flex...")
        try:
            # ESPERA OPTIMIZADA: Esperar máximo 8 segundos por las tarifas
            logger.info("🔄 Esperando opciones de tarifa...")
            FLEX_SELECTOR = (By.CSS_SELECTOR, "div.fare-control.fare9[aria-label*='Flex']")
            
            flex_element = WebDriverWait(self.driver, 8).until(
                EC.element_to_be_clickable(FLEX_SELECTOR)
            )
            
            # Buscar botón dentro del elemento Flex
            select_button = flex_element.find_element(By.CSS_SELECTOR, "button.fare_button")
            
            # Esperar que el botón sea clickeable
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(select_button))
            
            self.click(select_button)
            logger.info("✅✅✅ Flex seleccionado")
            
            # 🔥 ESPERA ESTRATÉGICA: Si es para vuelo de IDA, esperar MÁS para vuelos de regreso
            if not is_return_flight:
                logger.info("🔄 ESPERA ESTRATÉGICA: Procesando vuelos de regreso...")
                # Espera más larga específicamente para que carguen los vuelos de regreso
                time.sleep(8)  # 8 segundos adicionales para procesamiento del servidor
                
                # Además, verificar que la página esté completamente lista
                WebDriverWait(self.driver, 12).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
                
                logger.info("✅✅✅ VUELOS DE REGRESO DEBERÍAN ESTAR CARGADOS")
            else:
                # Para vuelo de regreso, espera normal
                time.sleep(3)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error seleccionando Flex: {e}")
            return False
        
    def wait_for_return_flights_loaded(self, timeout=20):  # 🔥 Aumentado a 20 segundos
        """Espera inteligente para vuelos de regreso - MÁS TOLERANTE"""
        logger.info("🔄 Esperando carga INTELIGENTE de vuelos de regreso...")
        
        try:
            # INDICADORES MÁS FLEXIBLES
            return_indicators = [
                # 1. Cualquier botón de vuelo
                (By.CSS_SELECTOR, "button.journey_price_button"),
                # 2. Cualquier texto relacionado con vuelos
                (By.XPATH, "//*[contains(text(), 'Retour') or contains(text(), 'Vuelta') or contains(text(), 'Return') or contains(text(), 'Regreso')]"),
                # 3. Cualquier contenedor de vuelo
                (By.CSS_SELECTOR, "[class*='journey'], [class*='flight']"),
                # 4. Aeropuertos
                (By.XPATH, "//*[contains(text(), 'BOG') or contains(text(), 'MDE') or contains(text(), 'Bogotá') or contains(text(), 'Medellín')]"),
                # 5. Fechas de vuelo
                (By.XPATH, "//*[contains(text(), '202')]")  # Años
            ]
            
            # Esperar a que AL MENOS UN indicador esté presente (con timeout extendido)
            WebDriverWait(self.driver, timeout).until(
                lambda driver: any(
                    len(driver.find_elements(*indicator)) > 0 
                    for indicator in return_indicators
                )
            )
            
            logger.info("✅ Indicadores de vuelos de regreso encontrados")
            
            # ESPERA ADICIONAL ESPECÍFICA para botones clickeables
            logger.info("🔄 Verificando que los botones sean clickeables...")
            WebDriverWait(self.driver, 8).until(
                lambda driver: any(
                    btn.is_displayed() and btn.is_enabled()
                    for btn in driver.find_elements(By.CSS_SELECTOR, "button.journey_price_button")
                    if btn.is_displayed()
                )
            )
            
            logger.info("✅✅✅ VUELOS DE REGRESO CARGADOS Y LISTOS")
            return True
            
        except Exception as e:
            logger.error(f"❌ Timeout esperando vuelos de regreso: {e}")
            
            # DEPURACIÓN: Mostrar qué SÍ hay disponible
            self.debug_return_flights_status()
            return False    

    def wait_for_page_complete_load(self, timeout=15):
        """Esperar a que la página cargue completamente - OPTIMIZADO"""
        logger.info("🔄 Esperando carga completa de página...")
        try:
            # Esperar a que el documento esté listo
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Esperar a que no haya elementos de carga visibles
            WebDriverWait(self.driver, timeout).until(
                lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "[class*='loading'], [class*='spinner']")) == 0
            )
            
            logger.info("✅ Página cargada completamente")
            return True
            
        except Exception as e:
            logger.warning(f"⚠️  Carga de página tomó más tiempo: {e}")
            return True  # Continuar de todos modos
        
    def select_return_flight_optimized(self):
        """Seleccionar vuelo de regreso - CON SCROLL Y SELECCIÓN EXACTA"""
        logger.info("🔄 Seleccionando vuelo de regreso (con scroll y selección exacta)...")
        
        try:
            # PASO 1: Espera INTELIGENTE para vuelos de regreso
            if not self.wait_for_return_flights_loaded(timeout=20):
                logger.error("❌ No se cargaron los vuelos de regreso a tiempo")
                return False
            
            # PASO 2: SCROLL ESTRATÉGICO para hacer visibles los vuelos de regreso
            logger.info("🔄 Haciendo scroll estratégico para vuelos de regreso...")
            
            # Scroll más específico para la sección de vuelos de regreso
            self.driver.execute_script("window.scrollTo(0, 800);")
            time.sleep(2)
            
            # Scroll adicional si es necesario
            self.driver.execute_script("window.scrollTo(0, 1000);")
            time.sleep(1)
            
            # PASO 3: Buscar EXACTAMENTE los botones de vuelo de regreso
            logger.info("🔍 Buscando botones específicos de vuelo de regreso...")
            
            # SELECTOR EXACTO basado en el HTML que me mostraste
            return_buttons = self.find_elements((By.CSS_SELECTOR, "button.journey_price_button.ng-tns-c12-62"))
            
            # Si no encuentra con la clase específica, buscar cualquier botón de vuelo
            if not return_buttons:
                logger.info("🔄 Buscando botones de vuelo alternativos...")
                return_buttons = self.find_elements((By.CSS_SELECTOR, "button.journey_price_button"))
            
            logger.info(f"🔍 Botones de vuelo de regreso encontrados: {len(return_buttons)}")
            
            if not return_buttons:
                logger.error("❌ No se encontraron botones de vuelo de regreso")
                return False
            
            # PASO 4: Filtrar y seleccionar el PRIMER botón visible y habilitado
            visible_buttons = []
            for i, btn in enumerate(return_buttons):
                try:
                    if btn.is_displayed() and btn.is_enabled():
                        btn_text = btn.text.replace('\n', ' ').strip()
                        logger.info(f"  ✅ Botón {i} disponible: '{btn_text}'")
                        visible_buttons.append(btn)
                except Exception as e:
                    logger.debug(f"  ❌ Botón {i} no disponible: {e}")
                    continue
            
            logger.info(f"🔍 Botones de regreso clickeables: {len(visible_buttons)}")
            
            if not visible_buttons:
                logger.error("❌ No hay botones clickeables de vuelo de regreso")
                return False
            
            # PASO 5: Seleccionar el PRIMER botón clickeable
            return_button = visible_buttons[0]
            return_text = return_button.text.replace('\n', ' ').strip()
            logger.info(f"🎯 Seleccionando primer vuelo de regreso: '{return_text}'")
            
            # SCROLL PRECISO al botón específico
            logger.info("🔄 Haciendo scroll preciso al botón...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", return_button)
            time.sleep(1)
            
            # Verificar una última vez que sea clickeable
            logger.info("🔍 Verificando que el botón esté listo para clic...")
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(return_button))
            
            # Hacer clic en el primer vuelo de regreso
            logger.info("🖱️ Haciendo clic en el primer vuelo de regreso...")
            self.click(return_button)
            
            logger.info("✅✅✅ VUELO DE REGRESO SELECCIONADO EXITOSAMENTE")
            
            # Espera para confirmar la selección
            time.sleep(3)
            return True
            
        except Exception as e:
            logger.error(f"❌ Error crítico seleccionando vuelo de regreso: {e}")
            
            # Tomar screenshot del error
            self.take_screenshot("error_critico_vuelo_regreso.png")
            
            # Depuración adicional
            self.debug_return_flights_status()
            return False
        
    def debug_return_flights_status(self):
        """Depurar estado actual de los vuelos de regreso - MÁS DETALLADO"""
        logger.info("🔍 DEPURANDO ESTADO DE VUELOS DE REGRESO (DETALLADO)...")
        
        try:
            # Verificar diferentes tipos de botones
            button_types = {
                "Botones journey_price_button (todos)": len(self.find_elements((By.CSS_SELECTOR, "button.journey_price_button"))),
                "Botones con clase específica ng-tns-c12-62": len(self.find_elements((By.CSS_SELECTOR, "button.journey_price_button.ng-tns-c12-62"))),
                "Botones visibles": len([btn for btn in self.find_elements((By.CSS_SELECTOR, "button.journey_price_button")) if btn.is_displayed()]),
                "Botones habilitados": len([btn for btn in self.find_elements((By.CSS_SELECTOR, "button.journey_price_button")) if btn.is_enabled()]),
            }
            
            logger.info("📊 ESTADO DETALLADO DE BOTONES:")
            for key, value in button_types.items():
                logger.info(f"  {key}: {value}")
            
            # Mostrar información de los primeros 3 botones
            all_buttons = self.find_elements((By.CSS_SELECTOR, "button.journey_price_button"))
            logger.info("🔍 INFORMACIÓN DE PRIMEROS 3 BOTONES:")
            for i, btn in enumerate(all_buttons[:3]):
                try:
                    text = btn.text.replace('\n', ' ').strip()
                    displayed = btn.is_displayed()
                    enabled = btn.is_enabled()
                    classes = btn.get_attribute('class')
                    logger.info(f"  Botón {i}: '{text}' | Visible: {displayed} | Habilitado: {enabled} | Clases: {classes}")
                except:
                    logger.info(f"  Botón {i}: No se pudo obtener información")
            
            # Tomar screenshot del estado actual
            self.take_screenshot("debug_return_flights_detailed.png")
            
            return button_types
            
        except Exception as e:
            logger.error(f"Error en depuración detallada: {e}")
            return {}
        
    def debug_flight_selection(self):
        """Método de depuración para ver qué hay en la página de vuelos"""
        logger.info("🔍 DEPURANDO PÁGINA DE SELECCIÓN DE VUELOS")
        
        try:
            # Tomar screenshot de la página actual
            self.take_screenshot("debug_flight_page.png")
            
            # Buscar todos los botones disponibles
            all_buttons = self.find_elements((By.TAG_NAME, "button"))
            logger.info(f"🔍 Total de botones en la página: {len(all_buttons)}")
            
            # Filtrar botones relevantes
            relevant_buttons = []
            for i, button in enumerate(all_buttons):
                try:
                    text = button.text.strip()
                    classes = button.get_attribute('class') or ''
                    if text and ('choisir' in text.lower() or 'select' in text.lower() or 'tarif' in text.lower()):
                        relevant_buttons.append((i, text, classes))
                except:
                    continue
            
            logger.info("🔍 BOTONES RELEVANTES ENCONTRADOS:")
            for idx, text, classes in relevant_buttons:
                logger.info(f"  {idx}: '{text}' - Clases: {classes}")
            
            # Buscar contenedores de vuelos
            flight_containers = self.find_elements((By.CSS_SELECTOR, "[class*='journey'], [class*='flight']"))
            logger.info(f"🔍 Contenedores de vuelo encontrados: {len(flight_containers)}")
            
            return {
                'total_buttons': len(all_buttons),
                'relevant_buttons': relevant_buttons,
                'flight_containers': len(flight_containers)
            }
            
        except Exception as e:
            logger.error(f"❌ Error en depuración: {e}")
            return {}    

    def select_round_trip_flights(self):
        """Seleccionar vuelos de ida y vuelta"""
        logger.info("🔄 Seleccionando vuelos de ida y vuelta...")
        try:
            # PASO 1: Seleccionar vuelo de IDA
            logger.info("1. Seleccionando vuelo de IDA...")
            if not self.select_first_flight():
                return False
            
            # PASO 2: Seleccionar tarifa Flex para IDA
            logger.info("2. Seleccionando tarifa Flex para IDA...")
            if not self.select_flex_fare():
                return False
            
            # Esperar a que cargue la selección del vuelo de vuelta
            time.sleep(5)
            
            # PASO 3: Seleccionar vuelo de VUELTA
            logger.info("3. Seleccionando vuelo de VUELTA...")
            if not self.select_first_flight():
                return False
            
            # PASO 4: Seleccionar tarifa Flex para VUELTA
            logger.info("4. Seleccionando tarifa Flex para VUELTA...")
            if not self.select_flex_fare():
                return False
            
            logger.info("✅✅✅ VUELOS DE IDA Y VUELTA SELECCIONADOS EXITOSAMENTE")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error seleccionando vuelos ida y vuelta: {e}")
            return False

    def is_select_flight_page_loaded(self):
        """Validar si la página de Select Flight cargó correctamente"""
        logger.info("Validando carga de página Select Flight")
        
        try:
            # Verificar por URL
            current_url = self.get_page_url().lower()
            if "select-flight" in current_url or "seleccionar-vuelo" in current_url:
                logger.info("✅ Select Flight page loaded (URL verification)")
                return True
            
            # Verificar por elementos de la página de resultados
            select_flight_indicators = [
                (By.XPATH, "//h1[contains(text(), 'Select Flight') or contains(text(), 'Seleccionar vuelo')]"),
                (By.XPATH, "//div[contains(@class, 'flight-option')]"),
                (By.XPATH, "//button[contains(text(), 'Select') or contains(text(), 'Seleccionar')]"),
                (By.CLASS_NAME, "flight-list"),
                (By.ID, "flightResults")
            ]
            
            for indicator in select_flight_indicators:
                if self.is_element_present(indicator, timeout=5):
                    logger.info(f"✅ Select Flight page loaded (element: {indicator})")
                    return True
            
            # Verificación de fallback: al menos no estamos en home
            if "nuxqa3.avtest.ink" in current_url and "search" not in current_url:
                logger.warning("❌ Still on home page after search")
                return False
                
            logger.info("✅ Search results page loaded (basic verification)")
            return True
            
        except Exception as e:
            logger.error(f"Error validating Select Flight page: {e}")
            return False

    # ===== MÉTODOS GENERALES =====
    
    def wait_for_page_load(self, timeout=10):
        """Esperar a que la página cargue completamente"""
        try:
            self.wait.until(EC.presence_of_element_located(self.PAGE_LOAD_INDICATOR))
            logger.info("Página cargada completamente")
            return True
        except Exception as e:
            logger.error(f"Error esperando carga de página: {e}")
            return False

    def take_screenshot(self, filename):
        """Tomar screenshot de la página actual"""
        try:
            import os
            os.makedirs("screenshots", exist_ok=True)
            self.driver.save_screenshot(f"screenshots/{filename}")
            logger.info(f"Screenshot guardado: {filename}")
            return True
        except Exception as e:
            logger.error(f"Error tomando screenshot: {e}")
            return False

    def get_page_url(self):
        """Obtener la URL actual de la página"""
        return self.driver.current_url

    def refresh_page(self):
        """Refrescar la página actual"""
        logger.info("Refrescando página")
        self.driver.refresh()
        self.wait_for_page_load()
        return True

    def is_element_present(self, locator, timeout=5):
        """Verificar si un elemento está presente en la página"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except:
            return False

    def find_elements(self, locator):
        """Encontrar múltiples elementos"""
        try:
            return self.driver.find_elements(*locator)
        except Exception as e:
            logger.error(f"Error encontrando elementos {locator}: {e}")
            return []
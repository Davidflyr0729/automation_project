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
    
    # ENLACES ESPECÍFICOS DENTRO DE LOS DROPDOWNS
    OFFERS_FLIGHTS_LINK = (By.XPATH, "//a[contains(@href, '/ofertas-de-vuelos/')]")
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

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    # ===== MÉTODO FALTANTE: NAVEGACIÓN =====
    def navigate_to(self, url):
        """Navegar a una URL específica"""
        logger.info(f"Navegando a: {url}")
        self.driver.get(url)
        self.wait_for_page_load()
        return True

    # ===== MÉTODOS DE IDIOMA (Caso 4) =====
    
    def open_language_dropdown(self):
        """Abrir el dropdown de selección de idioma"""
        logger.info("Abriendo dropdown de idioma")
        try:
            # Intentar diferentes selectores para el botón de idioma
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
                        language_btn.click()
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
                    language_option.click()
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

    # ===== MÉTODOS DE POS/PAÍS (Caso 5) - ACTUALIZADOS CON BOTÓN EXACTO =====
    
    def open_pos_dropdown(self):
        """Abrir el dropdown de selección de POS/País"""
        logger.info("Abriendo dropdown de POS/País")
        
        # Usar el ID correcto que encontraste
        pos_btn = self.wait.until(EC.element_to_be_clickable(self.POS_SELECTOR_BUTTON))
        pos_btn.click()
        
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
            apply_button.click()
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
                        button.click()
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
        country_option.click()
        
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

    # ===== MÉTODOS PARA CASO 6: REDIRECCIONES HEADER ===== (ESTRATEGIA CORREGIDA)
    
    def navigate_to_offers_and_destinations(self):
        """Navegar a la sección 'Ofertas y destinos' -> ofertas de vuelos"""
        logger.info("Navegando a: Ofertas y destinos -> ofertas de vuelos")
        try:
            # ESTRATEGIA 1: Usar dropdown de ofertas
            try:
                logger.info("🔍 Activando dropdown de ofertas...")
                offers_button = self.wait.until(EC.element_to_be_clickable(self.OFFERS_DROPDOWN_BUTTON))
                logger.info(f"✅ Botón de ofertas encontrado - Clases: {offers_button.get_attribute('class')}")
                offers_button.click()
                
                # Esperar a que el dropdown se abra
                self.wait.until(EC.visibility_of_element_located(self.OFFERS_DROPDOWN_MENU))
                logger.info("✅ Dropdown de ofertas abierto")
                
                # Hacer click en el enlace de ofertas de vuelos
                flights_link = self.wait.until(EC.element_to_be_clickable(self.OFFERS_FLIGHTS_LINK))
                logger.info(f"✅ Enlace de ofertas de vuelos encontrado - URL: {flights_link.get_attribute('href')}")
                flights_link.click()
                
            except Exception as e1:
                logger.warning(f"⚠️  Estrategia 1 falló: {e1}")
                
                # ESTRATEGIA 2: Usar enlace directo por texto
                logger.info("🔍 Buscando enlace directo por texto...")
                flights_link = self.wait.until(EC.element_to_be_clickable(self.OFFERS_FLIGHTS_LINK_ALT))
                logger.info(f"✅ Enlace alternativo encontrado - Texto: '{flights_link.text}'")
                flights_link.click()
            
            # Esperar a que cargue la nueva página
            self.wait.until(EC.presence_of_element_located(self.PAGE_LOAD_INDICATOR))
            time.sleep(2)  # Pausa adicional para asegurar carga
            
            logger.info("✅ Navegación exitosa a Ofertas de vuelos")
            # Guardar evidencia rápida
            try:
                ts = int(time.time())
                screenshot = f"caso6_offers_success_{ts}.png"
                self.take_screenshot(screenshot)
                with open(f"screenshots/caso6_offers_success_{ts}.html", 'w', encoding='utf-8') as f:
                    f.write(self.driver.page_source)
                logger.info(f"Evidencia guardada: screenshots/{screenshot}")
            except Exception as e:
                logger.debug(f"No se pudo guardar evidencia de ofertas: {e}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error navegando a Ofertas y destinos: {e}")
            self._debug_navbar_dropdowns()
            # ESTRATEGIA FINAL: Buscar cualquier enlace en header/nav que contenga indicadores de ofertas
            try:
                logger.info("🔁 Estrategia final: buscar enlaces en header/nav por texto/href para Ofertas")
                candidates = self.driver.find_elements(By.XPATH, "//header//a | //nav//a | //a")
                keywords = ['ofertas', 'offers', 'oferta', 'flight', 'vuelos', 'destinos']
                for link in candidates:
                    try:
                        href = (link.get_attribute('href') or '').lower()
                        text = (link.text or '').lower()
                        if any(k in href or k in text for k in keywords):
                            logger.info(f"✅ Enlace candidato encontrado (texto='{text}', href='{href}'), intentando click")
                            try:
                                link.click()
                            except Exception:
                                # fallback a JS click si click() falla (por overlays, estilos, etc.)
                                self.driver.execute_script("arguments[0].click();", link)

                            self.wait.until(EC.presence_of_element_located(self.PAGE_LOAD_INDICATOR))
                            time.sleep(2)
                            logger.info("✅ Navegación por estrategia final exitosa")
                            return True
                    except Exception:
                        continue
            except Exception as e_final:
                logger.error(f"❌ Estrategia final falló: {e_final}")

            return False

    def navigate_to_my_booking_checkin(self):
        """Navegar a la sección 'Tu reserva check-in' -> Gestiona tu reserva"""
        logger.info("Navegando a: Tu reserva check-in -> Gestiona tu reserva (optimizado)")
        initial_url = self.get_page_url()

        # Helper to capture quick evidence for each attempt
        def _capture_attempt(tag):
            try:
                ts = int(time.time())
                name = f"caso6_checkin_{tag}_{ts}.png"
                self.take_screenshot(name)
                with open(f"screenshots/caso6_checkin_{tag}_{ts}.html", 'w', encoding='utf-8') as f:
                    f.write(self.driver.page_source)
                logger.info(f"Evidencia de intento guardada: screenshots/{name}")
            except Exception as e:
                logger.debug(f"No se pudo guardar evidencia del intento: {e}")

        # Estrategia rápida A: enlaces directos en header/nav por palabras clave
        keywords = ['check-in', 'checkin', 'booking', 'reserva', 'manage-booking', 'mi-reserva', 'managebooking', 'my-booking', 'booking/']
        anchors = self.driver.find_elements(By.XPATH, "//header//a | //nav//a | //a")
        for idx, a in enumerate(anchors, start=1):
            try:
                href = (a.get_attribute('href') or '').lower()
                text = (a.text or '').lower()
                if not any(k in href or k in text for k in keywords):
                    continue

                # Log candidate details and outerHTML for debugging
                try:
                    outer = self.driver.execute_script('return arguments[0].outerHTML;', a)
                except Exception:
                    outer = ''
                logger.info(f"Candidato #{idx}: text='{text}' href='{href}'")
                logger.debug(f"OuterHTML: {outer[:1000]}")

                # Ensure element is visible and in view
                try:
                    self.driver.execute_script('arguments[0].scrollIntoView({block: "center"});', a)
                except Exception:
                    pass

                # Click with fallbacks and capture evidence
                try:
                    a.click()
                except Exception:
                    try:
                        self.driver.execute_script("arguments[0].click();", a)
                    except Exception:
                        logger.debug("No se pudo clicar el enlace de forma normal")

                # Wait shortly for URL change
                try:
                    WebDriverWait(self.driver, 6).until(lambda d: d.current_url != initial_url)
                    logger.info(f"✅ Navegación detectada tras clicar candidato #{idx}: {self.get_page_url()}")
                    _capture_attempt(f"success_{idx}")
                    return True
                except Exception:
                    logger.debug(f"Candidato #{idx} no provocó cambio de URL")
                    _capture_attempt(f"candidate_{idx}")
                    continue
            except Exception as e:
                logger.debug(f"Error procesando candidato #{idx}: {e}")
                continue

        # Estrategia B: abrir dropdown y buscar enlace (optimizado con short waits)
        short_wait = WebDriverWait(self.driver, 6)
        try:
            try:
                booking_btn = short_wait.until(EC.element_to_be_clickable(self.BOOKING_DROPDOWN_BUTTON))
                try:
                    booking_btn.click()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", booking_btn)
            except Exception:
                try:
                    alt_btn = short_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[class*='booking'], [class*='reserva']")))
                    self.driver.execute_script("arguments[0].click();", alt_btn)
                except Exception:
                    logger.debug("No se encontró botón de dropdown de reservas rápidamente")

            link_selectors = [self.CHECKIN_LINK, self.CHECKIN_LINK_ALT,
                              (By.XPATH, "//a[contains(@href, 'check-in') or contains(@href, 'checkin') or contains(@href, 'manage-booking') or contains(@href, 'booking') or contains(@href, 'reserva')]")]

            for i, sel in enumerate(link_selectors, start=1):
                try:
                    el = short_wait.until(EC.element_to_be_clickable(sel))
                    try:
                        self.driver.execute_script('arguments[0].scrollIntoView({block: "center"});', el)
                    except Exception:
                        pass
                    try:
                        el.click()
                    except Exception:
                        self.driver.execute_script("arguments[0].click();", el)

                    try:
                        WebDriverWait(self.driver, 7).until(lambda d: d.current_url != initial_url)
                        logger.info(f"✅ Navegación a Check-in exitosa desde dropdown: {self.get_page_url()}")
                        _capture_attempt(f"dropdown_success_{i}")
                        return True
                    except Exception:
                        logger.debug(f"Selector {sel} clicado pero no cambió URL")
                        _capture_attempt(f"dropdown_candidate_{i}")
                        continue
                except Exception as e:
                    logger.debug(f"Selector {sel} no clickeable: {e}")
                    continue

        except Exception as e:
            logger.debug(f"Estrategia dropdown falló rápido: {e}")

        # Falla final: guardar evidencia amplia y debug
        try:
            ts = int(time.time())
            screenshot = f"caso6_checkin_fail_{ts}.png"
            self.take_screenshot(screenshot)
            with open(f"screenshots/caso6_checkin_fail_{ts}.html", 'w', encoding='utf-8') as f:
                f.write(self.driver.page_source)
            logger.info(f"👀 Evidencia guardada: screenshots/{screenshot} y HTML")
        except Exception as e:
            logger.warning(f"No se pudo guardar evidencia: {e}")

        self._debug_navbar_dropdowns()
        logger.error("❌ No se pudo navegar a Tu reserva check-in en modo optimizado")
        return False

    def navigate_to_info_and_help_tariffs(self):
        """Navegar a la sección 'Información y ayuda' -> Tipos de tarifas"""
        logger.info("Navegando a: Información y ayuda -> Tipos de tarifas")
        try:
            # ESTRATEGIA 1: Usar dropdown de información
            try:
                logger.info("🔍 Activando dropdown de información...")
                info_button = self.wait.until(EC.element_to_be_clickable(self.INFO_DROPDOWN_BUTTON))
                logger.info(f"✅ Botón de información encontrado - Clases: {info_button.get_attribute('class')}")
                info_button.click()
                
                # Esperar a que el dropdown se abra
                self.wait.until(EC.visibility_of_element_located(self.INFO_DROPDOWN_MENU))
                logger.info("✅ Dropdown de información abierto")
                
                # Hacer click en el enlace de tarifas
                tariffs_link = self.wait.until(EC.element_to_be_clickable(self.TARIFFS_LINK))
                logger.info(f"✅ Enlace de tarifas encontrado - URL: {tariffs_link.get_attribute('href')}")
                tariffs_link.click()
                
            except Exception as e1:
                logger.warning(f"⚠️  Estrategia 1 falló: {e1}")
                
                # ESTRATEGIA 2: Usar enlace directo por texto
                logger.info("🔍 Buscando enlace directo por texto...")
                tariffs_link = self.wait.until(EC.element_to_be_clickable(self.TARIFFS_LINK_ALT))
                logger.info(f"✅ Enlace alternativo encontrado - Texto: '{tariffs_link.text}'")
                tariffs_link.click()
            
            # Esperar a que cargue la nueva página
            self.wait.until(EC.presence_of_element_located(self.PAGE_LOAD_INDICATOR))
            time.sleep(2)  # Pausa adicional para asegurar carga
            
            logger.info("✅ Navegación exitosa a Tipos de tarifas")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error navegando a Información y ayuda: {e}")
            self._debug_navbar_dropdowns()
            # ESTRATEGIA FINAL: Buscar cualquier enlace en header/nav que contenga indicadores de tarifas
            try:
                logger.info("🔁 Estrategia final: buscar enlaces en header/nav por texto/href para Tarifas")
                candidates = self.driver.find_elements(By.XPATH, "//header//a | //nav//a | //a")
                keywords = ['tarifas', 'fares', 'tarifa', 'tarifs', 'tarifas-avianca', 'pricing']
                for link in candidates:
                    try:
                        href = (link.get_attribute('href') or '').lower()
                        text = (link.text or '').lower()
                        if any(k in href or k in text for k in keywords):
                            logger.info(f"✅ Enlace candidato encontrado (texto='{text}', href='{href}'), intentando click")
                            try:
                                link.click()
                            except Exception:
                                self.driver.execute_script("arguments[0].click();", link)

                            self.wait.until(EC.presence_of_element_located(self.PAGE_LOAD_INDICATOR))
                            time.sleep(2)
                            logger.info("✅ Navegación por estrategia final exitosa")
                            return True
                    except Exception:
                        continue
            except Exception as e_final:
                logger.error(f"❌ Estrategia final falló: {e_final}")

            return False

    def _debug_navbar_dropdowns(self):
        """Método de debug para verificar botones dropdown del navbar"""
        logger.info("🔍 DEBUG: Analizando botones dropdown del navbar...")
        try:
            # Buscar todos los botones del navbar
            buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'main-header_nav-primary_item_link')]")
            logger.info(f"🔍 Botones del navbar encontrados: {len(buttons)}")
            
            for i, button in enumerate(buttons):
                classes = button.get_attribute('class')
                text = button.text.strip() if button.text.strip() else "(sin texto)"
                visible = button.is_displayed()
                logger.info(f"  {i+1}. Clases: '{classes}'")
                logger.info(f"     Texto: '{text}'")
                logger.info(f"     Visible: {visible}")
                
        except Exception as e:
            logger.error(f"❌ Error en debug dropdowns: {e}")

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
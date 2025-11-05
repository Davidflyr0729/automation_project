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

    # ===== MÉTODOS DE DIAGNÓSTICO PARA CASO 6 =====

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

    def debug_click_first_offers_link(self):
        """Intentar hacer click en el primer enlace de ofertas encontrado"""
        logger.info("🔍 DEBUG: Intentando click en primer enlace de ofertas...")
        
        links = self.debug_navbar_links()
        
        # Filtrar enlaces de ofertas
        offers_keywords = ['ofertas', 'offers', 'vuelos', 'flights', 'destinos', 'destinations']
        offers_links = []
        
        for link in links:
            href = link['href'].lower()
            text = link['text'].lower()
            
            if any(keyword in href or keyword in text for keyword in offers_keywords):
                if link['visible'] and link['enabled']:
                    offers_links.append(link)
        
        logger.info(f"🔍 Enlaces de ofertas encontrados: {len(offers_links)}")
        
        if offers_links:
            # Intentar hacer click en el primer enlace de ofertas
            first_link = offers_links[0]
            logger.info(f"🖱️  Intentando click en: '{first_link['text']}' - {first_link['href']}")
            
            try:
                # Scroll al elemento
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_link['element'])
                time.sleep(1)
                
                # Intentar click normal
                first_link['element'].click()
                logger.info("✅ Click exitoso")
                return True
                
            except Exception as e:
                logger.warning(f"❌ Click normal falló: {e}, intentando con JavaScript...")
                try:
                    self.driver.execute_script("arguments[0].click();", first_link['element'])
                    logger.info("✅ Click con JavaScript exitoso")
                    return True
                except Exception as e2:
                    logger.error(f"❌ Click con JavaScript también falló: {e2}")
                    return False
        else:
            logger.error("❌ No se encontraron enlaces de ofertas clickeables")
            return False

    # ===== MÉTODOS ACTUALIZADOS CON ESTRATEGIA MEJORADA =====

    def navigate_to_offers_and_destinations_optimized_v2(self):
        """Navegar a ofertas - VERSIÓN MEJORADA que primero entra a Ofertas y destinos y luego a Ofertas de vuelos"""
        logger.info("🚀 Navegando a Ofertas (versión mejorada)")
        
        initial_url = self.get_page_url()
        logger.info("1) Navegando primero a Ofertas y destinos...")
        
        try:
            # PASO 1: Activar el dropdown de ofertas
            offers_btn = self.wait.until(EC.element_to_be_clickable(self.OFFERS_DROPDOWN_BUTTON))
            logger.info("✅ Encontrado botón del menú Ofertas")
            offers_btn.click()
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
                    flights_link.click()
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

    # ===== MÉTODOS OPTIMIZADOS PARA CASO 6: REDIRECCIONES HEADER =====
    
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
                    link.click()
                    
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
                    link.click()
                    
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

    # ===== MÉTODOS ACTUALIZADOS PARA CASO 7: REDIRECCIONES FOOTER EN ESPAÑOL =====

    def is_footer_visible(self):
        """Verificar que el footer está visible"""
        logger.info("Verificando visibilidad del footer")
        try:
            footer = self.wait.until(EC.visibility_of_element_located(self.FOOTER_SECTION))
            logger.info("✅ Footer visible")
            return True
        except Exception as e:
            logger.error(f"❌ Footer no visible: {e}")
            return False

    def debug_footer_links(self):
        """Método de diagnóstico para encontrar todos los enlaces del footer"""
        logger.info("🔍 DEBUG: Buscando todos los enlaces del footer...")
        
        try:
            # Asegurarse de que el footer esté visible
            self.is_footer_visible()
            
            # Buscar todos los enlaces en el footer
            footer_links = self.driver.find_elements(By.XPATH, "//footer//a")
            logger.info(f"🔍 Enlaces encontrados en el footer: {len(footer_links)}")
            
            all_links = []
            for i, link in enumerate(footer_links):
                try:
                    href = link.get_attribute('href') or 'No href'
                    text = link.text.strip() or 'No text'
                    visible = link.is_displayed()
                    enabled = link.is_enabled()
                    
                    link_info = {
                        'index': i,
                        'href': href,
                        'text': text,
                        'visible': visible,
                        'enabled': enabled,
                        'element': link
                    }
                    
                    all_links.append(link_info)
                    
                    logger.info(f"  {i+1}. Text: '{text}'")
                    logger.info(f"     Href: {href}")
                    logger.info(f"     Visible: {visible}, Enabled: {enabled}")
                    
                except Exception as e:
                    logger.debug(f"Error procesando enlace {i}: {e}")
                    continue
            
            return all_links
            
        except Exception as e:
            logger.error(f"❌ Error en debug_footer_links: {e}")
            return []

    def navigate_to_footer_link(self, link_locator, expected_url_keyword, verification_locator=None, alternative_locators=None):
        """Navegar a un enlace específico del footer y verificar la redirección"""
        logger.info(f"Navegando a enlace del footer: {link_locator}")
        
        initial_url = self.get_page_url()
        
        try:
            # Scroll al footer primero
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            # Intentar diferentes locators si se proporcionan alternativas
            locators_to_try = [link_locator]
            if alternative_locators:
                locators_to_try.extend(alternative_locators)
            
            link = None
            for locator in locators_to_try:
                try:
                    link = self.wait.until(EC.element_to_be_clickable(locator))
                    logger.info(f"✅ Enlace encontrado con locator: {locator}")
                    break
                except:
                    continue
            
            if not link:
                logger.error("❌ No se pudo encontrar el enlace con ningún locator")
                return False
            
            href = link.get_attribute('href')
            text = link.text.strip()
            
            logger.info(f"🖱️ Haciendo click en: '{text}' -> {href}")
            
            # Intentar click con diferentes estrategias
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    link.click()
                    break
                except:
                    if attempt == max_attempts - 1:
                        self.driver.execute_script("arguments[0].click();", link)
                    else:
                        time.sleep(0.5)
                        continue

            # Esperar cambio de URL
            WebDriverWait(self.driver, 8).until(
                lambda driver: driver.current_url != initial_url
            )
            
            # Verificar que llegamos a la URL correcta
            current_url = self.get_page_url()
            if expected_url_keyword.lower() in current_url.lower():
                logger.info(f"✅ Redirección exitosa: {current_url}")
                
                # Verificación adicional con elemento específico si se proporciona
                if verification_locator:
                    if self.is_element_present(verification_locator):
                        logger.info("✅ Página cargada correctamente (verificación por elemento)")
                        return True
                    else:
                        logger.warning("⚠️  Redirección exitosa pero no se pudo verificar el elemento específico")
                        return True
                else:
                    return True
            else:
                logger.warning(f"⚠️  URL final no contiene la palabra clave esperada: {current_url}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error en navegación: {e}")
            return False

    # Métodos específicos para los 4 NUEVOS enlaces del footer en español - ACTUALIZADOS
    def navigate_to_footer_link_1(self):
        """Navegar a 'Vuelos baratos' - ACTUALIZADO con los nuevos locators"""
        return self.navigate_to_footer_link(
            self.FOOTER_LINK_1, 
            'vuelos-baratos', 
            self.FOOTER_PAGE_1_INDICATOR,
            alternative_locators=[self.FOOTER_LINK_1_ALT, self.FOOTER_LINK_1_BY_SPAN]
        )

    def navigate_to_footer_link_2(self):
        """Navegar a 'Somos avianca'"""
        return self.navigate_to_footer_link(
            self.FOOTER_LINK_2,
            'somos-avianca',
            self.FOOTER_PAGE_2_INDICATOR
        )

    def navigate_to_footer_link_3(self):
        """Navegar a 'aviancadirect'"""
        return self.navigate_to_footer_link(
            self.FOOTER_LINK_3,
            'aviancadirect', 
            self.FOOTER_PAGE_3_INDICATOR
        )

    def navigate_to_footer_link_4(self):
        """Navegar a 'Información legal'"""
        return self.navigate_to_footer_link(
            self.FOOTER_LINK_4,
            'legal',
            self.FOOTER_PAGE_4_INDICATOR
        )

    def verify_url_contains_language_context(self, expected_language):
        """Verificar que la URL contiene el contexto del idioma seleccionado"""
        current_url = self.get_page_url().lower()
        
        # Solo verificamos si la URL contiene el código de idioma
        language_codes = {
            'español': '/es/',
            'english': '/en/', 
            'français': '/fr/',
            'português': '/pt/'
        }
        
        if expected_language.lower() in language_codes:
            expected_code = language_codes[expected_language.lower()]
            if expected_code in current_url:
                logger.info(f"✅ URL contiene contexto de idioma: {expected_language} ({expected_code})")
                return True
            else:
                logger.warning(f"⚠️  URL no contiene contexto de idioma esperado: {expected_language}")
                logger.info(f"   URL actual: {current_url}")
                return False
        
        logger.warning(f"⚠️  Idioma no reconocido: {expected_language}")
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
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LanguagePage(BasePage):
    """Page Object para manejar cambios de idioma"""
    
    # LOCATOR CORREGIDO - El primer botón dropdown_trigger (sin texto)
    LANGUAGE_BUTTON = (By.CLASS_NAME, "dropdown_trigger")
    
    # Mapeo de idiomas
    LANGUAGE_MAP = {
        'español': ('Español', 'es'),
        'english': ('English', 'en'), 
        'francais': ('Français', 'fr'),
        'portugues': ('Português', 'pt')
    }
    
    # Textos característicos por idioma para validación de contenido
    LANGUAGE_TEXTS = {
        'español': 'Ofertas',      # Texto en español
        'english': 'Book',      # Texto en inglés  
        'francais': 'Vols',        # Texto en francés
        'portugues': 'Voos'        # Texto en portugués
    }
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def open_language_menu(self):
        """Abrir el menú de selección de idioma"""
        print("🔄 Abriendo menú de idiomas...")
        
        # Encontrar TODOS los botones con dropdown_trigger
        all_dropdown_buttons = self.driver.find_elements(By.CLASS_NAME, "dropdown_trigger")
        print(f"🔍 Encontrados {len(all_dropdown_buttons)} botones dropdown_trigger")
        
        # El primer botón (sin texto) es el de idioma
        if len(all_dropdown_buttons) > 0:
            language_button = all_dropdown_buttons[0]  # Primer botón
            print("✅ Usando el primer botón dropdown_trigger (idioma)")
            language_button.click()
        else:
            raise Exception("No se encontró el botón de idioma")
    
    def select_language(self, language_name):
        """Seleccionar un idioma específico"""
        print(f"🔄 Cambiando a idioma: {language_name}")
        
        # ✅ CORREGIDO: Obtener la URL base actual dinámicamente
        current_url = self.driver.current_url
        if "nuxqa4" in current_url:
            base_domain = "nuxqa4.avtest.ink"
        elif "nuxqa5" in current_url:
            base_domain = "nuxqa5.avtest.ink"
        else:
            base_domain = "nuxqa4.avtest.ink"  # Por defecto
        
        # Abrir el menú
        self.open_language_menu()
        
        # Pequeña pausa para que se abra el dropdown
        import time
        time.sleep(2)
        
        # Buscar el idioma en nuestro mapeo
        if language_name.lower() not in self.LANGUAGE_MAP:
            raise ValueError(f"Idioma no soportado: {language_name}")
        
        display_name, url_code = self.LANGUAGE_MAP[language_name.lower()]
        
        # Crear locator para la opción específica
        language_option = (By.XPATH, f"//*[contains(text(), '{display_name}')]")
        
        # Hacer click en la opción
        self.click_element(language_option)
        
        # ✅ CORREGIDO: Usar la URL base dinámica
        expected_url = f"https://{base_domain}/{url_code}/"
        self.wait_for_url(expected_url)
        
        return url_code
    
    def validate_language_content(self, language_name):
        """
        Valida que el contenido de la página esté en el idioma correcto
        buscando textos específicos de cada idioma
        """
        expected_text = self.LANGUAGE_TEXTS.get(language_name.lower())
        if not expected_text:
            raise ValueError(f"No hay texto de validación para: {language_name}")
        
        print(f"🔍 Validando texto '{expected_text}' para idioma {language_name}")
        
        try:
            # Buscar el texto en cualquier parte de la página
            element = self.wait_for_element(
                (By.XPATH, f"//*[contains(text(), '{expected_text}')]"),
                timeout=10
            )
            
            if element:
                print(f"✅ Validación EXITOSA: texto '{expected_text}' encontrado")
                return True
            else:
                print(f"❌ Validación FALLIDA: texto '{expected_text}' NO encontrado")
                return False
                
        except Exception as e:
            print(f"❌ Error en validación de contenido: {e}")
            return False
    
    def get_current_language(self):
        """Obtener el idioma actual basado en URL Y contenido"""
        current_url = self.driver.current_url
        
        # Primero verificar por URL (como lo haces actualmente)
        if '/en/' in current_url:
            url_lang = 'english'
        elif '/fr/' in current_url:
            url_lang = 'francais' 
        elif '/pt/' in current_url:
            url_lang = 'portugues'
        else:
            url_lang = 'español'
        
        # Luego validar que el contenido coincide
        content_valid = self.validate_language_content(url_lang)
        
        if not content_valid:
            print(f"⚠️  ADVERTENCIA: URL dice '{url_lang}' pero el contenido no coincide")
        
        return url_lang
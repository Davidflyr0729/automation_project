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
        
        # Esperar a que la URL cambie
        expected_url = f"https://nuxqa4.avtest.ink/{url_code}/"
        self.wait_for_url(expected_url)
        
        return url_code
    
    def get_current_language(self):
        """Obtener el idioma actual basado en la URL"""
        current_url = self.driver.current_url
        
        if '/en/' in current_url:
            return 'english'
        elif '/fr/' in current_url:
            return 'francais' 
        elif '/pt/' in current_url:
            return 'portugues'
        else:
            return 'español'
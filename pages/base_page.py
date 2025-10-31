from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from datetime import datetime

class BasePage:
    """Clase base para todas las páginas del proyecto"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, locator):
        """Encontrar un elemento con espera explícita"""
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            print(f"❌ Elemento no encontrado: {locator}")
            raise
    
    def click_element(self, locator):
        """Hacer click en un elemento"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            print(f"✅ Click realizado en: {locator}")
        except TimeoutException:
            print(f"❌ No se pudo hacer click en: {locator}")
            raise
    
    def wait_for_url(self, url, timeout=10):
        """Esperar a que la URL cambie"""
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_to_be(url))
            print(f"✅ URL cambiada correctamente a: {url}")
            return True
        except TimeoutException:
            print(f"❌ URL no cambió a: {url}")
            print(f"   URL actual: {self.driver.current_url}")
            return False
    
    def is_element_visible(self, locator):
        """Verificar si un elemento es visible"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            print(f"✅ Elemento visible: {locator}")
            return True
        except TimeoutException:
            print(f"⚠️  Elemento no visible: {locator}")
            return False
    
    def get_element_text(self, locator):
        """Obtener texto de un elemento"""
        try:
            element = self.find_element(locator)
            text = element.text
            print(f"✅ Texto obtenido: '{text}' de {locator}")
            return text
        except TimeoutException:
            print(f"❌ No se pudo obtener texto de: {locator}")
            raise
    
    def take_full_page_screenshot(self, filename):
        """Tomar screenshot de toda la página (scroll completo)"""
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            # Obtener dimensiones de la página completa
            total_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            
            print(f"📏 Dimensiones página: altura total={total_height}, vista={viewport_height}")
            
            # Si la página es más alta que la vista, hacer scroll y capturar
            if total_height > viewport_height:
                # Configurar el tamaño de la ventana para capturar toda la altura
                original_size = self.driver.get_window_size()
                self.driver.set_window_size(original_size['width'], total_height)
                
                # Tomar screenshot de página completa
                self.driver.save_screenshot(filename)
                
                # Restaurar tamaño original
                self.driver.set_window_size(original_size['width'], original_size['height'])
            else:
                # Página cabe en una sola captura
                self.driver.save_screenshot(filename)
            
            print(f"📸 Screenshot completo guardado: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Error tomando screenshot completo: {e}")
            # Fallback: screenshot normal
            self.driver.save_screenshot(filename)
            print(f"📸 Screenshot normal guardado: {filename}")
            return filename
    
    def take_screenshot_with_url(self, filename):
        """Tomar screenshot y agregar información de URL en el nombre"""
        try:
            # Obtener URL actual
            current_url = self.driver.current_url
            # Limpiar URL para nombre de archivo
            url_safe = current_url.replace('https://', '').replace('/', '_').replace(':', '')
            # Agregar timestamp
            timestamp = datetime.now().strftime("%H%M%S")
            
            # Crear nombre de archivo con URL
            base_name = os.path.splitext(filename)[0]
            extension = os.path.splitext(filename)[1]
            new_filename = f"{base_name}_{url_safe}_{timestamp}{extension}"
            
            # Tomar screenshot
            return self.take_full_page_screenshot(new_filename)
            
        except Exception as e:
            print(f"❌ Error tomando screenshot con URL: {e}")
            return self.take_full_page_screenshot(filename)
    
    def get_page_info(self):
        """Obtener información completa de la página"""
        try:
            info = {
                'url': self.driver.current_url,
                'title': self.driver.title,
                'window_size': self.driver.get_window_size(),
                'page_height': self.driver.execute_script("return document.body.scrollHeight"),
                'viewport_height': self.driver.execute_script("return window.innerHeight")
            }
            return info
        except Exception as e:
            print(f"❌ Error obteniendo información de página: {e}")
            return {'url': self.driver.current_url, 'title': self.driver.title}
    
    def wait_for_element(self, locator, timeout=10):
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except Exception as e:
            print(f"❌ Elemento no encontrado: {locator} - {e}")
            return None
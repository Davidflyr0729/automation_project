from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from .base_page import BasePage
import allure
import logging
import time

class LoginPage(BasePage):
    
    # LOCATORS del botón de login principal
    LOGIN_BUTTON = (By.ID, "auth-component")
    
    # LOCATORS DEL MODAL DE LOGIN
    USERNAME_INPUT = (By.ID, "u-username")
    PASSWORD_INPUT = (By.ID, "u-password") 
    MODAL_LOGIN_BUTTON = (By.ID, "Login-confirm")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
    
    @allure.step("Hacer clic en botón 'Iniciar sesión'")
    def click_login_button(self):
        """Hacer clic en el botón de login que encontramos"""
        self.logger.info("Buscando botón 'Iniciar sesión'...")
        
        try:
            # Guardar la URL actual y las pestañas antes del clic
            current_url = self.driver.current_url
            original_window = self.driver.current_window_handle
            original_windows = self.driver.window_handles
            
            print(f"📍 URL actual antes del clic: {current_url}")
            print(f"📍 Pestañas abiertas antes: {len(original_windows)}")
            
            # Usar el locator específico que encontramos
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.LOGIN_BUTTON)
            )
            
            self.logger.info("✅ Botón 'Iniciar sesión' encontrado")
            print(f"📍 Texto del botón: '{login_button.text}'")
            
            # Hacer clic (esto abrirá nueva pestaña)
            login_button.click()
            self.logger.info("✅ Clic en botón 'Iniciar sesión' realizado")
            
            # 🆕 ESPERAR QUE SE ABRA NUEVA PESTAÑA
            print("⏱️ Esperando que se abra nueva pestaña...")
            WebDriverWait(self.driver, 10).until(
                lambda driver: len(driver.window_handles) > len(original_windows)
            )
            
            # 🆕 CAMBIAR A LA NUEVA PESTAÑA
            new_windows = self.driver.window_handles
            new_window = [window for window in new_windows if window not in original_windows][0]
            
            self.driver.switch_to.window(new_window)
            print(f"✅ Cambiado a nueva pestaña")
            
            # 🆕 VERIFICAR QUE ESTAMOS EN HYDRA
            WebDriverWait(self.driver, 10).until(
                lambda driver: "hydra.uat-lifemiles.net" in driver.current_url
            )
            
            new_url = self.driver.current_url
            print(f"📍 NUEVA URL en nueva pestaña: {new_url}")
            print("✅ Redirección a página de login detectada")
            
            # Esperar a que la página cargue completamente
            time.sleep(3)
            
            return True
                
        except Exception as e:
            self.logger.error(f"❌ Error haciendo clic en botón de login: {e}")
            print(f"❌ Error: {e}")
            print(f"📍 URL actual en el error: {self.driver.current_url}")
            print(f"📍 Pestañas abiertas: {len(self.driver.window_handles)}")
            
            # Tomar captura de error
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="error_boton_login",
                attachment_type=allure.attachment_type.PNG
            )
            return False

    @allure.step("Ingresar usuario: {username}")
    def enter_username(self, username):
        """Ingresar nombre de usuario en el campo correspondiente"""
        try:
            print("🔍 Buscando campo de usuario...")
            
            # 🆕 VERIFICAR QUE ESTAMOS EN LA PÁGINA CORRECTA
            current_url = self.driver.current_url
            print(f"📍 URL actual: {current_url}")
            
            if "hydra.uat-lifemiles.net" not in current_url:
                print("❌ ERROR: No estamos en la página de login de hydra")
                return False
            
            # 🆕 BUSCAR DIRECTAMENTE EN EL DOM PRINCIPAL
            username_field = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(self.USERNAME_INPUT)
            )
            
            print(f"✅ Campo de usuario encontrado")
            print(f"📍 Visible: {username_field.is_displayed()}")
            print(f"📍 Habilitado: {username_field.is_enabled()}")
            print(f"📍 Placeholder: {username_field.get_attribute('placeholder')}")
            
            # 🆕 HACER CLIC EN EL CAMPO PRIMERO
            print("🖱️ Haciendo clic en el campo de usuario...")
            try:
                # Intentar con ActionChains para un clic más preciso
                actions = ActionChains(self.driver)
                actions.move_to_element(username_field).click().perform()
                time.sleep(0.5)
            except:
                # Si falla ActionChains, intentar clic directo
                username_field.click()
                time.sleep(0.5)
            
            # LIMPIAR CAMPO (por si acaso hay texto)
            username_field.clear()
            time.sleep(0.5)
            
            # INGRESAR USUARIO
            print("📝 Ingresando usuario...")
            username_field.send_keys(username)
            time.sleep(1)
            
            # VERIFICAR QUE EL USUARIO SE INGRESÓ CORRECTAMENTE
            entered_value = username_field.get_attribute('value')
            print(f"🔍 Valor ingresado en campo usuario: '{entered_value}'")
            
            if entered_value == username:
                self.logger.info(f"✅ Usuario ingresado correctamente: {username}")
                print(f"✅ USUARIO CONFIRMADO: '{entered_value}'")
                return True
            else:
                self.logger.error(f"❌ Usuario no se ingresó correctamente. Esperado: {username}, Obtenido: {entered_value}")
                print(f"❌ ERROR: Usuario no coincide. Esperado: '{username}', Obtenido: '{entered_value}'")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error ingresando usuario: {e}")
            print(f"❌ Error ingresando usuario: {e}")
            print(f"📍 URL actual en el error: {self.driver.current_url}")
            
            # TOMAR CAPTURA EN CASO DE ERROR
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="error_ingresar_usuario",
                attachment_type=allure.attachment_type.PNG
            )
            return False

    @allure.step("Ingresar contraseña")
    def enter_password(self, password):
        """Ingresar contraseña en el campo correspondiente"""
        try:
            print("🔍 Buscando campo de contraseña...")
            
            # 🆕 VERIFICAR QUE ESTAMOS EN LA PÁGINA CORRECTA
            current_url = self.driver.current_url
            print(f"📍 URL actual: {current_url}")
            
            if "hydra.uat-lifemiles.net" not in current_url:
                print("❌ ERROR: No estamos en la página de login de hydra")
                return False
            
            # 🆕 BUSCAR DIRECTAMENTE EN EL DOM PRINCIPAL
            password_field = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(self.PASSWORD_INPUT)
            )
            
            print(f"✅ Campo de contraseña encontrado")
            print(f"📍 Visible: {password_field.is_displayed()}")
            print(f"📍 Habilitado: {password_field.is_enabled()}")
            print(f"📍 Placeholder: {password_field.get_attribute('placeholder')}")
            
            # 🆕 HACER CLIC EN EL CAMPO PRIMERO
            print("🖱️ Haciendo clic en el campo de contraseña...")
            try:
                # Intentar con ActionChains para un clic más preciso
                actions = ActionChains(self.driver)
                actions.move_to_element(password_field).click().perform()
                time.sleep(0.5)
            except:
                # Si falla ActionChains, intentar clic directo
                password_field.click()
                time.sleep(0.5)
            
            # LIMPIAR CAMPO (por si acaso hay texto)
            password_field.clear()
            time.sleep(0.5)
            
            # INGRESAR CONTRASEÑA
            print("📝 Ingresando contraseña...")
            password_field.send_keys(password)
            time.sleep(1)
            
            # VERIFICAR QUE LA CONTRASEÑA SE INGRESÓ CORRECTAMENTE
            entered_value = password_field.get_attribute('value')
            # Para contraseñas, solo verificamos que no esté vacío (por seguridad)
            if entered_value:
                self.logger.info("✅ Contraseña ingresada correctamente")
                print("✅ CONTRASEÑA CONFIRMADA: [valor ingresado correctamente]")
                return True
            else:
                self.logger.error("❌ Contraseña no se ingresó correctamente - campo vacío")
                print("❌ ERROR: Contraseña no se ingresó - campo vacío")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error ingresando contraseña: {e}")
            print(f"❌ Error ingresando contraseña: {e}")
            print(f"📍 URL actual en el error: {self.driver.current_url}")
            
            # TOMAR CAPTURA EN CASO DE ERROR
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="error_ingresar_contrasena",
                attachment_type=allure.attachment_type.PNG
            )
            return False

    @allure.step("Hacer clic en botón 'Iniciar sesión' del modal")
    def click_modal_login_button(self):
        """Hacer clic en el botón de login dentro del modal"""
        try:
            print("🔍 Buscando botón de login del modal...")
            
            # 🆕 VERIFICAR QUE ESTAMOS EN LA PÁGINA CORRECTA
            current_url = self.driver.current_url
            print(f"📍 URL actual: {current_url}")
            
            if "hydra.uat-lifemiles.net" not in current_url:
                print("❌ ERROR: No estamos en la página de login de hydra")
                return False
            
            # 🆕 BUSCAR DIRECTAMENTE EN EL DOM PRINCIPAL
            login_button = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(self.MODAL_LOGIN_BUTTON)
            )
            
            print(f"✅ Botón de login encontrado")
            print(f"📍 Texto del botón: '{login_button.text}'")
            print(f"📍 Botón habilitado: {login_button.is_enabled()}")
            print(f"📍 Botón visible: {login_button.is_displayed()}")
            
            login_button.click()
            self.logger.info("✅ Clic en botón de login del modal realizado")
            print("✅ Clic en botón de login del modal realizado")
            
            # Esperar después del login
            time.sleep(3)
            return True
                
        except Exception as e:
            self.logger.error(f"❌ Error haciendo clic en botón de login del modal: {e}")
            print(f"❌ Error haciendo clic en botón de login del modal: {e}")
            print(f"📍 URL actual en el error: {self.driver.current_url}")
            return False

    @allure.step("Verificar si estamos en la página de login de hydra")
    def is_on_hydra_login_page(self):
        """Verificar si estamos en la página de login de hydra"""
        current_url = self.driver.current_url
        is_hydra = "hydra.uat-lifemiles.net" in current_url
        print(f"🔍 Verificando página de login: {current_url}")
        print(f"✅ ¿Estamos en hydra?: {is_hydra}")
        return is_hydra

    @allure.step("Verificar que los campos de login son visibles")
    def are_login_fields_visible(self):
        """Verificar que los campos de usuario y contraseña son visibles"""
        try:
            username_visible = self.wait_for_element(self.USERNAME_INPUT, 5).is_displayed()
            password_visible = self.wait_for_element(self.PASSWORD_INPUT, 5).is_displayed()
            login_button_visible = self.wait_for_element(self.MODAL_LOGIN_BUTTON, 5).is_displayed()
            
            print(f"🔍 Campo usuario visible: {username_visible}")
            print(f"🔍 Campo contraseña visible: {password_visible}")
            print(f"🔍 Botón login visible: {login_button_visible}")
            
            return username_visible and password_visible and login_button_visible
        except Exception as e:
            print(f"❌ Error verificando campos visibles: {e}")
            return False
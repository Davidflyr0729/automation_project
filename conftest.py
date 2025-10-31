import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def pytest_addoption(parser):
    """Añadir opciones de línea de comandos"""
    parser.addoption("--headless", action="store_true", help="Run in headless mode")
    parser.addoption("--browser", action="store", default="chrome", help="Browser to use: chrome or firefox")

@pytest.fixture
def browser(request):
    """Fixture para inicializar navegador en modo DESKTOP"""
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    print(f"\n🚀 Iniciando {browser_name.upper()} (headless: {headless}) - MODO DESKTOP")
    
    driver = None
    
    try:
        if browser_name.lower() == 'chrome':
            driver = _setup_chrome_desktop(headless)
        elif browser_name.lower() == 'firefox':
            driver = _setup_firefox_desktop(headless)
        else:
            raise ValueError(f"Navegador no soportado: {browser_name}")
        
        print(f"✅ {browser_name.upper()} inicializado correctamente en modo DESKTOP")
        
        # ENTREGAR EL DRIVER AL TEST
        yield driver
        
        # CERRAR EL NAVEGADOR DESPUÉS DEL TEST
        print("🔴 Cerrando navegador")
        driver.quit()
        
    except Exception as e:
        print(f"❌ Error inicializando {browser_name}: {e}")
        raise

def _setup_chrome_desktop(headless=False):
    """Configurar Chrome en modo DESKTOP"""
    # RUTA AL CHROMEDRIVER MANUAL
    chrome_driver_path = os.path.join(os.getcwd(), "drivers", "chromedriver.exe")
    
    # VERIFICAR QUE EL CHROMEDRIVER EXISTE
    if not os.path.exists(chrome_driver_path):
        raise FileNotFoundError(
            f"❌ ChromeDriver no encontrado en: {chrome_driver_path}\n"
            "💡 Asegúrate de que chromedriver.exe está en la carpeta 'drivers'\n"
            "💡 Descarga desde: https://chromedriver.chromium.org/"
        )
    
    print(f"✅ Usando ChromeDriver manual: {chrome_driver_path}")
    
    # CONFIGURAR OPCIONES DE CHROME PARA DESKTOP
    options = Options()
    
    # CONFIGURACIÓN PARA DESKTOP
    options.add_argument("--window-size=1920,1080")  # Tamaño desktop estándar
    options.add_argument("--start-maximized")        # Maximizar ventana
    
    # USER AGENT DE DESKTOP (Chrome en Windows)
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Configuración headless
    if headless:
        options.add_argument("--headless=new")
    
    # OPCIONES DE SEGURIDAD Y RENDIMIENTO
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # DESHABILITAR EXTENSIONES Y NOTIFICACIONES
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    
    # PREFERENCIAS ADICIONALES PARA DESKTOP
    prefs = {
        "profile.default_content_setting_values.notifications": 2,  # Bloquear notificaciones
        "credentials_enable_service": False,  # Deshabilitar guardado de contraseñas
        "profile.password_manager_enabled": False,
        "autofill.profile_enabled": False
    }
    options.add_experimental_option("prefs", prefs)
    
    # INICIALIZAR CHROME CON CHROMEDRIVER MANUAL
    service = ChromeService(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    
    # EJECUTAR SCRIPT PARA OCULTAR WEBDRIVER
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    # CONFIGURAR TIEMPOS DE ESPERA
    driver.implicitly_wait(10)
    
    # MAXIMIZAR VENTANA SI NO ESTÁ EN HEADLESS
    if not headless:
        driver.maximize_window()
    
    return driver

def _setup_firefox_desktop(headless=False):
    """Configurar Firefox en modo DESKTOP"""
    # RUTA AL GECKODRIVER MANUAL
    gecko_driver_path = os.path.join(os.getcwd(), "drivers", "geckodriver.exe")
    
    # VERIFICAR QUE EL GECKODRIVER EXISTE
    if not os.path.exists(gecko_driver_path):
        raise FileNotFoundError(
            f"❌ GeckoDriver no encontrado en: {gecko_driver_path}\n"
            "💡 Asegúrate de que geckodriver.exe está en la carpeta 'drivers'\n"
            "💡 Descarga desde: https://github.com/mozilla/geckodriver/releases"
        )
    
    print(f"✅ Usando GeckoDriver manual: {gecko_driver_path}")
    
    # CONFIGURAR OPCIONES DE FIREFOX PARA DESKTOP
    options = FirefoxOptions()
    
    # CONFIGURACIÓN PARA DESKTOP
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")
    
    # USER AGENT DE DESKTOP (Firefox en Windows)
    options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0")
    
    # Configuración headless
    if headless:
        options.add_argument("--headless")
    
    # PREFERENCIAS ADICIONALES PARA DESKTOP
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference('useAutomationExtension', False)
    options.set_preference("dom.push.enabled", False)  # Deshabilitar notificaciones push
    
    # INICIALIZAR FIREFOX CON GECKODRIVER MANUAL
    service = FirefoxService(executable_path=gecko_driver_path)
    driver = webdriver.Firefox(service=service, options=options)
    
    # CONFIGURAR TAMAÑO DE VENTANA
    driver.set_window_size(1920, 1080)
    
    # CONFIGURAR TIEMPOS DE ESPERA
    driver.implicitly_wait(10)
    
    # MAXIMIZAR VENTANA SI NO ESTÁ EN HEADLESS
    if not headless:
        driver.maximize_window()
    
    return driver
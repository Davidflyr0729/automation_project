import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

def pytest_addoption(parser):
    """Añadir opciones de línea de comandos"""
    parser.addoption("--headless", action="store_true", help="Run in headless mode")

@pytest.fixture
def browser(request):
    """Fixture para inicializar Chrome con ChromeDriver MANUAL"""
    headless = request.config.getoption("--headless")
    
    print(f"\n🚀 Iniciando Chrome (headless: {headless})")
    
    # RUTA AL CHROMEDRIVER MANUAL QUE YA TIENES DESCARGADO
    chrome_driver_path = os.path.join(os.getcwd(), "drivers", "chromedriver.exe")
    
    # VERIFICAR QUE EL CHROMEDRIVER EXISTE
    if not os.path.exists(chrome_driver_path):
        raise FileNotFoundError(
            f"❌ ChromeDriver no encontrado en: {chrome_driver_path}\n"
            "💡 Asegúrate de que chromedriver.exe está en la carpeta 'drivers'\n"
            "💡 Descarga desde: https://chromedriver.chromium.org/"
        )
    
    print(f"✅ Usando ChromeDriver manual: {chrome_driver_path}")
    
    # CONFIGURAR OPCIONES DE CHROME
    options = webdriver.ChromeOptions()
    
    # Configuración headless
    if headless:
        options.add_argument("--headless=new")
    
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    try:
        # INICIALIZAR CHROME CON CHROMEDRIVER MANUAL
        service = ChromeService(executable_path=chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        
        # CONFIGURAR EL DRIVER
        driver.implicitly_wait(10)
        if not headless:
            driver.maximize_window()
        
        print("✅ Chrome inicializado correctamente")
        
        # ENTREGAR EL DRIVER AL TEST
        yield driver
        
        # CERRAR EL NAVEGADOR DESPUÉS DEL TEST
        print("🔴 Cerrando Chrome")
        driver.quit()
        
    except Exception as e:
        print(f"❌ Error inicializando Chrome: {e}")
        print(f"💡 Verifica que ChromeDriver es compatible con tu versión de Chrome")
        raise
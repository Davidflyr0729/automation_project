import os
import pytest
import sqlite3
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Configurar logging
logger = logging.getLogger(__name__)

def pytest_addoption(parser):
    """Añadir opciones de línea de comandos"""
    parser.addoption("--headless", action="store_true", help="Run in headless mode")
    parser.addoption("--browser", action="store", default="chrome", help="Browser to use: chrome or firefox")
    parser.addoption("--base-url", action="store", default="https://nuxqa4.avtest.ink/", help="Base URL for testing")

def pytest_configure(config):
    """Configuración de pytest para los marcadores"""
    config.addinivalue_line(
        "markers", "footer: Tests relacionados con el footer"
    )
    config.addinivalue_line(
        "markers", "redirects: Tests de redirecciones"
    )
    config.addinivalue_line(
        "markers", "language: Tests de idiomas"
    )
    config.addinivalue_line(
        "markers", "debug: Tests de diagnóstico"
    )
    config.addinivalue_line(
        "markers", "comprehensive: Tests comprehensivos"
    )
    config.addinivalue_line(
        "markers", "header: Tests relacionados con el header"
    )
    config.addinivalue_line(
        "markers", "pos: Tests de cambio de POS/País"
    )
    config.addinivalue_line(
        "markers", "booking: Tests de booking"
    )
    config.addinivalue_line(
        "markers", "login: Tests de login"
    )

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

@pytest.fixture
def base_url(request):
    """Fixture para obtener la URL base de las pruebas"""
    return request.config.getoption("--base-url")

class TestDatabase:
    """Clase para manejar la base de datos SQLite de resultados de pruebas"""
    
    def __init__(self, db_path="test_results.db"):
        self.db_path = db_path
        self.connection = None
        self.setup_database()
    
    def setup_database(self):
        """Configurar la base de datos y crear tabla si no existe"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            cursor = self.connection.cursor()
            
            # Crear tabla de resultados de pruebas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS test_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    test_case TEXT NOT NULL,
                    status TEXT NOT NULL,
                    details TEXT,
                    additional_info TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    browser TEXT,
                    headless BOOLEAN
                )
            ''')
            
            self.connection.commit()
            logger.info("✅ Base de datos configurada correctamente")
            
        except Exception as e:
            logger.error(f"❌ Error configurando base de datos: {e}")
            raise
    
    def save_test_result(self, test_case, status, details="", additional_info="", browser="chrome", headless=False):
        """Guardar resultado de prueba en la base de datos"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO test_results 
                (test_case, status, details, additional_info, browser, headless)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (test_case, status, details, additional_info, browser, headless))
            
            self.connection.commit()
            logger.info(f"✅ Resultado guardado en BD: {test_case} - {status}")
            
        except Exception as e:
            logger.error(f"❌ Error guardando resultado en BD: {e}")
    
    def get_test_results(self, test_case=None):
        """Obtener resultados de pruebas de la base de datos"""
        try:
            cursor = self.connection.cursor()
            
            if test_case:
                cursor.execute('''
                    SELECT * FROM test_results 
                    WHERE test_case = ? 
                    ORDER BY timestamp DESC
                ''', (test_case,))
            else:
                cursor.execute('''
                    SELECT * FROM test_results 
                    ORDER BY timestamp DESC
                ''')
            
            return cursor.fetchall()
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo resultados de BD: {e}")
            return []
    
    def close(self):
        """Cerrar conexión a la base de datos"""
        if self.connection:
            self.connection.close()
            logger.info("🔴 Conexión a BD cerrada")

@pytest.fixture(scope="session")
def setup_database():
    """Fixture para configurar y proporcionar acceso a la base de datos"""
    database = TestDatabase()
    yield database
    database.close()

@pytest.fixture
def driver(browser):
    """Alias para el fixture browser (para compatibilidad)"""
    return browser

@pytest.fixture(autouse=True)
def log_test_execution(request, setup_database):
    """Fixture automático para registrar ejecución de tests en BD"""
    test_name = request.node.name
    logger.info(f"🧪 Ejecutando test: {test_name}")
    
    # Ejecutar el test
    yield
    
    # Verificar resultado del test y guardar en BD
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        status = "FAILED"
        details = f"Test falló: {test_name}"
    else:
        status = "PASSED" 
        details = f"Test exitoso: {test_name}"
    
    # Guardar resultado en BD
    setup_database.save_test_result(
        test_case=test_name,
        status=status,
        details=details,
        additional_info=f"Método: {request.node.originalname if hasattr(request.node, 'originalname') else 'N/A'}"
    )

def pytest_html_report_title(report):
    """Configurar título del reporte HTML"""
    report.title = "Pruebas Automatizadas - FLYR"

def pytest_configure(config):
    """Configuración adicional de pytest"""
    # Configurar opciones para reportes Allure si están disponibles
    if hasattr(config, 'option') and config.option.allure_report_dir:
        import allure
        allure.dynamic.title("Pruebas Automatizadas FLYR")
        allure.dynamic.description("Suite de pruebas automatizadas para el sitio FLYR")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook para obtener el resultado de los tests para Allure"""
    outcome = yield
    rep = outcome.get_result()
    
    # Guardar screenshot en caso de fallo
    if rep.when == "call" and rep.failed:
        try:
            # Intentar obtener el driver del test
            if 'driver' in item.funcargs:
                driver = item.funcargs['driver']
                take_screenshot_on_failure(driver, item.name)
        except Exception as e:
            logger.warning(f"No se pudo tomar screenshot: {e}")

def take_screenshot_on_failure(driver, test_name):
    """Tomar screenshot cuando un test falla"""
    try:
        screenshot_dir = "screenshots/failures"
        os.makedirs(screenshot_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{screenshot_dir}/{test_name}_{timestamp}.png"
        
        driver.save_screenshot(filename)
        logger.info(f"📸 Screenshot guardado: {filename}")
        
        # Adjuntar screenshot a Allure si está disponible
        try:
            import allure
            allure.attach.file(
                filename, 
                name=f"Screenshot_{test_name}",
                attachment_type=allure.attachment_type.PNG
            )
        except ImportError:
            pass
            
    except Exception as e:
        logger.error(f"Error tomando screenshot: {e}")

# Configuración para ejecución en paralelo con xdist
def pytest_sessionstart(session):
    """Ejecutar al inicio de la sesión de pruebas"""
    logger.info("🚀 Iniciando sesión de pruebas automatizadas")
    
    # Crear directorios necesarios
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("allure-results", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

def pytest_sessionfinish(session, exitstatus):
    """Ejecutar al finalizar la sesión de pruebas"""
    logger.info("🏁 Sesión de pruebas finalizada")
    
    # Mostrar resumen de resultados si la BD está disponible
    try:
        database = TestDatabase()
        results = database.get_test_results()
        
        if results:
            passed = sum(1 for r in results if r[2] == "PASSED")
            failed = sum(1 for r in results if r[2] == "FAILED")
            total = len(results)
            
            logger.info(f"📊 RESUMEN FINAL: {passed}/{total} pasaron, {failed}/{total} fallaron")
        database.close()
    except Exception as e:
        logger.warning(f"No se pudo generar resumen: {e}")
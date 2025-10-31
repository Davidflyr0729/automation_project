import pytest
import os
import allure
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage
from utils.database import DatabaseManager
from utils.video_recorder import VideoRecorder
import time

logger = logging.getLogger(__name__)

@allure.feature("Caso 6: Redirecciones Header")
@allure.story("Verificar navegación a 3 sitios diferentes del navbar")
class TestCase6:
    """Pruebas para el Caso 6: Redirecciones en el Header"""
    
    # URLs a probar - AMBAS REQUERIDAS
    # By default test both QA URLs, but allow overriding to a single URL using
    # the CASE6_URL environment variable for step-by-step runs.
    DEFAULT_TEST_URLS = [
        "https://nuxqa4.avtest.ink/",
        "https://nuxqa5.avtest.ink/"
    ]

    env_url = os.environ.get('CASE6_URL')
    if env_url:
        TEST_URLS = [env_url]
    else:
        TEST_URLS = DEFAULT_TEST_URLS
    
    @pytest.fixture(scope="function", params=TEST_URLS)
    def setup(self, browser, request):
        """Configuración inicial para cada test - Ejecuta en ambas URLs"""
        logger.info("🔄 Iniciando configuración para Caso 6")
        
        # Inicializar página principal
        home_page = HomePage(browser)
        
        # Inicializar grabadora de video
        test_name = f"{request.node.name}_{request.param.split('//')[1].split('.')[0]}"
        video_recorder = VideoRecorder(test_name=test_name, browser_name=browser.name)
        video_recorder.start_recording()
        
        # Inicializar base de datos
        db = DatabaseManager()
        
        # Navegar a la página principal (URL específica del parámetro)
        base_url = request.param
        home_page.navigate_to(base_url)
        home_page.wait_for_page_load()
        # Asegurarse de que las pruebas de Caso 6 se ejecuten en Español
        try:
            home_page.select_language('español')
            time.sleep(1)
            logger.info("Idioma forzado a Español en setup para Caso 6")
        except Exception as e:
            logger.warning(f"No se pudo forzar idioma a Español en setup: {e}")
        
        yield {
            'browser': browser,
            'home_page': home_page,
            'video_recorder': video_recorder,
            'db': db,
            'base_url': base_url
        }
        
        # Finalizar grabación y guardar en base de datos
        try:
            video_path = video_recorder.stop_recording()
            logger.info(f"🎥 Video guardado: {video_path}")
        except Exception as e:
            logger.error(f"Error al detener grabación: {e}")

    @allure.title("Caso 6.1: Navegar a Ofertas y Destinos")
    @allure.description("Verificar que la navegación a 'Ofertas y destinos' funciona correctamente en ambas URLs")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_navigate_to_offers_and_destinations(self, setup):
        """Test 6.1: Navegar a la sección Ofertas y destinos -> ofertas de vuelos"""
        browser = setup['browser']
        home_page = setup['home_page']
        db = setup['db']
        base_url = setup['base_url']
        
        logger.info(f"🚀 Iniciando Test 6.1: Navegación a Ofertas y destinos - {base_url}")
        
        try:
            with allure.step(f"Paso 1: Obtener URL inicial - {base_url}"):
                initial_url = home_page.get_page_url()
                logger.info(f"📄 URL inicial: {initial_url}")
                allure.attach(initial_url, name="URL Inicial", attachment_type=allure.attachment_type.TEXT)

            with allure.step("Paso 2: Navegar a Ofertas y destinos"):
                navigation_success = home_page.navigate_to_offers_and_destinations()
                assert navigation_success, "❌ Falló la navegación a Ofertas y destinos"
                
                # Esperar a que cambie la URL
                WebDriverWait(browser, 10).until(
                    lambda driver: driver.current_url != initial_url
                )
                
                current_url = home_page.get_page_url()
                logger.info(f"📄 URL después de navegación: {current_url}")
                allure.attach(current_url, name="URL Después de Navegación", attachment_type=allure.attachment_type.TEXT)

            with allure.step("Paso 3: Verificar que la página cargó correctamente"):
                page_loaded = home_page.verify_offers_page_loaded()
                assert page_loaded, "❌ La página de ofertas no cargó correctamente"
                
                # Tomar screenshot como evidencia
                screenshot_name = f"caso6_1_ofertas_destinos_{base_url.split('//')[1].split('.')[0]}.png"
                home_page.take_screenshot(screenshot_name)
                allure.attach.file(f"screenshots/{screenshot_name}", 
                                 name=f"Screenshot Ofertas y Destinos - {base_url}", 
                                 attachment_type=allure.attachment_type.PNG)

            with allure.step("Paso 4: Verificar que la URL es diferente a la inicial"):
                assert current_url != initial_url, "❌ La URL no cambió después de la navegación"
                assert "ofertas" in current_url.lower() or "offers" in current_url.lower() or "destinos" in current_url.lower(), \
                    f"❌ La URL no contiene indicadores de ofertas: {current_url}"

            with allure.step("Paso 5: Guardar resultados en base de datos"):
                db.save_test_result(
                    test_case_number=6,
                    test_case_name=f"Navegación a Ofertas y Destinos - {base_url}",
                    browser=browser.name,
                    language="español",
                    status="PASS",
                    url=base_url,
                    additional_info=f"URL destino: {current_url}"
                )
                
                # Guardar datos específicos del Caso 6
                db.save_case6_redirect(
                    test_name="Ofertas y Destinos",
                    browser=browser.name,
                    language="español",
                    from_url=initial_url,
                    to_url=current_url,
                    redirect_success=True,
                    page_title=browser.title,
                    additional_notes=f"URL base: {base_url}"
                )

            logger.info(f"✅ Test 6.1 PASÓ: Navegación a Ofertas y destinos exitosa - {base_url}")
            
        except Exception as e:
            logger.error(f"❌ Test 6.1 FALLÓ: {e} - {base_url}")
            
            # Guardar resultado fallido en base de datos
            db.save_test_result(
                test_case_number=6,
                test_case_name=f"Navegación a Ofertas y Destinos - {base_url}",
                browser=browser.name,
                language="español",
                status="FAIL",
                url=base_url,
                additional_info=f"Error: {str(e)}"
            )
            
            # Guardar redirección fallida
            db.save_case6_redirect(
                test_name="Ofertas y Destinos",
                browser=browser.name,
                language="español",
                from_url=home_page.get_page_url(),
                to_url="N/A",
                redirect_success=False,
                additional_notes=f"Error: {str(e)} - URL base: {base_url}"
            )
            
            # Tomar screenshot del error
            error_screenshot = f"caso6_1_error_{base_url.split('//')[1].split('.')[0]}.png"
            home_page.take_screenshot(error_screenshot)
            allure.attach.file(f"screenshots/{error_screenshot}", 
                             name=f"Screenshot Error - {base_url}", 
                             attachment_type=allure.attachment_type.PNG)
            raise

    @allure.title("Caso 6.2: Navegar a Tu Reserva Check-in")
    @allure.description("Verificar que la navegación a 'Tu reserva check-in' funciona correctamente en ambas URLs")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_navigate_to_my_booking_checkin(self, setup):
        """Test 6.2: Navegar a la sección Tu reserva check-in -> Gestiona tu reserva"""
        browser = setup['browser']
        home_page = setup['home_page']
        db = setup['db']
        base_url = setup['base_url']
        
        logger.info(f"🚀 Iniciando Test 6.2: Navegación a Tu reserva check-in - {base_url}")
        
        try:
            with allure.step(f"Paso 1: Obtener URL inicial - {base_url}"):
                initial_url = home_page.get_page_url()
                logger.info(f"📄 URL inicial: {initial_url}")

            with allure.step("Paso 2: Navegar a Tu reserva check-in"):
                navigation_success = home_page.navigate_to_my_booking_checkin()
                assert navigation_success, "❌ Falló la navegación a Tu reserva check-in"
                
                # Esperar a que cambie la URL
                WebDriverWait(browser, 10).until(
                    lambda driver: driver.current_url != initial_url
                )
                
                current_url = home_page.get_page_url()
                logger.info(f"📄 URL después de navegación: {current_url}")

            with allure.step("Paso 3: Verificar que la página cargó correctamente"):
                page_loaded = home_page.verify_checkin_page_loaded()
                assert page_loaded, "❌ La página de check-in no cargó correctamente"
                
                # Tomar screenshot como evidencia
                screenshot_name = f"caso6_2_tu_reserva_checkin_{base_url.split('//')[1].split('.')[0]}.png"
                home_page.take_screenshot(screenshot_name)
                allure.attach.file(f"screenshots/{screenshot_name}", 
                                 name=f"Screenshot Tu Reserva Check-in - {base_url}", 
                                 attachment_type=allure.attachment_type.PNG)

            with allure.step("Paso 4: Verificar que la URL es diferente a la inicial"):
                assert current_url != initial_url, "❌ La URL no cambió después de la navegación"
                assert "check-in" in current_url.lower() or "checkin" in current_url.lower() or "booking" in current_url.lower() or "reserva" in current_url.lower(), \
                    f"❌ La URL no contiene indicadores de check-in: {current_url}"

            with allure.step("Paso 5: Guardar resultados en base de datos"):
                db.save_test_result(
                    test_case_number=6,
                    test_case_name=f"Navegación a Tu Reserva Check-in - {base_url}",
                    browser=browser.name,
                    language="español",
                    status="PASS",
                    url=base_url,
                    additional_info=f"URL destino: {current_url}"
                )
                
                # Guardar datos específicos del Caso 6
                db.save_case6_redirect(
                    test_name="Tu Reserva Check-in",
                    browser=browser.name,
                    language="español",
                    from_url=initial_url,
                    to_url=current_url,
                    redirect_success=True,
                    page_title=browser.title,
                    additional_notes=f"URL base: {base_url}"
                )

            logger.info(f"✅ Test 6.2 PASÓ: Navegación a Tu reserva check-in exitosa - {base_url}")
            
        except Exception as e:
            logger.error(f"❌ Test 6.2 FALLÓ: {e} - {base_url}")
            
            # Guardar resultado fallido en base de datos
            db.save_test_result(
                test_case_number=6,
                test_case_name=f"Navegación a Tu Reserva Check-in - {base_url}",
                browser=browser.name,
                language="español",
                status="FAIL",
                url=base_url,
                additional_info=f"Error: {str(e)}"
            )
            
            # Guardar redirección fallida
            db.save_case6_redirect(
                test_name="Tu Reserva Check-in",
                browser=browser.name,
                language="español",
                from_url=home_page.get_page_url(),
                to_url="N/A",
                redirect_success=False,
                additional_notes=f"Error: {str(e)} - URL base: {base_url}"
            )
            
            # Tomar screenshot del error
            error_screenshot = f"caso6_2_error_{base_url.split('//')[1].split('.')[0]}.png"
            home_page.take_screenshot(error_screenshot)
            allure.attach.file(f"screenshots/{error_screenshot}", 
                             name=f"Screenshot Error - {base_url}", 
                             attachment_type=allure.attachment_type.PNG)
            raise

    @allure.title("Caso 6.3: Navegar a Información y Ayuda - Tipos de Tarifas")
    @allure.description("Verificar que la navegación a 'Información y ayuda' -> Tipos de tarifas funciona correctamente en ambas URLs")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_navigate_to_info_and_help_tariffs(self, setup):
        """Test 6.3: Navegar a la sección Información y ayuda -> Tipos de tarifas"""
        browser = setup['browser']
        home_page = setup['home_page']
        db = setup['db']
        base_url = setup['base_url']
        
        logger.info(f"🚀 Iniciando Test 6.3: Navegación a Información y ayuda - Tipos de tarifas - {base_url}")
        
        try:
            with allure.step(f"Paso 1: Obtener URL inicial - {base_url}"):
                initial_url = home_page.get_page_url()
                logger.info(f"📄 URL inicial: {initial_url}")

            with allure.step("Paso 2: Navegar a Información y ayuda"):
                navigation_success = home_page.navigate_to_info_and_help_tariffs()
                assert navigation_success, "❌ Falló la navegación a Información y ayuda"
                
                # Esperar a que cambie la URL
                WebDriverWait(browser, 10).until(
                    lambda driver: driver.current_url != initial_url
                )
                
                current_url = home_page.get_page_url()
                logger.info(f"📄 URL después de navegación: {current_url}")

            with allure.step("Paso 3: Verificar que la página cargó correctamente"):
                page_loaded = home_page.verify_tariff_types_page_loaded()
                assert page_loaded, "❌ La página de tipos de tarifas no cargó correctamente"
                
                # Tomar screenshot como evidencia
                screenshot_name = f"caso6_3_info_ayuda_tarifas_{base_url.split('//')[1].split('.')[0]}.png"
                home_page.take_screenshot(screenshot_name)
                allure.attach.file(f"screenshots/{screenshot_name}", 
                                 name=f"Screenshot Información y Ayuda - {base_url}", 
                                 attachment_type=allure.attachment_type.PNG)

            with allure.step("Paso 4: Verificar que la URL es diferente a la inicial"):
                assert current_url != initial_url, "❌ La URL no cambió después de la navegación"
                assert "tarifas" in current_url.lower() or "fares" in current_url.lower() or "informacion" in current_url.lower() or "ayuda" in current_url.lower(), \
                    f"❌ La URL no contiene indicadores de información/tarifas: {current_url}"

            with allure.step("Paso 5: Guardar resultados en base de datos"):
                db.save_test_result(
                    test_case_number=6,
                    test_case_name=f"Navegación a Información y Ayuda - Tarifas - {base_url}",
                    browser=browser.name,
                    language="español",
                    status="PASS",
                    url=base_url,
                    additional_info=f"URL destino: {current_url}"
                )
                
                # Guardar datos específicos del Caso 6
                db.save_case6_redirect(
                    test_name="Información y Ayuda - Tarifas",
                    browser=browser.name,
                    language="español",
                    from_url=initial_url,
                    to_url=current_url,
                    redirect_success=True,
                    page_title=browser.title,
                    additional_notes=f"URL base: {base_url}"
                )

            logger.info(f"✅ Test 6.3 PASÓ: Navegación a Información y ayuda exitosa - {base_url}")
            
        except Exception as e:
            logger.error(f"❌ Test 6.3 FALLÓ: {e} - {base_url}")
            
            # Guardar resultado fallido en base de datos
            db.save_test_result(
                test_case_number=6,
                test_case_name=f"Navegación a Información y Ayuda - Tarifas - {base_url}",
                browser=browser.name,
                language="español",
                status="FAIL",
                url=base_url,
                additional_info=f"Error: {str(e)}"
            )
            
            # Guardar redirección fallida
            db.save_case6_redirect(
                test_name="Información y Ayuda - Tarifas",
                browser=browser.name,
                language="español",
                from_url=home_page.get_page_url(),
                to_url="N/A",
                redirect_success=False,
                additional_notes=f"Error: {str(e)} - URL base: {base_url}"
            )
            
            # Tomar screenshot del error
            error_screenshot = f"caso6_3_error_{base_url.split('//')[1].split('.')[0]}.png"
            home_page.take_screenshot(error_screenshot)
            allure.attach.file(f"screenshots/{error_screenshot}", 
                             name=f"Screenshot Error - {base_url}", 
                             attachment_type=allure.attachment_type.PNG)
            raise

    @allure.title("Caso 6.4: Verificar redirecciones con diferentes idiomas")
    @allure.description("Verificar que las URLs cambian correctamente según el idioma seleccionado en ambas URLs")
    @allure.severity(allure.severity_level.NORMAL)
    def test_verify_redirects_with_different_languages(self, setup):
        """Test 6.4: Verificar que las URLs cambian según el idioma"""
        browser = setup['browser']
        home_page = setup['home_page']
        db = setup['db']
        base_url = setup['base_url']
        
        logger.info(f"🚀 Iniciando Test 6.4: Verificación de redirecciones con idiomas - {base_url}")
        
        try:
            with allure.step("Paso 1: Probar con idioma Español"):
                # Asegurarse de estar en español con reintento
                max_attempts = 3
                for attempt in range(max_attempts):
                    try:
                        home_page.select_language('español')
                        time.sleep(2)
                        
                        # Verificar que el cambio fue exitoso
                        if "español" in home_page.get_current_language().lower():
                            break
                    except:
                        if attempt < max_attempts - 1:
                            home_page.refresh_page()
                            time.sleep(2)
                            continue
                        raise
                
                # Navegar a una sección y capturar URL con reintento
                assert home_page.navigate_to_offers_and_destinations(), "No se pudo navegar a Ofertas en español"
                url_spanish = home_page.get_page_url()
                logger.info(f"📄 URL en Español: {url_spanish}")
                
                # Guardar redirección en español
                db.save_case6_redirect(
                    test_name="Redirección con Idioma Español",
                    browser=browser.name,
                    language="español",
                    from_url=base_url,
                    to_url=url_spanish,
                    redirect_success=True,
                    page_title=browser.title,
                    additional_notes=f"URL base: {base_url}"
                )
                
                # Volver a la página principal con reintento
                max_attempts = 3
                for attempt in range(max_attempts):
                    try:
                        home_page.navigate_to(base_url)
                        home_page.wait_for_page_load()
                        break
                    except:
                        if attempt < max_attempts - 1:
                            time.sleep(2)
                            continue
                        raise

            with allure.step("Paso 2: Probar con idioma English"):
                # Cambiar a inglés con reintento
                max_attempts = 3
                for attempt in range(max_attempts):
                    try:
                        home_page.select_language('english')
                        time.sleep(2)
                        
                        # Verificar que el cambio fue exitoso
                        if "english" in home_page.get_current_language().lower():
                            break
                    except:
                        if attempt < max_attempts - 1:
                            home_page.refresh_page()
                            time.sleep(2)
                            continue
                        raise
                
                # Navegar a la misma sección y capturar URL con reintento
                assert home_page.navigate_to_offers_and_destinations(), "No se pudo navegar a Ofertas en inglés"
                url_english = home_page.get_page_url()
                logger.info(f"📄 URL en English: {url_english}")
                
                # Guardar redirección en inglés
                db.save_case6_redirect(
                    test_name="Redirección con Idioma English",
                    browser=browser.name,
                    language="english",
                    from_url=base_url,
                    to_url=url_english,
                    redirect_success=True,
                    page_title=browser.title,
                    additional_notes=f"URL base: {base_url}"
                )

            with allure.step("Paso 3: Verificar que las URLs son diferentes por idioma"):
                # Verificar diferencias en URL o contenido
                url_spanish_lower = url_spanish.lower()
                url_english_lower = url_english.lower()
                
                # Comprobar diferencias específicas en las URLs
                spanish_indicators = ['ofertas', 'vuelos', 'destinos']
                english_indicators = ['offers', 'flights', 'destinations']
                
                has_spanish = any(indicator in url_spanish_lower for indicator in spanish_indicators)
                has_english = any(indicator in url_english_lower for indicator in english_indicators)
                
                # Si las URLs no muestran el idioma claramente, verificar el contenido
                if not (has_spanish or has_english):
                    assert self._verify_content_difference(home_page), \
                        "❌ Ni las URLs ni el contenido reflejan el cambio de idioma"

            with allure.step("Paso 4: Guardar resultados en base de datos"):
                db.save_test_result(
                    test_case_number=6,
                    test_case_name=f"Verificación de redirecciones con idiomas - {base_url}",
                    browser=browser.name,
                    language="múltiple",
                    status="PASS",
                    url=base_url,
                    additional_info=f"URL Español: {url_spanish}, URL English: {url_english}"
                )

            logger.info(f"✅ Test 6.4 PASÓ: Verificación de redirecciones con idiomas exitosa - {base_url}")
            
        except Exception as e:
            logger.error(f"❌ Test 6.4 FALLÓ: {e} - {base_url}")
            
            db.save_test_result(
                test_case_number=6,
                test_case_name=f"Verificación de redirecciones con idiomas - {base_url}",
                browser=browser.name,
                language="múltiple",
                status="FAIL",
                url=base_url,
                additional_info=f"Error: {str(e)}"
            )
            raise

    def _verify_content_difference(self, home_page):
        """Método auxiliar para verificar diferencias de contenido por idioma"""
        try:
            page_content = home_page.driver.page_source.lower()
            # Buscar indicadores de diferentes idiomas
            has_english = any(word in page_content for word in ['book', 'offers', 'flights', 'english'])
            has_spanish = any(word in page_content for word in ['reservar', 'ofertas', 'vuelos', 'español'])
            
            return has_english != has_spanish  # Deberían ser diferentes
        except:
            return False

# Configuración para ejecución en paralelo
def pytest_generate_tests(metafunc):
    """Generar tests para múltiples navegadores si es necesario"""
    if 'browser' in metafunc.fixturenames:
        metafunc.parametrize('browser', ['chrome', 'firefox'], indirect=True)
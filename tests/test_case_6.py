import pytest
import os
import allure
import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pages.home_page import HomePage
from utils.database import DatabaseManager
from utils.video_recorder import VideoRecorder

logger = logging.getLogger(__name__)


@allure.feature("Caso 6: Navegación en Navbar")
class TestCase6:
    """Tests para navegación en el navbar - Ofertas de vuelos, Check-in e Información y ayuda"""

    # URLs a testear
    URLS = [
        "https://nuxqa4.avtest.ink/",
        "https://nuxqa5.avtest.ink/"
    ]

    @pytest.fixture(scope="function", params=URLS)
    def setup(self, browser, request):
        """Setup: Prepara el entorno para cada URL"""
        base_url = request.param
        url_name = "nuxqa4" if "nuxqa4" in base_url else "nuxqa5"
        
        logger.info(f"Iniciando setup - Caso 6 (URL: {base_url})")
        
        home_page = HomePage(browser)
        
        # Configurar video recording
        test_name = f"caso6_{url_name}_{browser.name}"
        video_recorder = VideoRecorder(test_name=test_name, browser_name=browser.name)
        
        # Configurar base de datos
        db = DatabaseManager()

        try:
            # Iniciar grabación de video
            video_recorder.start_recording()
        except Exception as e:
            logger.warning(f"No se pudo iniciar VideoRecorder: {e}")

        # Navegar a la URL base
        home_page.navigate_to(base_url)
        home_page.wait_for_page_load()

        # Verificar y forzar idioma español si es necesario
        current_url = home_page.get_page_url()
        logger.info(f"URL actual: {current_url}")
        
        if not current_url.endswith('/es/'):
            try:
                logger.info("Forzando idioma a español...")
                home_page.select_language('español')
                time.sleep(3)
                # Verificar que cambió a español
                new_url = home_page.get_page_url()
                logger.info(f"URL después de cambiar idioma: {new_url}")
            except Exception as e:
                logger.warning(f"No se pudo forzar idioma a Español: {e}")

        yield {
            'browser': browser,
            'home_page': home_page,
            'video_recorder': video_recorder,
            'db': db,
            'base_url': base_url,
            'url_name': url_name  # Asegurar que esta línea está presente
        }

        # Teardown: detener grabación
        try:
            video_path = video_recorder.stop_recording()
            logger.info(f"Video guardado: {video_path}")
        except Exception as e:
            logger.debug(f"No se pudo detener VideoRecorder: {e}")

    @allure.title("Caso 6.1: Navegación a Ofertas de Vuelos")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_navigate_to_flight_offers(self, setup):
        """Navegar desde el navbar a Ofertas y destinos -> Ofertas de vuelos"""
        browser = setup['browser']
        home_page = setup['home_page']
        video_recorder = setup['video_recorder']
        db = setup['db']
        base_url = setup['base_url']
        url_name = setup['url_name']  # Obtener url_name del setup

        logger.info(f"=== INICIANDO TEST 6.1: Ofertas de Vuelos - {url_name} ===")

        try:
            # Paso 1: Verificar que estamos en español
            with allure.step("Verificar idioma español"):
                current_url = home_page.get_page_url()
                logger.info(f"URL verificada: {current_url}")
                
                # Si no termina en /es/, intentar navegar directamente a la versión española
                if not current_url.endswith('/es/'):
                    spanish_url = f"{base_url}es/"
                    logger.info(f"Navegando directamente a: {spanish_url}")
                    home_page.navigate_to(spanish_url)
                    home_page.wait_for_page_load()
                    current_url = home_page.get_page_url()
                
                assert '/es/' in current_url, f"La URL no contiene '/es/': {current_url}"
                logger.info(f"✅ URL en español confirmada: {current_url}")
                allure.attach(current_url, name="URL en Español", attachment_type=allure.attachment_type.TEXT)

                # Capturar screenshot inicial
                video_recorder.capture_frame(browser)

            # Paso 2: Localizar el menú "Ofertas y destinos" con múltiples selectores
            with allure.step("Localizar menú Ofertas y destinos"):
                logger.info("Buscando menú 'Ofertas y destinos'...")
                
                # Diferentes estrategias para encontrar el menú
                selectors = [
                    "//a[contains(text(), 'Ofertas y destinos')]",
                    "//a[contains(@href, 'ofertas-destinos')]",
                    "//button[contains(text(), 'Ofertas y destinos')]",
                    "//*[contains(@class, 'nav')]//*[contains(text(), 'Ofertas y destinos')]",
                    "//*[contains(@class, 'menu')]//*[contains(text(), 'Ofertas y destinos')]",
                    "//*[contains(@class, 'navbar')]//*[contains(text(), 'Ofertas y destinos')]"
                ]
                
                offers_menu = None
                used_selector = ""
                
                for selector in selectors:
                    try:
                        offers_menu = WebDriverWait(browser, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        used_selector = selector
                        logger.info(f"✅ Menú encontrado con selector: {selector}")
                        break
                    except:
                        continue
                
                if not offers_menu:
                    # Último intento: buscar cualquier elemento que contenga "Ofertas"
                    try:
                        offers_menu = WebDriverWait(browser, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Ofertas')]"))
                        )
                        used_selector = "//*[contains(text(), 'Ofertas')]"
                        logger.info("✅ Menú encontrado con selector genérico 'Ofertas'")
                    except:
                        # Tomar screenshot para diagnóstico
                        home_page.take_screenshot(f"caso6_1_diagnostico_menu_{url_name}.png")
                        raise Exception("No se pudo encontrar el menú 'Ofertas y destinos' con ningún selector")
                
                allure.attach(used_selector, name="Selector usado para menú", attachment_type=allure.attachment_type.TEXT)

            # Paso 3: Interactuar con el menú
            with allure.step("Abrir menú Ofertas y destinos"):
                logger.info("Interactuando con el menú...")
                
                # Capturar antes de la interacción
                video_recorder.capture_frame(browser)
                
                # Intentar diferentes métodos de interacción
                try:
                    # Método 1: Click directo
                    browser.execute_script("arguments[0].click();", offers_menu)
                    logger.info("✅ Click ejecutado con JavaScript")
                except Exception as e:
                    logger.warning(f"Click con JS falló: {e}")
                    try:
                        # Método 2: Actions click
                        actions = ActionChains(browser)
                        actions.move_to_element(offers_menu).click().perform()
                        logger.info("✅ Click ejecutado con ActionChains")
                    except Exception as e2:
                        logger.warning(f"Click con ActionChains falló: {e2}")
                        # Método 3: Click normal
                        offers_menu.click()
                        logger.info("✅ Click ejecutado normalmente")
                
                time.sleep(2)  # Esperar a que se abra el menú
                video_recorder.capture_frame(browser)

            # Paso 4: Localizar "Ofertas de vuelos" en el submenú
            with allure.step("Localizar Ofertas de vuelos"):
                logger.info("Buscando 'Ofertas de vuelos' en el submenú...")
                
                flight_selectors = [
                    "//a[contains(text(), 'Ofertas de vuelos')]",
                    "//a[contains(@href, 'ofertas-de-vuelos')]",
                    "//*[contains(text(), 'Ofertas de vuelos')]",
                    "//a[contains(text(), 'Vuelos')]",
                    "//*[contains(@class, 'submenu')]//*[contains(text(), 'Ofertas de vuelos')]",
                    "//*[contains(@class, 'dropdown')]//*[contains(text(), 'Ofertas de vuelos')]"
                ]
                
                flight_offers_link = None
                used_flight_selector = ""
                
                for selector in flight_selectors:
                    try:
                        flight_offers_link = WebDriverWait(browser, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        used_flight_selector = selector
                        logger.info(f"✅ 'Ofertas de vuelos' encontrado con selector: {selector}")
                        break
                    except:
                        continue
                
                if not flight_offers_link:
                    # Tomar screenshot del menú abierto
                    home_page.take_screenshot(f"caso6_1_menu_abierto_{url_name}.png")
                    raise Exception("No se pudo encontrar 'Ofertas de vuelos' en el submenú")
                
                allure.attach(used_flight_selector, name="Selector usado para Ofertas de vuelos", attachment_type=allure.attachment_type.TEXT)

            # Paso 5: Hacer click en "Ofertas de vuelos"
            with allure.step("Navegar a Ofertas de vuelos"):
                start_time = time.time()
                
                # Capturar antes del click
                video_recorder.capture_frame(browser)
                
                # Hacer click en el enlace
                try:
                    browser.execute_script("arguments[0].click();", flight_offers_link)
                except:
                    flight_offers_link.click()
                
                # Esperar a que la página cargue - con diferentes condiciones
                try:
                    WebDriverWait(browser, 15).until(
                        EC.url_contains("ofertas-de-vuelos")
                    )
                except:
                    # Si no contiene la URL exacta, esperar cualquier cambio
                    WebDriverWait(browser, 15).until(
                        lambda driver: driver.current_url != current_url
                    )
                
                execution_time = time.time() - start_time
                logger.info(f"✅ Navegación completada en {execution_time:.2f}s")

            # Paso 6: Verificaciones finales
            with allure.step("Verificar navegación exitosa"):
                final_url = home_page.get_page_url()
                page_title = browser.title
                
                logger.info(f"URL final: {final_url}")
                logger.info(f"Título de página: {page_title}")
                
                # Verificaciones flexibles
                url_checks = [
                    "ofertas-de-vuelos" in final_url,
                    "ofertas" in final_url and "vuelos" in final_url,
                    "offers" in final_url and "flights" in final_url,
                    any(keyword in final_url.lower() for keyword in ['ofertas', 'offers', 'vuelos', 'flights'])
                ]
                
                assert any(url_checks), f"URL no parece ser de ofertas de vuelos: {final_url}"
                
                # Adjuntar información a Allure
                allure.attach(final_url, name="URL Final", attachment_type=allure.attachment_type.TEXT)
                allure.attach(page_title, name="Título de Página", attachment_type=allure.attachment_type.TEXT)
                allure.attach(f"Tiempo de ejecución: {execution_time:.2f}s", name="Tiempo de Navegación", attachment_type=allure.attachment_type.TEXT)

            # Paso 7: Capturar evidencias
            with allure.step("Capturar evidencias visuales"):
                # Screenshot final
                screenshot_name = f"caso6_1_ofertas_vuelos_{browser.name}_{url_name}.png"
                home_page.take_screenshot(screenshot_name)
                
                allure.attach.file(
                    f"screenshots/{screenshot_name}",
                    name=f"Screenshot Ofertas Vuelos - {browser.name} - {url_name}",
                    attachment_type=allure.attachment_type.PNG
                )
                
                # Capturar frame final
                video_recorder.capture_frame(browser)
                logger.info("✅ Evidencias visuales capturadas")

            # Paso 8: Guardar en base de datos
            with allure.step("Guardar resultados en base de datos"):
                db.save_test_result(
                    test_case_number=6.1,
                    test_case_name=f"Navegación a Ofertas de Vuelos - {url_name}",
                    browser=browser.name,
                    language="español",
                    status="PASS",
                    url=base_url,
                    additional_info=f"URL destino: {final_url}, Tiempo: {execution_time:.2f}s, Título: {page_title}"
                )

                db.save_case6_redirect(
                    test_name=f"Ofertas de Vuelos - {url_name}",
                    browser=browser.name,
                    language="español",
                    from_url=base_url,
                    to_url=final_url,
                    redirect_success=True,
                    page_title=page_title,
                    additional_notes=f"Tiempo: {execution_time:.2f}s"
                )

            logger.info(f"✅ Test 6.1 PASÓ completamente - {url_name} - Tiempo total: {execution_time:.2f}s")

        except Exception as e:
            logger.error(f"❌ Test 6.1 FALLÓ - {url_name}: {e}")
            
            # Capturar screenshot de error
            try:
                error_screenshot = f"caso6_1_error_{browser.name}_{url_name}.png"
                home_page.take_screenshot(error_screenshot)
                allure.attach.file(
                    f"screenshots/{error_screenshot}",
                    name=f"Screenshot Error Test 6.1 - {browser.name} - {url_name}",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as screenshot_error:
                logger.debug(f"No se pudo tomar screenshot de error: {screenshot_error}")

            # Guardar error en base de datos
            try:
                current_url_on_error = home_page.get_page_url()
                db.save_test_result(
                    test_case_number=6.1,
                    test_case_name=f"Navegación a Ofertas de Vuelos - {url_name}",
                    browser=browser.name,
                    language="español",
                    status="FAIL",
                    url=base_url,
                    additional_info=f"Error: {str(e)} - URL en error: {current_url_on_error}"
                )

                db.save_case6_redirect(
                    test_name=f"Ofertas de Vuelos - {url_name}",
                    browser=browser.name,
                    language="español",
                    from_url=base_url,
                    to_url=current_url_on_error,
                    redirect_success=False,
                    additional_notes=f"Error: {str(e)}"
                )
            except Exception as db_error:
                logger.debug(f"Fallo al guardar en DB: {db_error}")

            raise

    @allure.title("Caso 6.2: Navegación a Tu Reserva Check-in y Personaliza tu Viaje")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_navigate_to_checkin_and_customize(self, setup):
        """Navegar desde el navbar a Tu reserva / Check-in -> Personaliza tu viaje"""
        browser = setup['browser']
        home_page = setup['home_page']
        video_recorder = setup['video_recorder']
        db = setup['db']
        base_url = setup['base_url']
        url_name = setup['url_name']  # Obtener url_name del setup

        logger.info(f"=== INICIANDO TEST 6.2: Check-in y Personaliza tu Viaje - {url_name} ===")

        try:
            # Paso 1: Volver a la página principal en español
            with allure.step("Navegar a página principal en español"):
                spanish_url = f"{base_url}es/"
                home_page.navigate_to(spanish_url)
                home_page.wait_for_page_load()
                
                current_url = home_page.get_page_url()
                assert '/es/' in current_url, f"No se pudo navegar a la página principal en español: {current_url}"
                logger.info(f"✅ En página principal española: {current_url}")
                
                video_recorder.capture_frame(browser)
                allure.attach(current_url, name="URL Inicial Test 6.2", attachment_type=allure.attachment_type.TEXT)

            # Paso 2: Localizar el menú "Tu reserva / Check-in" (al lado derecho de Ofertas y destinos)
            with allure.step("Localizar menú Tu reserva / Check-in"):
                logger.info("Buscando menú 'Tu reserva / Check-in'...")
                
                checkin_selectors = [
                    "//a[contains(text(), 'Tu reserva / Check-in')]",
                    "//a[contains(text(), 'Check-in')]",
                    "//a[contains(@href, 'check-in')]",
                    "//a[contains(@href, 'checkin')]",
                    "//button[contains(text(), 'Check-in')]",
                    "//*[contains(@class, 'nav')]//*[contains(text(), 'Check-in')]",
                    "//*[contains(@class, 'nav')]//*[contains(text(), 'Tu reserva')]"
                ]
                
                checkin_menu = None
                used_checkin_selector = ""
                
                for selector in checkin_selectors:
                    try:
                        checkin_menu = WebDriverWait(browser, 10).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        used_checkin_selector = selector
                        logger.info(f"✅ Menú Check-in encontrado con selector: {selector}")
                        break
                    except:
                        continue
                
                if not checkin_menu:
                    raise Exception("No se pudo encontrar el menú 'Tu reserva / Check-in'")
                
                allure.attach(used_checkin_selector, name="Selector usado para Check-in", attachment_type=allure.attachment_type.TEXT)

            # Paso 3: Interactuar con el menú Check-in
            with allure.step("Abrir menú Tu reserva / Check-in"):
                logger.info("Interactuando con el menú Check-in...")
                
                video_recorder.capture_frame(browser)
                
                # Hacer click para abrir el menú
                try:
                    browser.execute_script("arguments[0].click();", checkin_menu)
                    logger.info("✅ Click ejecutado con JavaScript en menú Check-in")
                except Exception as e:
                    logger.warning(f"Click con JS falló: {e}")
                    try:
                        actions = ActionChains(browser)
                        actions.move_to_element(checkin_menu).click().perform()
                        logger.info("✅ Click ejecutado con ActionChains")
                    except Exception as e2:
                        logger.warning(f"Click con ActionChains falló: {e2}")
                        checkin_menu.click()
                        logger.info("✅ Click normal ejecutado")
                
                time.sleep(2)  # Esperar a que se abra el menú
                video_recorder.capture_frame(browser)
                
                # Tomar screenshot después de abrir el menú
                home_page.take_screenshot(f"caso6_2_menu_checkin_abierto_{url_name}.png")

            # Paso 4: Localizar "Personaliza tu viaje" en el submenú (al lado izquierdo)
            with allure.step("Localizar Personaliza tu viaje"):
                logger.info("Buscando 'Personaliza tu viaje' en el submenú...")
                
                customize_selectors = [
                    "//a[contains(text(), 'Personaliza tu viaje')]",
                    "//a[contains(text(), 'Personaliza')]",
                    "//a[contains(@href, 'personaliza-tu-viaje')]",
                    "//a[contains(@href, 'personaliza')]",
                    "//*[contains(text(), 'Personaliza tu viaje')]",
                    "//*[contains(@class, 'submenu')]//*[contains(text(), 'Personaliza tu viaje')]",
                    "//*[contains(@class, 'dropdown')]//*[contains(text(), 'Personaliza tu viaje')]"
                ]
                
                customize_link = None
                used_customize_selector = ""
                
                for selector in customize_selectors:
                    try:
                        customize_link = WebDriverWait(browser, 10).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        used_customize_selector = selector
                        logger.info(f"✅ 'Personaliza tu viaje' encontrado con selector: {selector}")
                        break
                    except:
                        continue
                
                if not customize_link:
                    # Tomar screenshot para diagnóstico
                    home_page.take_screenshot(f"caso6_2_submenu_checkin_{url_name}.png")
                    raise Exception("No se pudo encontrar 'Personaliza tu viaje' en el submenú")
                
                allure.attach(used_customize_selector, name="Selector usado para Personaliza tu viaje", attachment_type=allure.attachment_type.TEXT)

            # Paso 5: Hacer click en "Personaliza tu viaje"
            with allure.step("Navegar a Personaliza tu viaje"):
                start_time = time.time()
                initial_url = browser.current_url
                
                video_recorder.capture_frame(browser)
                
                # Hacer click en el enlace
                try:
                    browser.execute_script("arguments[0].click();", customize_link)
                except:
                    customize_link.click()
                
                # Esperar a que la página cargue - verificar URL específica
                WebDriverWait(browser, 15).until(
                    EC.url_contains("/tu-reserva/personaliza-tu-viaje/")
                )
                
                execution_time = time.time() - start_time
                logger.info(f"✅ Navegación a Personaliza tu viaje completada en {execution_time:.2f}s")

            # Paso 6: Verificaciones finales
            with allure.step("Verificar navegación exitosa"):
                final_url = home_page.get_page_url()
                page_title = browser.title
                
                logger.info(f"URL final: {final_url}")
                logger.info(f"Título de página: {page_title}")
                
                # Verificar URL específica
                expected_url = f"{base_url}es/tu-reserva/personaliza-tu-viaje/"
                assert final_url == expected_url, f"URL no coincide con la esperada. Esperada: {expected_url}, Actual: {final_url}"
                
                # Adjuntar información a Allure
                allure.attach(final_url, name="URL Final Personaliza", attachment_type=allure.attachment_type.TEXT)
                allure.attach(page_title, name="Título de Página Personaliza", attachment_type=allure.attachment_type.TEXT)
                allure.attach(f"Tiempo de ejecución: {execution_time:.2f}s", name="Tiempo de Navegación Personaliza", attachment_type=allure.attachment_type.TEXT)

            # Paso 7: Capturar evidencias finales
            with allure.step("Capturar evidencias visuales"):
                screenshot_name = f"caso6_2_personaliza_viaje_{browser.name}_{url_name}.png"
                home_page.take_screenshot(screenshot_name)
                
                allure.attach.file(
                    f"screenshots/{screenshot_name}",
                    name=f"Screenshot Personaliza Viaje - {browser.name} - {url_name}",
                    attachment_type=allure.attachment_type.PNG
                )
                
                # Capturar frame final
                video_recorder.capture_frame(browser)
                logger.info("✅ Evidencias visuales capturadas para Test 6.2")

            # Paso 8: Guardar en base de datos
            with allure.step("Guardar resultados en base de datos"):
                db.save_test_result(
                    test_case_number=6.2,
                    test_case_name=f"Navegación a Check-in y Personaliza tu Viaje - {url_name}",
                    browser=browser.name,
                    language="español",
                    status="PASS",
                    url=base_url,
                    additional_info=f"URL destino: {final_url}, Tiempo: {execution_time:.2f}s, Título: {page_title}"
                )

                db.save_case6_redirect(
                    test_name=f"Check-in y Personaliza tu Viaje - {url_name}",
                    browser=browser.name,
                    language="español",
                    from_url=base_url,
                    to_url=final_url,
                    redirect_success=True,
                    page_title=page_title,
                    additional_notes=f"Tiempo: {execution_time:.2f}s"
                )

            logger.info(f"✅ Test 6.2 PASÓ completamente - {url_name} - Tiempo total: {execution_time:.2f}s")

        except Exception as e:
            logger.error(f"❌ Test 6.2 FALLÓ - {url_name}: {e}")
            
            # Capturar screenshot de error
            try:
                error_screenshot = f"caso6_2_error_{browser.name}_{url_name}.png"
                home_page.take_screenshot(error_screenshot)
                allure.attach.file(
                    f"screenshots/{error_screenshot}",
                    name=f"Screenshot Error Test 6.2 - {browser.name} - {url_name}",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as screenshot_error:
                logger.debug(f"No se pudo tomar screenshot de error: {screenshot_error}")

            # Guardar error en base de datos
            try:
                current_url_on_error = home_page.get_page_url()
                db.save_test_result(
                    test_case_number=6.2,
                    test_case_name=f"Navegación a Check-in y Personaliza tu Viaje - {url_name}",
                    browser=browser.name,
                    language="español",
                    status="FAIL",
                    url=base_url,
                    additional_info=f"Error: {str(e)} - URL en error: {current_url_on_error}"
                )

                db.save_case6_redirect(
                    test_name=f"Check-in y Personaliza tu Viaje - {url_name}",
                    browser=browser.name,
                    language="español",
                    from_url=base_url,
                    to_url=current_url_on_error,
                    redirect_success=False,
                    additional_notes=f"Error: {str(e)}"
                )
            except Exception as db_error:
                logger.debug(f"Fallo al guardar en DB: {db_error}")

            raise

    @allure.title("Caso 6.3: Navegación a Información y Ayuda - Tipos de Tarifa")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_navigate_to_info_and_help_tariffs(self, setup):
        """Navegar desde el navbar a Información y ayuda -> Tipos de tarifa"""
        browser = setup['browser']
        home_page = setup['home_page']
        video_recorder = setup['video_recorder']
        db = setup['db']
        base_url = setup['base_url']
        url_name = setup['url_name']  # Obtener url_name del setup

        logger.info(f"=== INICIANDO TEST 6.3: Información y Ayuda - Tipos de Tarifa - {url_name} ===")

        try:
            # Paso 1: Volver a la página principal en español
            with allure.step("Navegar a página principal en español"):
                spanish_url = f"{base_url}es/"
                home_page.navigate_to(spanish_url)
                home_page.wait_for_page_load()
                
                current_url = home_page.get_page_url()
                assert '/es/' in current_url, f"No se pudo navegar a la página principal en español: {current_url}"
                logger.info(f"✅ En página principal española: {current_url}")
                
                video_recorder.capture_frame(browser)
                allure.attach(current_url, name="URL Inicial Test 6.3", attachment_type=allure.attachment_type.TEXT)

            # Paso 2: Localizar el menú "Información y ayuda" (al lado derecho de Tu reserva / Check-in)
            with allure.step("Localizar menú Información y ayuda"):
                logger.info("Buscando menú 'Información y ayuda'...")
                
                info_selectors = [
                    "//a[contains(text(), 'Información y ayuda')]",
                    "//a[contains(text(), 'Información')]",
                    "//a[contains(@href, 'informacion-y-ayuda')]",
                    "//a[contains(@href, 'informacion')]",
                    "//button[contains(text(), 'Información')]",
                    "//*[contains(@class, 'nav')]//*[contains(text(), 'Información y ayuda')]",
                    "//*[contains(@class, 'nav')]//*[contains(text(), 'Información')]"
                ]
                
                info_menu = None
                used_info_selector = ""
                
                for selector in info_selectors:
                    try:
                        info_menu = WebDriverWait(browser, 10).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        used_info_selector = selector
                        logger.info(f"✅ Menú Información y ayuda encontrado con selector: {selector}")
                        break
                    except:
                        continue
                
                if not info_menu:
                    raise Exception("No se pudo encontrar el menú 'Información y ayuda'")
                
                allure.attach(used_info_selector, name="Selector usado para Información y ayuda", attachment_type=allure.attachment_type.TEXT)

            # Paso 3: Interactuar con el menú Información y ayuda
            with allure.step("Abrir menú Información y ayuda"):
                logger.info("Interactuando con el menú Información y ayuda...")
                
                video_recorder.capture_frame(browser)
                
                # Hacer click para abrir el menú
                try:
                    browser.execute_script("arguments[0].click();", info_menu)
                    logger.info("✅ Click ejecutado con JavaScript en menú Información y ayuda")
                except Exception as e:
                    logger.warning(f"Click con JS falló: {e}")
                    try:
                        actions = ActionChains(browser)
                        actions.move_to_element(info_menu).click().perform()
                        logger.info("✅ Click ejecutado con ActionChains")
                    except Exception as e2:
                        logger.warning(f"Click con ActionChains falló: {e2}")
                        info_menu.click()
                        logger.info("✅ Click normal ejecutado")
                
                time.sleep(2)  # Esperar a que se abra el menú
                video_recorder.capture_frame(browser)
                
                # Tomar screenshot después de abrir el menú
                home_page.take_screenshot(f"caso6_3_menu_info_abierto_{url_name}.png")

            # Paso 4: Localizar "Tipos de tarifa" en el submenú (al lado izquierdo)
            with allure.step("Localizar Tipos de tarifa"):
                logger.info("Buscando 'Tipos de tarifa' en el submenú...")
                
                tariff_selectors = [
                    "//a[contains(text(), 'Tipos de tarifa')]",
                    "//a[contains(text(), 'Tarifas')]",
                    "//a[contains(@href, 'tarifas-avianca')]",
                    "//a[contains(@href, 'tarifas')]",
                    "//*[contains(text(), 'Tipos de tarifa')]",
                    "//*[contains(@class, 'submenu')]//*[contains(text(), 'Tipos de tarifa')]",
                    "//*[contains(@class, 'dropdown')]//*[contains(text(), 'Tipos de tarifa')]"
                ]
                
                tariff_link = None
                used_tariff_selector = ""
                
                for selector in tariff_selectors:
                    try:
                        tariff_link = WebDriverWait(browser, 10).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        used_tariff_selector = selector
                        logger.info(f"✅ 'Tipos de tarifa' encontrado con selector: {selector}")
                        break
                    except:
                        continue
                
                if not tariff_link:
                    # Tomar screenshot para diagnóstico
                    home_page.take_screenshot(f"caso6_3_submenu_info_{url_name}.png")
                    raise Exception("No se pudo encontrar 'Tipos de tarifa' en el submenú")
                
                allure.attach(used_tariff_selector, name="Selector usado para Tipos de tarifa", attachment_type=allure.attachment_type.TEXT)

            # Paso 5: Hacer click en "Tipos de tarifa"
            with allure.step("Navegar a Tipos de tarifa"):
                start_time = time.time()
                initial_url = browser.current_url
                
                video_recorder.capture_frame(browser)
                
                # Hacer click en el enlace
                try:
                    browser.execute_script("arguments[0].click();", tariff_link)
                except:
                    tariff_link.click()
                
                # Esperar a que la página cargue - verificar URL específica
                WebDriverWait(browser, 15).until(
                    EC.url_contains("/informacion-y-ayuda/tarifas-avianca/")
                )
                
                execution_time = time.time() - start_time
                logger.info(f"✅ Navegación a Tipos de tarifa completada en {execution_time:.2f}s")

            # Paso 6: Verificaciones finales
            with allure.step("Verificar navegación exitosa"):
                final_url = home_page.get_page_url()
                page_title = browser.title
                
                logger.info(f"URL final: {final_url}")
                logger.info(f"Título de página: {page_title}")
                
                # Verificar URL específica
                expected_url = f"{base_url}es/informacion-y-ayuda/tarifas-avianca/"
                assert final_url == expected_url, f"URL no coincide con la esperada. Esperada: {expected_url}, Actual: {final_url}"
                
                # Adjuntar información a Allure
                allure.attach(final_url, name="URL Final Tarifas", attachment_type=allure.attachment_type.TEXT)
                allure.attach(page_title, name="Título de Página Tarifas", attachment_type=allure.attachment_type.TEXT)
                allure.attach(f"Tiempo de ejecución: {execution_time:.2f}s", name="Tiempo de Navegación Tarifas", attachment_type=allure.attachment_type.TEXT)

            # Paso 7: Capturar evidencias finales
            with allure.step("Capturar evidencias visuales"):
                screenshot_name = f"caso6_3_tipos_tarifa_{browser.name}_{url_name}.png"
                home_page.take_screenshot(screenshot_name)
                
                allure.attach.file(
                    f"screenshots/{screenshot_name}",
                    name=f"Screenshot Tipos de Tarifa - {browser.name} - {url_name}",
                    attachment_type=allure.attachment_type.PNG
                )
                
                # Capturar frame final y adjuntar video
                video_recorder.capture_frame(browser)
                
                try:
                    video_file = video_recorder.stop_recording()
                    if video_file and os.path.exists(video_file):
                        allure.attach.file(
                            video_file,
                            name=f"Video Completo - Tests 6.1, 6.2 y 6.3 - {url_name}",
                            attachment_type=allure.attachment_type.MP4
                        )
                        logger.info("✅ Video completo adjuntado a Allure")
                except Exception as e:
                    logger.warning(f"No se pudo adjuntar video: {e}")

                logger.info("✅ Evidencias visuales capturadas para Test 6.3")

            # Paso 8: Guardar en base de datos
            with allure.step("Guardar resultados en base de datos"):
                db.save_test_result(
                    test_case_number=6.3,
                    test_case_name=f"Navegación a Información y Ayuda - Tipos de Tarifa - {url_name}",
                    browser=browser.name,
                    language="español",
                    status="PASS",
                    url=base_url,
                    additional_info=f"URL destino: {final_url}, Tiempo: {execution_time:.2f}s, Título: {page_title}"
                )

                db.save_case6_redirect(
                    test_name=f"Información y Ayuda - Tipos de Tarifa - {url_name}",
                    browser=browser.name,
                    language="español",
                    from_url=base_url,
                    to_url=final_url,
                    redirect_success=True,
                    page_title=page_title,
                    additional_notes=f"Tiempo: {execution_time:.2f}s"
                )

            logger.info(f"✅ Test 6.3 PASÓ completamente - {url_name} - Tiempo total: {execution_time:.2f}s")
            logger.info(f"🎉 TODOS LOS TESTS DEL CASO 6 COMPLETADOS EXITOSAMENTE - {url_name}")

        except Exception as e:
            logger.error(f"❌ Test 6.3 FALLÓ - {url_name}: {e}")
            
            # Capturar screenshot de error
            try:
                error_screenshot = f"caso6_3_error_{browser.name}_{url_name}.png"
                home_page.take_screenshot(error_screenshot)
                allure.attach.file(
                    f"screenshots/{error_screenshot}",
                    name=f"Screenshot Error Test 6.3 - {browser.name} - {url_name}",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as screenshot_error:
                logger.debug(f"No se pudo tomar screenshot de error: {screenshot_error}")

            # Guardar error en base de datos
            try:
                current_url_on_error = home_page.get_page_url()
                db.save_test_result(
                    test_case_number=6.3,
                    test_case_name=f"Navegación a Información y Ayuda - Tipos de Tarifa - {url_name}",
                    browser=browser.name,
                    language="español",
                    status="FAIL",
                    url=base_url,
                    additional_info=f"Error: {str(e)} - URL en error: {current_url_on_error}"
                )

                db.save_case6_redirect(
                    test_name=f"Información y Ayuda - Tipos de Tarifa - {url_name}",
                    browser=browser.name,
                    language="español",
                    from_url=base_url,
                    to_url=current_url_on_error,
                    redirect_success=False,
                    additional_notes=f"Error: {str(e)}"
                )
            except Exception as db_error:
                logger.debug(f"Fallo al guardar en DB: {db_error}")

            # Intentar detener la grabación
            try:
                video_recorder.stop_recording()
            except Exception:
                pass

            raise


def pytest_generate_tests(metafunc):
    """Configurar solo Chrome para las pruebas"""
    if 'browser' in metafunc.fixturenames:
        metafunc.parametrize('browser', ['chrome'], indirect=True)
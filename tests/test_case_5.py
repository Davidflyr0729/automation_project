import pytest
import allure
import logging
from pages.home_page import HomePage
from utils.database import DatabaseManager
from utils.video_recorder import VideoRecorder

logger = logging.getLogger(__name__)

class TestCase5:
    """Caso 5: Verificar cambio de POS (País)"""
    
    @pytest.mark.parametrize("base_url", [
        "https://nuxqa4.avtest.ink/",
        "https://nuxqa5.avtest.ink/"
    ])
    @pytest.mark.parametrize("pos_country", [
        "Otros países",
        "España", 
        "Chile"
    ])
    def test_change_pos(self, browser, base_url, pos_country):
        """
        Caso 5: Verificar cambio de POS (País)
        - Seleccionar 3 POS: Otros países, España, Chile
        - Verificar que cada cambio de POS se haga correctamente
        """
        test_name = f"test_change_pos_{pos_country.replace(' ', '_').lower()}"
        video_recorder = None
        home_page = HomePage(browser)
        
        try:
            # Configurar grabación de video
            video_recorder = VideoRecorder(
                test_name=test_name,
                browser_name=browser.name
            )
            video_recorder.start_recording()

            with allure.step(f"1. Navegar a la página principal: {base_url}"):
                home_page.navigate_to(base_url)
                home_page.wait_for_page_load()
                video_recorder.capture_frame(browser)
                logger.info(f"Navegado a: {base_url}")
                
                # Tomar screenshot inicial
                home_page.take_screenshot(f"initial_{pos_country.replace(' ', '_')}.png")

            with allure.step(f"2. Cambiar POS a: {pos_country}"):
                home_page.select_pos(pos_country)
                video_recorder.capture_frame(browser)
                logger.info(f"POS cambiado a: {pos_country}")
                
                # Tomar screenshot después del cambio
                home_page.take_screenshot(f"after_pos_change_{pos_country.replace(' ', '_')}.png")

            with allure.step(f"3. Verificar que el POS {pos_country} se aplicó correctamente"):
                verification_result = home_page.verify_pos_changed(pos_country)
                assert verification_result, f"Falló la verificación del POS {pos_country}"
                
                current_pos = home_page.get_current_pos()
                logger.info(f"POS actual detectado: {current_pos}")
                
                video_recorder.capture_frame(browser)
                logger.info(f"POS {pos_country} verificado correctamente")

            # Guardar resultado en base de datos - CORREGIDO: agregando parámetro 'language'
            db = DatabaseManager()
            db.save_test_result(
                test_case_number=5,
                test_case_name=f"Change POS to {pos_country}",
                browser=browser.name,
                language="español",  # PARÁMETRO FALTANTE AGREGADO
                status="PASS",
                url=base_url,
                additional_info=f"POS cambiado exitosamente a {pos_country}. Detectado: {current_pos}"
            )
            
            # Adjuntar evidencias a Allure
            allure.attach(
                browser.get_screenshot_as_png(),
                name=f"screenshot_pos_{pos_country.replace(' ', '_')}",
                attachment_type=allure.attachment_type.PNG
            )
            
        except Exception as e:
            # Capturar error y guardar en base de datos - CORREGIDO: agregando parámetro 'language'
            error_msg = f"Error en test_change_pos para {pos_country}: {str(e)}"
            logger.error(error_msg)
            
            if video_recorder:
                video_recorder.capture_frame(browser)
            
            db = DatabaseManager()
            db.save_test_result(
                test_case_number=5,
                test_case_name=f"Change POS to {pos_country}",
                browser=browser.name,
                language="español",  # PARÁMETRO FALTANTE AGREGADO
                status="FAIL",
                url=base_url,
                additional_info=error_msg
            )
            
            # Adjuntar screenshot de error
            allure.attach(
                browser.get_screenshot_as_png(),
                name=f"error_screenshot_pos_{pos_country.replace(' ', '_')}",
                attachment_type=allure.attachment_type.PNG
            )
            
            raise e
        
        finally:
            # Detener grabación de video
            if video_recorder:
                video_path = video_recorder.stop_recording()
                if video_path:
                    allure.attach.file(
                        video_path,
                        name=f"video_pos_{pos_country.replace(' ', '_')}",
                        attachment_type=allure.attachment_type.MP4
                    )
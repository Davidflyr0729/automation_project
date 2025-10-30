import pytest
import allure
from pages.language_page import LanguagePage
from utils.database import DatabaseManager

@allure.feature("Caso 4: Cambio de idioma - Múltiples navegadores")
class TestCase4MultiBrowser:
    """Test Caso 4 en diferentes navegadores"""
    
    def setup_method(self):
        self.db = DatabaseManager()
    
    @pytest.mark.parametrize("browser_name", ["chrome"])  # Podemos agregar "firefox" después
    def test_language_change_chrome(self, browser):
        """Test de cambio de idioma en Chrome"""
        self._run_language_test(browser, "chrome")
    
    def _run_language_test(self, browser, browser_name):
        """Ejecutar test de idiomas para un navegador específico"""
        language_page = LanguagePage(browser)
        
        browser.get("https://nuxqa4.avtest.ink/")
        
        languages = ['english', 'francais', 'portugues', 'español']
        
        for language in languages:
            with allure.step(f"Cambiar a {language} en {browser_name}"):
                try:
                    url_code = language_page.select_language(language)
                    current_language = language_page.get_current_language()
                    
                    assert current_language == language
                    assert f"/{url_code}/" in browser.current_url
                    
                    # Guardar en BD
                    self.db.save_test_result(
                        test_case="Caso_4_MultiBrowser",
                        browser=browser_name,
                        language=language,
                        result="PASS",
                        url=browser.current_url
                    )
                    
                    allure.attach(
                        browser.get_screenshot_as_png(),
                        name=f"{browser_name}_{language}",
                        attachment_type=allure.attachment_type.PNG
                    )
                    
                except Exception as e:
                    self.db.save_test_result(
                        test_case="Caso_4_MultiBrowser",
                        browser=browser_name,
                        language=language,
                        result="FAIL",
                        additional_info=f"Error: {str(e)}"
                    )
                    raise
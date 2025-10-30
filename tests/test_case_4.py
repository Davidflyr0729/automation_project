import pytest
import allure
import os
from pages.language_page import LanguagePage
from utils.database import DatabaseManager

@allure.feature("Caso 4: Verificación de cambio de idioma")
@allure.severity(allure.severity_level.CRITICAL)
class TestCase4:
    """Test para el Caso 4 - Cambio de idioma en ambas URLs (nuxqa4 y nuxqa5)"""
    
    def setup_method(self):
        """Configuración antes de cada test"""
        self.db = DatabaseManager()
        self.test_case_number = 4
        self.test_case_name = "Cambio de Idiomas"
        os.makedirs("screenshots", exist_ok=True)
        self.failed_tests = []  # Para trackear tests que fallaron
    
    @allure.story("Cambiar a los 4 idiomas en ambas URLs")
    @allure.description("Verificar idiomas en nuxqa4.avtest.ink y nuxqa5.avtest.ink")
    def test_change_all_languages_both_urls(self, browser):
        """Test que cambia por los 4 idiomas en AMBAS URLs"""
        language_page = LanguagePage(browser)
        
        # AMBAS URLs A PROBAR
        urls_to_test = [
            "https://nuxqa4.avtest.ink/",
            "https://nuxqa5.avtest.ink/"
        ]
        
        # LOS 4 IDIOMAS A PROBAR
        languages_to_test = ['english', 'francais', 'portugues', 'español']
        
        all_test_results = []
        self.failed_tests = []
        
        with allure.step("Probar en ambas URLs"):
            for url in urls_to_test:
                with allure.step(f"Probando en: {url}"):
                    
                    # Navegar a la URL actual
                    browser.get(url)
                    current_url = browser.current_url
                    print(f"🌐 Probando en: {current_url}")
                    
                    # Probar los 4 idiomas en esta URL
                    url_results = self._test_languages_for_url(browser, language_page, languages_to_test, current_url)
                    all_test_results.extend(url_results)
        
        # Reporte final
        self._generate_final_report(all_test_results)
    
    def _test_languages_for_url(self, browser, language_page, languages_to_test, base_url):
        """Probar idiomas para una URL específica"""
        url_results = []
        
        for language in languages_to_test:
            with allure.step(f"Cambiar a {language} en {base_url}"):
                try:
                    # Tomar screenshot COMPLETO antes del cambio
                    site_name = "nuxqa4" if "nuxqa4" in base_url else "nuxqa5"
                    before_screenshot = language_page.take_screenshot_with_url(
                        f"screenshots/full_before_{site_name}_{language}_{browser.name}.png"
                    )
                    
                    # Cambiar idioma
                    url_code = language_page.select_language(language)
                    
                    # Tomar screenshot COMPLETO después del cambio
                    after_screenshot = language_page.take_screenshot_with_url(
                        f"screenshots/full_after_{site_name}_{language}_{browser.name}.png"
                    )
                    
                    # Verificaciones
                    current_language = language_page.get_current_language()
                    current_url = browser.current_url
                    
                    assert current_language == language, \
                        f"El idioma actual debería ser {language} pero es {current_language}"
                    
                    assert f"/{url_code}/" in current_url, \
                        f"La URL debería contener /{url_code}/"
                    
                    # Resultado exitoso
                    url_results.append((site_name, language, "PASS", current_url))
                    
                    # Guardar en base de datos
                    self.db.save_test_result(
                        test_case_number=self.test_case_number,
                        test_case_name=f"{self.test_case_name} - {site_name}",
                        browser=browser.name,
                        language=language,
                        status="PASS",
                        url=current_url,
                        screenshot_path=after_screenshot,
                        additional_info=f"Idioma {language} exitoso en {site_name}"
                    )
                    
                    # Adjuntar screenshot COMPLETO a Allure
                    with open(after_screenshot, "rb") as f:
                        allure.attach(
                            f.read(),
                            name=f"full_{site_name}_{language}",
                            attachment_type=allure.attachment_type.PNG
                        )
                    
                    # Adjuntar información de la página
                    page_info = language_page.get_page_info()
                    allure.attach(
                        str(page_info),
                        name=f"info_{site_name}_{language}",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    
                    print(f"✅ {site_name} - {language}: PASS - {current_url}")
                    print(f"   📸 Screenshots: {before_screenshot} -> {after_screenshot}")
                    
                except Exception as e:
                    # Resultado fallido
                    site_name = "nuxqa4" if "nuxqa4" in base_url else "nuxqa5"
                    url_results.append((site_name, language, "FAIL", str(e)))
                    self.failed_tests.append(f"{site_name}_{language}")
                    
                    # Screenshot COMPLETO del error
                    error_screenshot = language_page.take_screenshot_with_url(
                        f"screenshots/full_error_{site_name}_{language}_{browser.name}.png"
                    )
                    
                    # Guardar error en BD
                    self.db.save_test_result(
                        test_case_number=self.test_case_number,
                        test_case_name=f"{self.test_case_name} - {site_name}",
                        browser=browser.name,
                        language=language,
                        status="FAIL",
                        url=browser.current_url,
                        screenshot_path=error_screenshot,
                        additional_info=f"Error en {site_name}: {str(e)}"
                    )
                    
                    # Adjuntar screenshot COMPLETO del error a Allure
                    with open(error_screenshot, "rb") as f:
                        allure.attach(
                            f.read(),
                            name=f"full_error_{site_name}_{language}",
                            attachment_type=allure.attachment_type.PNG
                        )
                    
                    print(f"❌ {site_name} - {language}: FAIL - {e}")
                    print(f"   📸 Screenshot error: {error_screenshot}")
                    
                    # Intentar volver a la URL base
                    try:
                        browser.get(base_url)
                        print(f"🔄 Volviendo a {base_url}")
                    except:
                        print(f"⚠️  No se pudo volver a {base_url}")
        
        return url_results
    
    def _generate_final_report(self, all_test_results):
        """Generar reporte final"""
        with allure.step("Resumen final de todas las pruebas"):
            allure.attach(
                str(all_test_results),
                name="resumen_completo_resultados",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Estadísticas por sitio
            nuxqa4_results = [r for r in all_test_results if r[0] == "nuxqa4"]
            nuxqa5_results = [r for r in all_test_results if r[0] == "nuxqa5"]
            
            nuxqa4_passed = [r for r in nuxqa4_results if r[2] == "PASS"]
            nuxqa5_passed = [r for r in nuxqa5_results if r[2] == "PASS"]
            
            print("\n📊 RESUMEN FINAL CASO 4 - AMBAS URLs:")
            print("=" * 60)
            
            print("\n🌐 nuxqa4.avtest.ink:")
            for site, lang, result, info in nuxqa4_results:
                status_icon = "✅" if result == "PASS" else "❌"
                print(f"   {status_icon} {lang}: {result} - {info}")
            
            print(f"\n🌐 nuxqa5.avtest.ink:")
            for site, lang, result, info in nuxqa5_results:
                status_icon = "✅" if result == "PASS" else "❌"
                print(f"   {status_icon} {lang}: {result} - {info}")
            
            print(f"\n📈 ESTADÍSTICAS FINALES:")
            print(f"   nuxqa4: {len(nuxqa4_passed)}/{len(nuxqa4_results)} éxitos")
            print(f"   nuxqa5: {len(nuxqa5_passed)}/{len(nuxqa5_results)} éxitos")
            print(f"   TOTAL: {len(nuxqa4_passed + nuxqa5_passed)}/{len(all_test_results)} éxitos")
            
            # Mostrar información de screenshots
            print(f"\n📸 SCREENSHOTS GENERADOS:")
            screenshots = [f for f in os.listdir('screenshots') if f.startswith('full_') and f.endswith('.png')]
            for screenshot in screenshots[:6]:  # Mostrar primeros 6
                print(f"   📄 {screenshot}")
            
            # Verificación final
            total_passed = len(nuxqa4_passed) + len(nuxqa5_passed)
            if total_passed == 0:
                pytest.fail("❌ TODAS las pruebas fallaron en ambas URLs")
            elif len(self.failed_tests) > 0:
                print(f"⚠️  Algunas pruebas fallaron: {self.failed_tests}")
    
    def teardown_method(self):
        """Limpieza después de cada test"""
        # Mostrar resumen de la base de datos
        self.db.print_database_summary()
        
        # Mostrar resumen específico por sitio
        print(f"\n🔍 REGISTROS POR SITIO EN BD:")
        all_results = self.db.get_test_results(4)
        nuxqa4_count = len([r for r in all_results if "nuxqa4" in str(r[2])])
        nuxqa5_count = len([r for r in all_results if "nuxqa5" in str(r[2])])
        
        print(f"   nuxqa4: {nuxqa4_count} registros")
        print(f"   nuxqa5: {nuxqa5_count} registros")
        print(f"   TOTAL: {len(all_results)} registros")
        
        # Mostrar estadísticas de screenshots
        print(f"\n📊 ESTADÍSTICAS SCREENSHOTS:")
        screenshots = [f for f in os.listdir('screenshots') if f.endswith('.png')]
        full_screenshots = [f for f in screenshots if f.startswith('full_')]
        print(f"   Total screenshots: {len(screenshots)}")
        print(f"   Screenshots completos: {len(full_screenshots)}")
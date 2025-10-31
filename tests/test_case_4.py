import pytest
import allure
import os
from pages.language_page import LanguagePage
from utils.database import DatabaseManager
from utils.video_recorder import VideoRecorder

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
        os.makedirs("videos", exist_ok=True)
        self.failed_tests = []
    
    @allure.story("Cambiar a los 4 idiomas en ambas URLs")
    @allure.description("Verificar idiomas en nuxqa4.avtest.ink y nuxqa5.avtest.ink")
    def test_change_all_languages_both_urls(self, browser):
        """Test que cambia por los 4 idiomas en AMBAS URLs - CON 8 VIDEOS INDIVIDUALES"""
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
        all_video_paths = []  # ✅ NUEVO: Para trackear todos los videos generados
        
        with allure.step("Probar en ambas URLs"):
            for url in urls_to_test:
                with allure.step(f"Probando en: {url}"):
                    
                    # Navegar a la URL actual
                    browser.get(url)
                    current_url = browser.current_url
                    print(f"🌐 Probando en: {current_url}")
                    
                    # Probar los 4 idiomas en esta URL
                    url_results, url_video_paths = self._test_languages_for_url(
                        browser, language_page, languages_to_test, current_url
                    )
                    all_test_results.extend(url_results)
                    all_video_paths.extend(url_video_paths)  # ✅ NUEVO: Acumular videos
        
        # ✅ NUEVO: Generar reporte de videos
        self._generate_video_report(all_video_paths)
        
        # Reporte final
        self._generate_final_report(all_test_results, all_video_paths)
    
    def _test_languages_for_url(self, browser, language_page, languages_to_test, base_url):
        """Probar idiomas para una URL específica - CON VIDEO INDIVIDUAL POR IDIOMA"""
        url_results = []
        url_video_paths = []  # ✅ NUEVO: Videos generados en esta URL
        
        for language in languages_to_test:
            with allure.step(f"Cambiar a {language} en {base_url}"):
                # ✅ NUEVO: Crear video recorder INDIVIDUAL para este idioma
                site_name = "nuxqa4" if "nuxqa4" in base_url else "nuxqa5"
                video_recorder = VideoRecorder(
                    test_name=f"{site_name}_{language}",
                    browser_name=browser.name,
                    output_dir="videos"
                )
                
                video_path = None
                
                try:
                    # ✅ NUEVO: Iniciar grabación INDIVIDUAL
                    video_recorder.start_recording()
                    
                    # Capturar frame inicial (página actual)
                    video_recorder.capture_frame(browser)
                    
                    # Tomar screenshot COMPLETO antes del cambio
                    before_screenshot = language_page.take_screenshot_with_url(
                        f"screenshots/full_before_{site_name}_{language}_{browser.name}.png"
                    )
                    
                    # Cambiar idioma
                    url_code = language_page.select_language(language)
                    
                    # Capturar frame después del cambio
                    video_recorder.capture_frame(browser)
                    
                    # Validación de contenido
                    content_valid = language_page.validate_language_content(language)
                    assert content_valid, f"El contenido no coincide con el idioma {language}"
                    
                    # Capturar frame final (validación exitosa)
                    video_recorder.capture_frame(browser)
                    
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
                    
                    # ✅ NUEVO: Detener grabación INDIVIDUAL y obtener video
                    video_path = video_recorder.stop_recording()
                    if video_path:
                        url_video_paths.append(video_path)
                    
                    # Resultado exitoso
                    url_results.append((site_name, language, "PASS", current_url, video_path))
                    
                    # Guardar en base de datos
                    self.db.save_test_result(
                        test_case_number=self.test_case_number,
                        test_case_name=f"{self.test_case_name} - {site_name}",
                        browser=browser.name,
                        language=language,
                        status="PASS",
                        url=current_url,
                        screenshot_path=after_screenshot,
                        additional_info=f"Idioma {language} exitoso en {site_name}" + 
                                       (f" - Video: {os.path.basename(video_path)}" if video_path else "")
                    )
                    
                    # Adjuntar screenshot COMPLETO a Allure
                    with open(after_screenshot, "rb") as f:
                        allure.attach(
                            f.read(),
                            name=f"full_{site_name}_{language}",
                            attachment_type=allure.attachment_type.PNG
                        )
                    
                    # ✅ NUEVO: Adjuntar video INDIVIDUAL a Allure
                    if video_path and os.path.exists(video_path):
                        try:
                            with open(video_path, "rb") as video_file:
                                allure.attach(
                                    video_file.read(),
                                    name=f"video_{site_name}_{language}",
                                    attachment_type=allure.attachment_type.MP4
                                )
                            print(f"🎥 Video individual adjuntado: {site_name} - {language}")
                        except Exception as e:
                            print(f"❌ Error adjuntando video individual: {e}")
                    
                    # Adjuntar información de la página
                    page_info = language_page.get_page_info()
                    allure.attach(
                        str(page_info),
                        name=f"info_{site_name}_{language}",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    
                    print(f"✅ {site_name} - {language}: PASS - {current_url}")
                    if video_path:
                        print(f"   🎥 Video generado: {os.path.basename(video_path)}")
                    
                except Exception as e:
                    # ✅ NUEVO: En caso de error, también capturar video
                    try:
                        # Capturar frame del error
                        video_recorder.capture_frame(browser)
                        error_video_path = video_recorder.stop_recording()
                        if error_video_path:
                            url_video_paths.append(error_video_path)
                    except:
                        error_video_path = None
                    
                    url_results.append((site_name, language, "FAIL", str(e), error_video_path))
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
                        additional_info=f"Error en {site_name}: {str(e)}" + 
                                       (f" - Video error: {os.path.basename(error_video_path)}" if error_video_path else "")
                    )
                    
                    # Adjuntar screenshot COMPLETO del error a Allure
                    with open(error_screenshot, "rb") as f:
                        allure.attach(
                            f.read(),
                            name=f"full_error_{site_name}_{language}",
                            attachment_type=allure.attachment_type.PNG
                        )
                    
                    # ✅ NUEVO: Adjuntar video del error si existe
                    if error_video_path and os.path.exists(error_video_path):
                        try:
                            with open(error_video_path, "rb") as video_file:
                                allure.attach(
                                    video_file.read(),
                                    name=f"video_error_{site_name}_{language}",
                                    attachment_type=allure.attachment_type.MP4
                                )
                            print(f"🎥 Video de error adjuntado: {site_name} - {language}")
                        except Exception as video_error:
                            print(f"❌ Error adjuntando video de error: {video_error}")
                    
                    print(f"❌ {site_name} - {language}: FAIL - {e}")
                    print(f"   📸 Screenshot error: {error_screenshot}")
                    if error_video_path:
                        print(f"   🎥 Video error: {os.path.basename(error_video_path)}")
                    
                    # Intentar volver a la URL base
                    try:
                        browser.get(base_url)
                        print(f"🔄 Volviendo a {base_url}")
                    except:
                        print(f"⚠️  No se pudo volver a {base_url}")
        
        return url_results, url_video_paths
    
    def _generate_video_report(self, all_video_paths):
        """Generar reporte de videos generados"""
        with allure.step("Resumen de videos generados"):
            if all_video_paths:
                video_info = "🎥 VIDEOS GENERADOS:\n" + "="*50 + "\n"
                for i, video_path in enumerate(all_video_paths, 1):
                    video_info += f"{i}. {os.path.basename(video_path)}\n"
                    if os.path.exists(video_path):
                        file_size = os.path.getsize(video_path) / 1024  # KB
                        video_info += f"   Tamaño: {file_size:.1f} KB\n"
                
                allure.attach(
                    video_info,
                    name="resumen_videos_generados",
                    attachment_type=allure.attachment_type.TEXT
                )
                
                print(f"\n🎥 RESUMEN VIDEOS GENERADOS:")
                print("=" * 50)
                for video_path in all_video_paths:
                    if os.path.exists(video_path):
                        file_size = os.path.getsize(video_path) / 1024
                        print(f"   📹 {os.path.basename(video_path)} ({file_size:.1f} KB)")
    
    def _generate_final_report(self, all_test_results, all_video_paths):
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
            for site, lang, result, info, video_path in nuxqa4_results:
                status_icon = "✅" if result == "PASS" else "❌"
                video_info = " 🎥" if video_path else ""
                print(f"   {status_icon} {lang}: {result} - {info}{video_info}")
            
            print(f"\n🌐 nuxqa5.avtest.ink:")
            for site, lang, result, info, video_path in nuxqa5_results:
                status_icon = "✅" if result == "PASS" else "❌"
                video_info = " 🎥" if video_path else ""
                print(f"   {status_icon} {lang}: {result} - {info}{video_info}")
            
            print(f"\n📈 ESTADÍSTICAS FINALES:")
            print(f"   nuxqa4: {len(nuxqa4_passed)}/{len(nuxqa4_results)} éxitos")
            print(f"   nuxqa5: {len(nuxqa5_passed)}/{len(nuxqa5_results)} éxitos")
            print(f"   TOTAL: {len(nuxqa4_passed + nuxqa5_passed)}/{len(all_test_results)} éxitos")
            
            # ✅ NUEVO: Mostrar información de videos
            if all_video_paths:
                print(f"\n🎥 VIDEOS GENERADOS: {len(all_video_paths)} videos")
                successful_videos = [vp for vp in all_video_paths if os.path.exists(vp)]
                print(f"   ✅ Videos exitosos: {len(successful_videos)}/{len(all_video_paths)}")
            
            # Mostrar información de screenshots
            print(f"\n📸 SCREENSHOTS GENERADOS:")
            screenshots = [f for f in os.listdir('screenshots') if f.startswith('full_') and f.endswith('.png')]
            for screenshot in screenshots[:6]:
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
        
        # Mostrar estadísticas de screenshots y videos
        print(f"\n📊 ESTADÍSTICAS MULTIMEDIA:")
        screenshots = [f for f in os.listdir('screenshots') if f.endswith('.png')]
        full_screenshots = [f for f in screenshots if f.startswith('full_')]
        videos = [f for f in os.listdir('videos') if f.endswith('.mp4')]
        
        print(f"   Total screenshots: {len(screenshots)}")
        print(f"   Screenshots completos: {len(full_screenshots)}")
        print(f"   Videos generados: {len(videos)}")
        
        # ✅ NUEVO: Mostrar lista de videos generados
        if videos:
            print(f"\n🎥 LISTA DE VIDEOS GENERADOS:")
            for video in videos:
                video_path = os.path.join('videos', video)
                if os.path.exists(video_path):
                    file_size = os.path.getsize(video_path) / 1024
                    print(f"   📹 {video} ({file_size:.1f} KB)")
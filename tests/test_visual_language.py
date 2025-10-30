import pytest
import time
from pages.language_page import LanguagePage

def test_visual_language_change(browser):
    """Test VISUAL para ver el cambio de idioma en acción - LOS 4 IDIOMAS"""
    
    language_page = LanguagePage(browser)
    
    print("👀 INICIANDO TEST VISUAL - Puedes ver el navegador")
    print("🎯 Probando los 4 idiomas: Español, English, Français, Português")
    
    # 1. Navegar a la página
    browser.get("https://nuxqa4.avtest.ink/")
    print("📍 Página cargada - Idioma inicial: Español")
    time.sleep(3)  # Pausa para ver
    
    # 2. Probar cambiar a English
    print("🔄 1/4 Cambiando a ENGLISH...")
    language_page.select_language('english')
    time.sleep(3)
    print(f"✅ Cambiado a English - URL: {browser.current_url}")
    
    # 3. Probar cambiar a Français
    print("🔄 2/4 Cambiando a FRANÇAIS...")
    language_page.select_language('francais')
    time.sleep(3)
    print(f"✅ Cambiado a Français - URL: {browser.current_url}")
    
    # 4. Probar cambiar a Português
    print("🔄 3/4 Cambiando a PORTUGUÊS...")
    language_page.select_language('portugues')
    time.sleep(3)
    print(f"✅ Cambiado a Português - URL: {browser.current_url}")
    
    # 5. Volver a Español
    print("🔄 4/4 Volviendo a ESPAÑOL...")
    language_page.select_language('español')
    time.sleep(3)
    print(f"✅ Vuelto a Español - URL: {browser.current_url}")
    
    print("🎉 TEST VISUAL COMPLETADO - LOS 4 IDIOMAS PROBADOS")
    print("📊 Resumen:")
    print("   ✅ Español")
    print("   ✅ English") 
    print("   ✅ Français")
    print("   ✅ Português")
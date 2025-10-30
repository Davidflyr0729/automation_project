def test_selenium_browser(browser):
    """Test básico para verificar que Selenium funciona"""
    # Navegar a Google
    browser.get("https://www.google.com")
    
    # Verificar que cargó correctamente
    title = browser.title
    current_url = browser.current_url
    
    print(f"📄 Título de la página: {title}")
    print(f"🌐 URL actual: {current_url}")
    
    assert "Google" in title
    assert current_url.startswith("https://www.google.com")
    print("✅ Navegación a Google exitosa")

def test_navigation_to_test_site(browser):
    """Test de navegación a la página de la prueba técnica"""
    browser.get("https://nuxqa4.avtest.ink/")
    
    title = browser.title
    current_url = browser.current_url
    
    print(f"🌐 Página de prueba - Título: {title}")
    print(f"🔗 Página de prueba - URL: {current_url}")
    
    # Verificar que cargó la página de la prueba técnica
    assert current_url.startswith("https://nuxqa4.avtest.ink/")
    print("✅ Navegación a la página de prueba técnica exitosa")

def test_page_loaded_correctly(browser):
    """Test para verificar que la página cargó los elementos básicos"""
    browser.get("https://nuxqa4.avtest.ink/")

    # Verificar que la pagina contenga un titulo
    title = browser.title
    print(f"📄 Título de la página de prueba: {title}")
    assert title != "", "La página debe tener un título"

    # Verificar que la página se cargó correctamente
    page_source = browser.page_source
    assert len(page_source) > 0, "El código fuente de la página no debe estar vacío"
    print("✅ La página de prueba técnica cargó correctamente")
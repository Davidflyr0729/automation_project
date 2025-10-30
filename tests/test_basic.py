def test_browser_option(browser):
    """Test básico para validar que el fixture funcione"""
    # browser es un objeto WebDriver de Chrome
    print(f"🔧 Navegador en uso: {browser.name}")
    print(f"📄 URL actual: {browser.current_url}")
    
    # Verificar que tenemos un objeto WebDriver válido
    assert hasattr(browser, 'get'), "El objeto browser debe tener método get"
    assert hasattr(browser, 'title'), "El objeto browser debe tener atributo title"
    assert hasattr(browser, 'current_url'), "El objeto browser debe tener atributo current_url"
    
    # Verificar que es Chrome
    browser_name = browser.name.lower()
    assert "chrome" in browser_name, f"Navegador {browser_name} no es Chrome"
    
    print("✅ WebDriver está correctamente inicializado")

def test_simple_assertion():
    """Test básico para validar que pytest funcione"""
    assert 1 + 1 == 2
    print("✅ Test básico de assertions funciona")

def test_browser_navigation(browser):
    """Test de navegación básica"""
    # Navegar a una página simple
    browser.get("about:blank")
    
    # Verificar que navegó correctamente
    assert browser.current_url == "about:blank"
    assert browser.title == ""
    
    print("✅ Navegación básica funciona correctamente")
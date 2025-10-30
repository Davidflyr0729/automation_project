import pytest
from selenium.webdriver.common.by import By
import time

def test_investigate_language_elements(browser):
    """Test para investigar qué elementos existen realmente"""
    
    print("🔍 INVESTIGANDO ELEMENTOS DE LA PÁGINA...")
    
    # 1. Navegar a la página
    browser.get("https://nuxqa4.avtest.ink/")
    print(f"📍 URL: {browser.current_url}")
    
    # 2. Tomar screenshot para ver qué hay
    browser.save_screenshot("investigation.png")
    print("📸 Screenshot guardado: investigation.png")
    
    # 3. Buscar elementos relacionados con idioma
    possible_selectors = [
        (By.CLASS_NAME, "dropdown_trigger"),
        (By.CLASS_NAME, "dropdown-trigger"),
        (By.CLASS_NAME, "language"),
        (By.CLASS_NAME, "lang"),
        (By.XPATH, "//*[contains(text(), 'ES')]"),
        (By.XPATH, "//*[contains(text(), 'EN')]"),
        (By.XPATH, "//*[contains(text(), 'FR')]"),
        (By.XPATH, "//*[contains(text(), 'PT')]"),
        (By.XPATH, "//select"),  # Cualquier dropdown
        (By.XPATH, "//button"),  # Cualquier botón
    ]
    
    print("🔎 Buscando elementos...")
    found_elements = []
    
    for by, selector in possible_selectors:
        try:
            elements = browser.find_elements(by, selector)
            if elements:
                for i, element in enumerate(elements):
                    tag = element.tag_name
                    text = element.text[:50] if element.text else "Sin texto"
                    found_elements.append((by, selector, tag, text))
                    print(f"✅ ENCONTRADO: {by}='{selector}' -> <{tag}> '{text}'")
        except Exception as e:
            print(f"❌ Error con {by}='{selector}': {e}")
    
    # 4. Mostrar todos los elementos encontrados
    print("\n📋 RESUMEN DE ELEMENTOS ENCONTRADOS:")
    for by, selector, tag, text in found_elements:
        print(f"   - {by}='{selector}' -> <{tag}> '{text}'")
    
    # 5. Mostrar todo el HTML de la página para debug
    print(f"\n📄 Longitud del HTML: {len(browser.page_source)} caracteres")
    
    # Buscar cualquier menú desplegable
    dropdown_keywords = ["dropdown", "select", "menu", "language", "lang", "idioma"]
    for keyword in dropdown_keywords:
        if keyword in browser.page_source.lower():
            print(f"🔍 Keyword '{keyword}' encontrada en el HTML")
    
    assert True  # No fallar el test
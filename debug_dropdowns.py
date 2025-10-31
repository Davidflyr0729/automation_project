#!/usr/bin/env python3
"""
DEBUG DROPDOWNS NAVBAR
Debug específico para los botones dropdown del navbar
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

def setup_driver():
    """Configurar el driver del navegador"""
    options = Options()
    options.add_argument('--headless')  # Quitar para ver la interfaz
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver

def debug_dropdowns(url="https://nuxqa4.avtest.ink/"):
    """Debug específico para dropdowns del navbar"""
    logger.info("🚀 INICIANDO DEBUG DROPDOWNS")
    logger.info(f"🌐 URL: {url}")
    
    driver = setup_driver()
    
    try:
        # Navegar a la página
        logger.info("📄 Navegando a la página...")
        driver.get(url)
        time.sleep(3)
        
        logger.info("=" * 80)
        logger.info("🔍 DEBUG ESPECÍFICO: BOTONES DROPDOWN DEL NAVBAR")
        logger.info("=" * 80)
        
        # 1. BUSCAR TODOS LOS BOTONES EN EL HEADER
        logger.info("\n📋 1. BUSCANDO TODOS LOS BOTONES EN EL HEADER:")
        all_buttons = driver.find_elements(By.TAG_NAME, "button")
        header_buttons = []
        
        for button in all_buttons:
            try:
                if button.is_displayed():
                    classes = button.get_attribute('class')
                    text = button.text.strip()
                    if "nav" in classes.lower() or "header" in classes.lower():
                        header_buttons.append(button)
                        logger.info(f"  🔘 Botón: '{text}'")
                        logger.info(f"     Clases: {classes}")
                        logger.info(f"     ID: {button.get_attribute('id')}")
            except:
                continue
        
        logger.info(f"🔍 Botones en header: {len(header_buttons)}")
        
        # 2. BUSCAR BOTONES ESPECÍFICOS POR CLASE
        logger.info("\n📋 2. BUSCANDO BOTONES POR CLASES ESPECÍFICAS:")
        
        button_selectors = [
            "button.main-header_nav-primary_item_link",
            "button[class*='main-header_nav-primary_item_link']",
            "button[class*='nav-primary_item']",
            "button[class*='section-offer']",
            "button[class*='section-booking']", 
            "button[class*='section-info']"
        ]
        
        for selector in button_selectors:
            try:
                buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                if buttons:
                    logger.info(f"✅ Selector '{selector}': {len(buttons)} botones")
                    for i, btn in enumerate(buttons):
                        logger.info(f"   {i+1}. Texto: '{btn.text.strip()}'")
                        logger.info(f"      Clases: '{btn.get_attribute('class')}'")
                        logger.info(f"      Visible: {btn.is_displayed()}")
                        logger.info(f"      Habilitado: {btn.is_enabled()}")
            except Exception as e:
                logger.error(f"❌ Error con selector '{selector}': {e}")
        
        # 3. BUSCAR ELEMENTOS CLICKEABLES EN EL NAVBAR
        logger.info("\n📋 3. ELEMENTOS CLICKEABLES EN EL ÁREA DEL NAVBAR:")
        
        # Buscar en el área del header
        header = driver.find_element(By.TAG_NAME, "header")
        clickable_elements = header.find_elements(By.XPATH, ".//*[self::a or self::button or self::div[@role='button']]")
        
        visible_clickable = [elem for elem in clickable_elements if elem.is_displayed()]
        logger.info(f"🔍 Elementos clickeables visibles en header: {len(visible_clickable)}")
        
        for i, elem in enumerate(visible_clickable[:10]):  # Mostrar primeros 10
            tag = elem.tag_name
            text = elem.text.strip() if elem.text.strip() else "(sin texto)"
            classes = elem.get_attribute('class')
            logger.info(f"  {i+1}. <{tag}>: '{text}'")
            logger.info(f"     Clases: '{classes}'")
        
        # 4. PROBAR CLICK EN POSIBLES BOTONES
        logger.info("\n📋 4. PROBANDO CLICK EN BOTONES:")
        
        # Buscar botones con texto específico
        possible_button_texts = ["Ofertas", "Reserva", "Información", "Vuelos", "Check-in", "Tarifas"]
        
        for text in possible_button_texts:
            try:
                elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{text}')]")
                clickable_elements = [elem for elem in elements if elem.is_displayed() and elem.is_enabled()]
                
                if clickable_elements:
                    logger.info(f"✅ Texto '{text}': {len(clickable_elements)} elementos clickeables")
                    for elem in clickable_elements[:2]:  # Mostrar primeros 2
                        logger.info(f"   - <{elem.tag_name}>: '{elem.text.strip()}'")
                        logger.info(f"     Clases: '{elem.get_attribute('class')}'")
            except Exception as e:
                logger.error(f"❌ Error buscando texto '{text}': {e}")
        
        # 5. TOMAR SCREENSHOT DEL HEADER
        logger.info("\n📸 5. TOMANDO SCREENSHOT DEL HEADER...")
        header.screenshot("debug_header_screenshot.png")
        logger.info("✅ Screenshot del header guardado como: debug_header_screenshot.png")
        
        logger.info("\n" + "=" * 80)
        logger.info("✅ DEBUG DROPDOWNS COMPLETADO")
        logger.info("📝 Revisa los logs para ver la estructura real de los botones")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"❌ ERROR CRÍTICO: {e}")
        import traceback
        logger.error(traceback.format_exc())
        
    finally:
        driver.quit()
        logger.info("🔚 Navegador cerrado")

if __name__ == "__main__":
    print("🚀 EJECUTANDO DEBUG DROPDOWNS")
    print("=" * 50)
    
    urls_to_test = [
        "https://nuxqa4.avtest.ink/",
        "https://nuxqa5.avtest.ink/"
    ]
    
    for url in urls_to_test:
        print(f"\n🌐 PROBANDO URL: {url}")
        print("-" * 50)
        debug_dropdowns(url)
        time.sleep(2)
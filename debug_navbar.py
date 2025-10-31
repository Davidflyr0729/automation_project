#!/usr/bin/env python3
"""
DEBUG NAVBAR ELEMENTS
Archivo específico para debugging de elementos del navbar
Ejecutar con: python debug_navbar.py
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

def setup_driver(browser_name='chrome'):
    """Configurar el driver del navegador"""
    if browser_name.lower() == 'chrome':
        options = Options()
        options.add_argument('--headless')  # Ejecutar en modo sin cabeza
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
    elif browser_name.lower() == 'firefox':
        options = FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError("Navegador no soportado. Usar 'chrome' o 'firefox'")
    
    driver.implicitly_wait(10)
    return driver

def debug_navbar_elements(url="https://nuxqa4.avtest.ink/"):
    """Función principal de debug para analizar elementos del navbar"""
    logger.info("🚀 INICIANDO DEBUG NAVBAR")
    logger.info(f"🌐 URL: {url}")
    
    driver = setup_driver('chrome')
    
    try:
        # Navegar a la página
        logger.info("📄 Navegando a la página...")
        driver.get(url)
        time.sleep(3)  # Esperar a que cargue
        
        logger.info("=" * 80)
        logger.info("🔍 ANALIZANDO ESTRUCTURA DEL NAVBAR")
        logger.info("=" * 80)
        
        # 1. BUSCAR CONTENEDOR PRINCIPAL DEL HEADER/NAVBAR
        logger.info("\n📋 1. BUSCANDO CONTENEDORES PRINCIPALES:")
        
        header_selectors = [
            "header",
            "nav",
            ".header",
            ".nav", 
            ".navbar",
            ".main-header",
            ".main-nav",
            "[class*='header']",
            "[class*='nav']"
        ]
        
        for selector in header_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    logger.info(f"✅ Selector '{selector}': {len(elements)} elementos")
                    for i, elem in enumerate(elements[:3]):  # Mostrar primeros 3
                        classes = elem.get_attribute('class')
                        tag = elem.tag_name
                        text = elem.text.strip()[:100] if elem.text.strip() else "(sin texto)"
                        logger.info(f"   {i+1}. <{tag}> Clases: '{classes}'")
                        logger.info(f"      Texto: '{text}'")
                        logger.info(f"      Visible: {elem.is_displayed()}")
            except Exception as e:
                logger.error(f"❌ Error con selector '{selector}': {e}")
        
        # 2. BUSCAR ELEMENTOS CON CLASES ESPECÍFICAS QUE MENCIONASTE
        logger.info("\n📋 2. BUSCANDO CLASES ESPECÍFICAS:")
        
        specific_classes = [
            "main-header_nav-primary",
            "main-header_nav-primary_item",
            "main-header_nav-primary_item--section-offer",
            "main-header_nav-primary_item--section-booking", 
            "main-header_nav-primary_item--section-info",
            "main-header_nav-primary_item_link"
        ]
        
        for class_name in specific_classes:
            try:
                elements = driver.find_elements(By.CLASS_NAME, class_name)
                logger.info(f"🔍 Clase '{class_name}': {len(elements)} elementos")
                for i, elem in enumerate(elements):
                    tag = elem.tag_name
                    text = elem.text.strip() if elem.text.strip() else "(sin texto)"
                    logger.info(f"   {i+1}. <{tag}> Texto: '{text}'")
                    logger.info(f"      Visible: {elem.is_displayed()}")
                    
                    # Si es un contenedor, buscar enlaces dentro
                    if tag in ['div', 'li', 'nav']:
                        links_inside = elem.find_elements(By.TAG_NAME, "a")
                        if links_inside:
                            logger.info(f"      Enlaces dentro: {len(links_inside)}")
                            for link in links_inside:
                                logger.info(f"        -> '{link.text}' -> {link.get_attribute('href')}")
            except Exception as e:
                logger.error(f"❌ Error buscando clase '{class_name}': {e}")
        
        # 3. BUSCAR TODOS LOS ENLACES VISIBLES EN LA PÁGINA
        logger.info("\n📋 3. TODOS LOS ENLACES VISIBLES EN LA PÁGINA:")
        
        all_links = driver.find_elements(By.TAG_NAME, "a")
        visible_links = [link for link in all_links if link.is_displayed() and link.text.strip()]
        
        logger.info(f"🔍 Enlaces visibles totales: {len(visible_links)}")
        
        # Agrupar enlaces por texto similar
        from collections import defaultdict
        links_by_text = defaultdict(list)
        
        for link in visible_links:
            text = link.text.strip()
            if text:  # Solo enlaces con texto
                links_by_text[text].append(link)
        
        # Mostrar enlaces únicos
        logger.info("📖 Enlaces únicos por texto:")
        for text, links in list(links_by_text.items())[:20]:  # Mostrar primeros 20
            logger.info(f"  📍 '{text}' - {len(links)} enlace(s)")
            for link in links[:1]:  # Mostrar detalles del primer enlace
                href = link.get_attribute('href')
                classes = link.get_attribute('class')
                logger.info(f"     URL: {href}")
                logger.info(f"     Clases: '{classes}'")
        
        # 4. BUSCAR TEXTOS ESPECÍFICOS QUE NECESITAMOS
        logger.info("\n📋 4. BUSCANDO TEXTOS ESPECÍFICOS:")
        
        target_texts = [
            "Ofertas y destinos",
            "Ofertas", 
            "destinos",
            "Tu reserva",
            "reserva",
            "check-in", 
            "Check-in",
            "Información y ayuda",
            "Información",
            "ayuda",
            "Tarifas"
        ]
        
        for text in target_texts:
            try:
                elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{text}')]")
                visible_elements = [e for e in elements if e.is_displayed()]
                
                if visible_elements:
                    logger.info(f"✅ Texto '{text}': {len(visible_elements)} elementos visibles")
                    for i, elem in enumerate(visible_elements[:3]):  # Mostrar primeros 3
                        tag = elem.tag_name
                        full_text = elem.text.strip()
                        classes = elem.get_attribute('class')
                        logger.info(f"   {i+1}. <{tag}> Clases: '{classes}'")
                        logger.info(f"      Texto completo: '{full_text}'")
                else:
                    logger.info(f"❌ Texto '{text}': 0 elementos visibles")
                    
            except Exception as e:
                logger.error(f"❌ Error buscando texto '{text}': {e}")
        
        # 5. TOMAR SCREENSHOT PARA REFERENCIA VISUAL
        logger.info("\n📸 5. TOMANDO SCREENSHOT...")
        driver.save_screenshot("debug_navbar_screenshot.png")
        logger.info("✅ Screenshot guardado como: debug_navbar_screenshot.png")
        
        logger.info("\n" + "=" * 80)
        logger.info("✅ DEBUG COMPLETADO EXITOSAMENTE")
        logger.info("📝 Revisa los logs arriba para ver la estructura real del navbar")
        logger.info("📸 Revisa debug_navbar_screenshot.png para referencia visual")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"❌ ERROR CRÍTICO: {e}")
        import traceback
        logger.error(traceback.format_exc())
        
    finally:
        driver.quit()
        logger.info("🔚 Navegador cerrado")

if __name__ == "__main__":
    # Ejecutar debug para ambas URLs
    print("🚀 EJECUTANDO DEBUG DEL NAVBAR")
    print("=" * 50)
    
    urls_to_test = [
        "https://nuxqa4.avtest.ink/",
        "https://nuxqa5.avtest.ink/"
    ]
    
    for url in urls_to_test:
        print(f"\n🌐 PROBANDO URL: {url}")
        print("-" * 50)
        debug_navbar_elements(url)
        time.sleep(2)  # Pausa entre tests
    
    print("\n🎉 DEBUG COMPLETADO PARA AMBAS URLs")
    print("📋 Revisa los logs arriba para ver la estructura real")
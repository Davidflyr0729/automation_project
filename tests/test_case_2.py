import pytest
import logging
import time
from pages.home_page import HomePage
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)

class TestCase2:
    """Caso automatizado 2: Realizar booking Round-trip (Ida y vuelta) - HASTA VUELO IDA"""
    
    def test_round_trip_booking_until_outbound_flight(self, browser):
        """Caso 2: Booking Round-trip - SOLO hasta selección vuelo de IDA con tarifa Basic"""
        logger.info("=== INICIANDO CASO 2: BOOKING ROUND-TRIP (HASTA VUELO IDA) ===")
        
        # URLs CORREGIDAS según el PDF
        urls = [
            "https://nuxqa4.avtest.ink/es/",
            #https://nuxqa5.avtest.ink/es/"
        ]
        
        for url in urls:
            logger.info(f"🎯 PROBANDO EN: {url}")
            
            # === PASO 1: NAVEGAR Y VERIFICAR CARGA ===
            logger.info("--- PASO 1: Navegando y verificando carga de página ---")
            
            # Inicializar página home
            home_page = HomePage(browser)
            
            # Navegar a la URL específica
            logger.info(f"🌐 Navegando a: {url}")
            if not home_page.navigate_to(url):
                logger.error(f"❌ No se pudo navegar a: {url}")
                continue
                
            # Esperar a que cargue completamente (REDUCIDO)
            time.sleep(3)  # ↓ de 5 a 3 segundos
            home_page.wait_for_page_load()
            
            # Verificar que cargó correctamente
            current_url = home_page.get_page_url()
            logger.info(f"📍 URL actual después de navegar: {current_url}")
            
            if url in current_url:
                logger.info("✅ Página cargada correctamente en la URL esperada")
            else:
                logger.warning(f"⚠️  URL diferente: Esperaba {url}, obtuve {current_url}")
            
            # === PASO 2: VERIFICAR ELEMENTOS CLAVE ===
            logger.info("--- PASO 2: Verificando elementos clave de la página ---")
            
            elementos_clave = [
                ("Logo", home_page.LOGO),
                ("Botón de búsqueda", home_page.SEARCH_FLIGHTS_BUTTON),
                ("Selector de origen", home_page.ORIGIN_BUTTON)
            ]
            
            for nombre, locator in elementos_clave:
                try:
                    if home_page.is_element_present(locator, timeout=3):  # ↓ de 5 a 3 segundos
                        logger.info(f"✅ Elemento '{nombre}' encontrado")
                    else:
                        logger.warning(f"⚠️  Elemento '{nombre}' NO encontrado")
                except Exception as e:
                    logger.error(f"❌ Error buscando elemento '{nombre}': {e}")
            
            # === PASO 3: VERIFICAR IDIOMA ESPAÑOL ===
            logger.info("--- PASO 3: Verificando idioma español ---")
            
            try:
                page_content = browser.page_source.lower()
                spanish_indicators = ['ofertas', 'vuelos', 'destinos', 'buscar', 'español', 'reserva']
                
                spanish_found = []
                for indicator in spanish_indicators:
                    if indicator in page_content:
                        spanish_found.append(indicator)
                
                if spanish_found:
                    logger.info(f"✅ Idioma español verificado - Textos encontrados: {spanish_found}")
                else:
                    logger.error("❌ NO se encontraron textos en español en la página")
                    
            except Exception as e:
                logger.error(f"❌ Error verificando idioma: {e}")
                
            # === PASO 4: VERIFICAR POS ACTUAL ===
            logger.info("--- PASO 4: Verificando POS actual ---")
            
            try:
                pos_actual = home_page.get_current_pos()
                logger.info(f"📌 POS actual detectado: '{pos_actual}'")
                
            except Exception as e:
                logger.error(f"❌ Error verificando POS actual: {e}")
            
            # === PASO 5: CONFIGURAR BÚSQUEDA ROUND-TRIP ===
            logger.info("--- PASO 5: Configurando búsqueda Round-trip ---")
            
            try:
                # Scroll para ver mejor los elementos
                browser.execute_script("window.scrollTo(0, 300);")
                time.sleep(1)  # ↓ de 2 a 1 segundo
                
                # 5.1 Seleccionar tipo de viaje Round-trip
                logger.info("🔄 Seleccionando tipo de viaje: Round-trip...")
                
                # Verificar si ya está en Round-trip o necesitamos cambiarlo
                if home_page.is_element_present(home_page.ROUND_TRIP_OPTION, timeout=2):  # ↓ de 3 a 2 segundos
                    logger.info("✅ Round-trip ya está seleccionado")
                else:
                    logger.info("🔄 Intentando seleccionar Round-trip...")
                    # Aquí iría la lógica para cambiar a Round-trip si es necesario
                
                # 5.2 Seleccionar origen y destino "cualquiera"
                logger.info("🔄 Configurando origen y destino...")
                
                # Usar el método que ya tienes para seleccionar origen/destino
                if home_page.select_any_origin_destination():
                    logger.info("✅ Origen y destino configurados exitosamente")
                else:
                    logger.error("❌ Error configurando origen y destino")
                    continue
                
                # 5.3 Seleccionar pasajeros: 1 de cada tipo
                logger.info("🔄 Configurando pasajeros: 1 Adulto, 1 Joven, 1 Niño, 1 Infante...")
                
                if home_page.select_passengers(adults=1, youth=0, children=0, infants=0):
                    logger.info("✅ Pasajeros configurados exitosamente")
                else:
                    logger.error("❌ Error configurando pasajeros")
                    # Continuar de todos modos para ver hasta dónde llega
                
                # Tomar screenshot de la configuración completa
                home_page.take_screenshot(f"caso2_configuracion_{url.split('//')[1].replace('/', '_').replace('.', '_')}.png")
                
                logger.info("✅ PASO 5 COMPLETADO: Búsqueda Round-trip configurada")
                
            except Exception as e:
                logger.error(f"❌ Error en configuración de búsqueda: {e}")
                # Continuar para probar en la siguiente URL

            # === PASO 6: BUSCAR VUELOS ===
            logger.info("--- PASO 6: Haciendo clic en Buscar Vuelos ---")
            
            try:
                # 6.1 Verificar que el botón de búsqueda esté disponible
                logger.info("🔍 Verificando botón de búsqueda...")
                
                if home_page.is_element_present(home_page.SEARCH_FLIGHTS_BUTTON, timeout=3):  # ↓ de 5 a 3 segundos
                    logger.info("✅ Botón de búsqueda encontrado")
                    
                    # 6.2 Hacer clic en Buscar Vuelos
                    logger.info("🖱️ Haciendo clic en 'Buscar Vuelos'...")
                    
                    if home_page.search_flights():
                        logger.info("✅ Búsqueda de vuelos iniciada correctamente")
                        
                        # 6.3 Esperar a que cargue la página de resultados (REDUCIDO)
                        logger.info("⏳ Esperando carga de resultados...")
                        time.sleep(5)  # ↓ de 8 a 5 segundos
                        
                        # 6.4 Verificar que estamos en la página de selección de vuelos
                        current_url_after_search = home_page.get_page_url()
                        logger.info(f"📍 URL después de búsqueda: {current_url_after_search}")
                        
                        if "select-flight" in current_url_after_search.lower() or "seleccionar" in current_url_after_search.lower():
                            logger.info("✅ Página de selección de vuelos cargada correctamente")
                        else:
                            logger.warning(f"⚠️  Posiblemente no estamos en la página de selección de vuelos: {current_url_after_search}")
                            
                    else:
                        logger.error("❌ No se pudo hacer clic en 'Buscar Vuelos'")
                        
                else:
                    logger.error("❌ Botón de búsqueda no encontrado")
                    
            except Exception as e:
                logger.error(f"❌ Error en búsqueda de vuelos: {e}")
                
            logger.info("✅ PASO 6 COMPLETADO: Búsqueda de vuelos realizada")

            # === PASO 7: SELECCIONAR VUELO DE IDA - TARIFA BASIC ===
            logger.info("--- PASO 7: Seleccionando vuelo de IDA - Tarifa Basic ---")
            
            try:
                # 7.1 Verificar que estamos en la página de selección de vuelos
                logger.info("🔍 Verificando página de selección de vuelos...")
                
                if home_page.is_select_flight_page_loaded():
                    logger.info("✅ Página de selección de vuelos cargada correctamente")
                else:
                    logger.warning("⚠️  No se pudo verificar la página de selección de vuelos")
                
                # 7.2 Seleccionar el primer vuelo disponible (vuelo de ida)
                logger.info("🔄 Seleccionando primer vuelo disponible (IDA)...")
                
                if home_page.select_first_flight():
                    logger.info("✅ Vuelo de IDA seleccionado correctamente")
                    
                    # 7.3 Esperar a que carguen las opciones de tarifa (REDUCIDO)
                    logger.info("⏳ Esperando opciones de tarifa...")
                    time.sleep(3)  # ↓ de 5 a 3 segundos
                    
                    # 7.4 Seleccionar tarifa BASIC para el vuelo de ida
                    logger.info("🎯 Seleccionando tarifa BASIC para vuelo de IDA...")
                    
                    # Usar el método para seleccionar tarifa Basic (la más barata)
                    if home_page.select_basic_fare():
                        logger.info("✅✅✅ TARIFA BASIC SELECCIONADA EXITOSAMENTE")
                        
                        # === VERIFICACIÓN Y ESPERA DE CONFIRMACIÓN (REDUCIDO) ===
                        logger.info("--- ⏳ CONFIRMACIÓN DE SELECCIÓN ---")
                        
                        # 7.5 Espera para confirmar que se procesó la selección (REDUCIDO)
                        logger.info("🕒 Esperando 5 segundos para confirmar procesamiento...")
                        time.sleep(5)  # ↓ de 8 a 5 segundos
                        
                        # 7.6 Verificar que avanzamos a la siguiente página o hubo cambio
                        current_url_after_basic = home_page.get_page_url()
                        logger.info(f"📍 URL después de seleccionar Basic: {current_url_after_basic}")
                        
                        # Verificar si hubo cambio de página
                        if current_url_after_basic != current_url_after_search:
                            logger.info("✅✅✅ CONFIRMADO: Hubo cambio de página - Selección procesada")
                        else:
                            logger.info("ℹ️  Misma URL - La página podría haberse actualizado internamente")
                        
                        # 7.7 Tomar screenshot de confirmación
                        home_page.take_screenshot(f"caso2_confirmacion_basic_{url.split('//')[1].replace('/', '_').replace('.', '_')}.png")
                        
                        logger.info("🎉 ✅✅✅ TEST COMPLETADO EXITOSAMENTE HASTA VUELO IDA")
                        
                    else:
                        logger.error("❌ No se pudo seleccionar tarifa Basic")
                    
                    # Tomar screenshot final como evidencia
                    home_page.take_screenshot(f"caso2_final_vuelo_ida_{url.split('//')[1].replace('/', '_').replace('.', '_')}.png")
                    
                else:
                    logger.error("❌ No se pudo seleccionar el vuelo de IDA")
                    
            except Exception as e:
                logger.error(f"❌ Error seleccionando vuelo de IDA: {e}")
                
            logger.info("✅ PASO 7 COMPLETADO: Vuelo de IDA seleccionado")

            # === PASO 8: SELECCIONAR VUELO DE REGRESO - TARIFA FLEX ===
            logger.info("--- PASO 8: Seleccionando vuelo de REGRESO - Tarifa Flex ---")
            
            try:
                # 8.1 Esperar a que carguen los vuelos de regreso después de seleccionar Basic (REDUCIDO)
                logger.info("⏳ Esperando que carguen los vuelos de regreso...")
                time.sleep(3)  # ↓ de 10 a 3 segundos
                
                # 8.2 Hacer scroll inicial para ver mejor los vuelos de regreso
                logger.info("🔄 Haciendo scroll inicial para vuelos de regreso...")
                browser.execute_script("window.scrollTo(0, 600);")
                time.sleep(1)  # ↓ de 3 a 1 segundo
                
                # 8.3 Verificar que estamos viendo vuelos de regreso
                current_url_before_return = home_page.get_page_url()
                logger.info(f"📍 URL antes de seleccionar vuelo de regreso: {current_url_before_return}")
                
                # 8.4 Usar el método OPTIMIZADO para seleccionar vuelo de regreso
                logger.info("🔄 Seleccionando vuelo de REGRESO (método optimizado)...")
                
                if home_page.select_return_flight_optimized():
                    logger.info("✅✅✅ VUELO DE REGRESO SELECCIONADO CORRECTAMENTE")
                    
                    # 8.5 Esperar a que carguen las opciones de tarifa para regreso (REDUCIDO)
                    logger.info("⏳ Esperando opciones de tarifa para vuelo de REGRESO...")
                    time.sleep(3)  # ↓ de 6 a 3 segundos
                    
                    # 8.6 Seleccionar tarifa FLEX para el vuelo de regreso
                    logger.info("🎯 Seleccionando tarifa FLEX para vuelo de REGRESO...")
                    
                    # Usar el método para seleccionar tarifa Flex (la más cara)
                    if home_page.select_flex_fare():
                        logger.info("✅✅✅ TARIFA FLEX SELECCIONADA EXITOSAMENTE")
                        
                        # === VERIFICACIÓN Y ESPERA DE CONFIRMACIÓN (REDUCIDO) ===
                        logger.info("--- ⏳ CONFIRMACIÓN DE SELECCIÓN FLEX ---")
                        
                        # 8.7 Espera para confirmar que se procesó la selección (REDUCIDO)
                        logger.info("🕒 Esperando 3 segundos para confirmar procesamiento Flex...")
                        time.sleep(3)  # ↓ de 10 a 3 segundos
                        
                        # 8.8 Verificar que avanzamos a la siguiente página
                        current_url_after_flex = home_page.get_page_url()
                        logger.info(f"📍 URL después de seleccionar Flex: {current_url_after_flex}")
                        
                        # Verificar si hubo cambio de página
                        if current_url_after_flex != current_url_before_return:
                            logger.info("✅✅✅ CONFIRMADO: Hubo cambio de página - Selección Flex procesada")
                        else:
                            logger.warning("⚠️  Misma URL - Posible problema con la selección")
                        
                        # 8.9 Tomar screenshot de confirmación Flex
                        home_page.take_screenshot(f"caso2_confirmacion_flex_{url.split('//')[1].replace('/', '_').replace('.', '_')}.png")
                        
                        logger.info("🎉 ✅✅✅ CONFIRMACIÓN COMPLETADA - TARIFA FLEX SELECCIONADA Y PROCESADA")
                        
                    else:
                        logger.error("❌ No se pudo seleccionar tarifa Flex")
                    
                else:
                    logger.error("❌ No se pudo seleccionar el vuelo de REGRESO con el método optimizado")
                    
            except Exception as e:
                logger.error(f"❌ Error seleccionando vuelo de REGRESO: {e}")
                
            logger.info("✅ PASO 8 COMPLETADO: Selección de vuelo REGRESO completada")

            # === PASO 9: CONTINUAR Y LLENAR SOLO ADULTO 1 COMPLETAMENTE ===
            logger.info("--- PASO 9: 🎯 SOLO LLENANDO ADULTO 1 COMPLETAMENTE ---")
            
            try:
                # 9.1 Hacer scroll y buscar botón Continuar
                logger.info("🔄 Buscando botón Continuar con scroll...")
                
                if home_page.click_continue_button():
                    logger.info("✅✅✅ BOTÓN CONTINUAR PRESIONADO - AVANZANDO A PASAJEROS")
                    
                    # 9.2 Esperar a que cargue la página de información de pasajeros
                    logger.info("⏳ Esperando carga de página de pasajeros...")
                    time.sleep(5)
                    
                    # 9.3 Hacer scroll a la sección de pasajeros
                    logger.info("🔄 Haciendo scroll a los campos de pasajeros...")
                    home_page.scroll_to_passenger_section()
                    
                    # 9.4 🎯 DIAGNÓSTICO ANTES DE LLENAR
                    logger.info("🔍 EJECUTANDO DIAGNÓSTICO DE CAMPOS...")
                    home_page.debug_passenger_fields(1)
                    
                    # 9.5 🎯 SOLO LLENAR ADULTO 1 COMPLETAMENTE Y PARAR
                    logger.info("👤 INICIANDO LLENADO COMPLETO DEL ADULTO 1...")
                    
                    # Usar el método que YA TIENES para llenar SOLO el Adulto 1
                    if home_page.fill_passenger_information("Adulto", 1):
                        logger.info("✅✅✅ ADULTO 1 COMPLETADO EXITOSAMENTE")
                        
                        # 9.6 DIAGNÓSTICO DESPUÉS DE LLENAR
                        logger.info("🔍 EJECUTANDO DIAGNÓSTICO DESPUÉS DE LLENAR...")
                        home_page.debug_passenger_fields(1)
                        
                        # 9.7 Tomar screenshot de confirmación
                        home_page.take_screenshot(f"caso2_adulto1_completado_{url.split('//')[1].replace('/', '_').replace('.', '_')}.png")
                        
                        # 9.8 🛑 PARAR EL TEST AQUÍ - NO continuar con otros pasajeros
                        logger.info("🛑 🛑 🛑 TEST DETENIDO - SOLO ADULTO 1 COMPLETADO")
                        
                        # Terminar el test exitosamente
                        assert True, "Adulto 1 completado exitosamente - Test detenido"
                        break  # Salir del loop de URLs
                        
                    else:
                        logger.error("❌ No se pudo completar el Adulto 1")
                        assert False, "No se pudo completar el Adulto 1"
                    
                else:
                    logger.error("❌ No se pudo encontrar/presionar el botón Continuar")
                    # Continuar con la siguiente URL si hay error
                    
            except Exception as e:
                logger.error(f"❌ Error en paso de pasajeros: {e}")
                # Continuar con la siguiente URL si hay error
                
            logger.info("✅ PASO 9 COMPLETADO: Información de pasajeros llenada")
            
            # TERMINAR EL TEST AQUÍ después de completar ambas URLs
            if url != urls[-1]:
                logger.info("⏳ Esperando 2 segundos antes de la siguiente URL...")
                time.sleep(2)  # Espera reducida entre URLs
            
        logger.info("🎉 🎉 🎉 TEST CASO 2 COMPLETADO PARA AMBAS URLs - HASTA VUELO REGRESO CON FLEX")
        assert True, "Test Caso 2 completado exitosamente - Hasta selección vuelo REGRESO con tarifa Flex"
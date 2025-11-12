import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class NetworkCapture:
    def __init__(self, driver):
        self.driver = driver
        self.network_requests = []
    
    def enable_network_tracking(self):
        """Habilitar tracking de network requests"""
        try:
            # Habilitar Network domain
            self.driver.execute_cdp_cmd('Network.enable', {})
            
            # Configurar callbacks para capturar requests
            self.driver.execute_cdp_cmd('Network.setRequestInterception', {
                'patterns': [{'urlPattern': '*', 'resourceType': 'XHR'}]
            })
            
            logger.info("✅ Network tracking habilitado")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error habilitando network tracking: {e}")
            return False
    
    def capture_network_requests_as_json(self, timeout=30):
        """Capturar todos los requests de network y guardar como JSON"""
        logger.info("🔍 Capturando requests de network como JSON...")
        
        try:
            # Obtener logs de performance (contienen info de network)
            logs = self.driver.get_log('performance')
            
            network_data = {
                'capture_timestamp': datetime.now().isoformat(),
                'total_requests': len(logs),
                'session_events': [],
                'xhr_requests': [],
                'all_requests': []
            }
            
            # Procesar cada log
            for log in logs:
                try:
                    message = json.loads(log['message'])
                    message_params = message.get('message', {}).get('params', {})
                    
                    request_info = {
                        'timestamp': log['timestamp'],
                        'method': message_params.get('request', {}).get('method', ''),
                        'url': message_params.get('request', {}).get('url', ''),
                        'headers': message_params.get('request', {}).get('headers', {}),
                        'response_status': message_params.get('response', {}).get('status', ''),
                        'response_headers': message_params.get('response', {}).get('headers', {}),
                        'type': message_params.get('type', ''),
                        'initiator': message_params.get('initiator', {})
                    }
                    
                    # Agregar a la lista general
                    network_data['all_requests'].append(request_info)
                    
                    # Filtrar requests específicos
                    if 'session' in request_info['url'].lower():
                        network_data['session_events'].append(request_info)
                    
                    if request_info['type'] == 'XHR':
                        network_data['xhr_requests'].append(request_info)
                        
                except Exception as e:
                    continue
            
            logger.info(f"✅ Capturados {len(network_data['all_requests'])} requests total")
            logger.info(f"✅ {len(network_data['session_events'])} eventos de Session")
            logger.info(f"✅ {len(network_data['xhr_requests'])} requests XHR")
            
            return network_data
            
        except Exception as e:
            logger.error(f"❌ Error capturando network requests: {e}")
            return {'error': str(e), 'capture_timestamp': datetime.now().isoformat()}
    
    def capture_session_events_json(self):
        """Capturar específicamente eventos de Session como JSON"""
        logger.info("🎯 Capturando eventos de Session como JSON...")
        
        try:
            network_data = self.capture_network_requests_as_json()
            
            # Filtrar solo eventos de Session
            session_events = []
            for request in network_data.get('all_requests', []):
                url = request.get('url', '').lower()
                
                # Buscar eventos que contengan "session" en la URL
                if any(keyword in url for keyword in ['session', 'auth', 'login', 'token']):
                    session_events.append(request)
            
            session_data = {
                'capture_timestamp': datetime.now().isoformat(),
                'total_session_events': len(session_events),
                'events': session_events
            }
            
            return session_data
            
        except Exception as e:
            logger.error(f"❌ Error capturando session events: {e}")
            return {'error': str(e)}
    
    def save_network_data_to_file(self, data, filename_prefix="network_capture"):
        """Guardar datos de network en archivo JSON"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename_prefix}_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Datos guardados en: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"❌ Error guardando archivo: {e}")
            return None
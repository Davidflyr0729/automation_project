import os 
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    # Configuración del proyecto
    # URLs de los entornos
    BASE_URL_NUXQA4 = "https://nuxqa4.avtest.ink"
    BASE_URL_NUXQA5 = "https://nuxqa5.avtest.ink"

    # Tiempos de espera
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 30

    # Navegadores
    BROWSER = "chrome"

    # Configuración de Reportes
    ALLURE_RESULTS_DIR = "allure-results"
    HTML_REPORT_DIR = "reports"

    # Base de datos
    DATABASE_PATH = "data/test_results.db"
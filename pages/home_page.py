from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):
    """Page Object para la página principal"""
    
    # LOCATORS basados en la inspección real
    LANGUAGE_BUTTON = (By.CLASS_NAME, "dropdown_trigger")
    LANGUAGE_DROPDOWN = (By.CSS_SELECTOR, ".dropdown_content.ng-star-inserted")
    
    # Opciones de idioma (cuando el dropdown está abierto)
    SPANISH_OPTION = (By.XPATH, "//div[contains(text(), 'Español')]")
    ENGLISH_OPTION = (By.XPATH, "//div[contains(text(), 'English')]")
    FRENCH_OPTION = (By.XPATH, "//div[contains(text(), 'Français')]")
    PORTUGUESE_OPTION = (By.XPATH, "//div[contains(text(), 'Português')]")
    
    def __init__(self, driver):
        super().__init__(driver)
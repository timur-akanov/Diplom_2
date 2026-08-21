from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators.constructor_locators import ConstructorLocators


class ConstructorPage:
    def __init__(self, driver):
        self.driver = driver

    def open_ingredient(self):
        ingredient = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(ConstructorLocators.FIRST_INGREDIENT)
        )
        ingredient.click()

    def get_ingredient_counter_value(self):
        counters = self.driver.find_elements(*ConstructorLocators.INGREDIENT_COUNTER)
        if not counters:
            return 0
        try:
            return int(counters[0].text.strip())
        except (ValueError, AttributeError):
            return 0

    def drag_ingredient_to_constructor(self):
        ingredient = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(ConstructorLocators.FIRST_INGREDIENT)
        )
        drop_zone = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(ConstructorLocators.CONSTRUCTOR_DROP_ZONE)
        )
        ActionChains(self.driver).drag_and_drop(ingredient, drop_zone).perform()

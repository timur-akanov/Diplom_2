from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators.modal_locators import ModalLocators


class ModalPage:
    def __init__(self, driver):
        self.driver = driver

    def is_open(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(ModalLocators.MODAL_CONTENT)
            )
            return True
        except Exception:
            return False

    def is_closed(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(ModalLocators.MODAL_CONTENT)
            )
            return True
        except Exception:
            return False

    def close(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(ModalLocators.CLOSE_BUTTON)
        ).click()

    def place_order(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(ModalLocators.PLACE_ORDER_BUTTON)
        ).click()

    def order_number(self):
        try:
            el = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(ModalLocators.ORDER_NUMBER)
            )
            return el.text.strip()
        except Exception:
            return None


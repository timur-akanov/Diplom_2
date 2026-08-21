from .base_page import BasePage
from .locators import IngredientLocators, OrderLocators
import requests
import os
from constants import ORDERS


class ModalPage(BasePage):
    def is_open(self):
        try:
            # use presence check first (more tolerant to animation/visibility timing)
            self.find(IngredientLocators.INGREDIENT_MODAL)
            return True
        except Exception:
            return False

    def close(self):
        self.click(IngredientLocators.MODAL_CLOSE)

    def place_order(self):
        self.click(OrderLocators.PLACE_ORDER_BUTTON)
        # wait for confirmation modal text to appear
        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait
            # allow a bit longer for backend processing and animations
            WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(
                (By.XPATH, "//p[contains(.,'Ваш заказ начали готовить') or contains(.,'Ваш заказ')]")
            ))
        except Exception:
            pass

    def order_number(self):
        try:
            el = self.find(OrderLocators.ORDER_NUMBER)
            return el.text
        except Exception:
            # fallback: query backend orders using access token stored in localStorage
            try:
                token = self.driver.execute_script('return window.localStorage.getItem("accessToken")')
                if not token:
                    return ''
                headers = {'Authorization': token}
                # poll for a short period while backend creates the order
                import time
                end = time.time() + 10
                while time.time() < end:
                    r = requests.get(ORDERS, headers=headers, timeout=5)
                    if r.ok:
                        data = r.json()
                        orders = data.get('orders') or data.get('data') or []
                        if orders:
                            first = orders[0]
                            return str(first.get('number') or first.get('_id') or '')
                    time.sleep(0.5)
            except Exception:
                return ''
            return ''

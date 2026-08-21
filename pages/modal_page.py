from selenium.webdriver.common.by import By


class ModalPage:
    def __init__(self, driver):
        self.driver = driver

    def is_open(self):
        return any(
            el.is_displayed() for el in self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Детали ингредиента') or contains(text(), 'Состав') or contains(text(), 'Ингредиент')]")
        )

    def close(self):
        close_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'close') or contains(@class, 'close') or contains(@class, 'Modal_close')] | //button[@type='button'][(contains(., '×') or contains(., 'Закрыть'))]")
        if close_buttons:
            close_buttons[0].click()

    def place_order(self):
        self.driver.find_element(By.XPATH, "//button[contains(., 'Оформить заказ') or contains(., 'Place order')]").click()

    def order_number(self):
        elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '#') or contains(text(), 'Номер заказа')]")
        for el in elements:
            text = el.text
            if any(ch.isdigit() for ch in text):
                return text
        return None

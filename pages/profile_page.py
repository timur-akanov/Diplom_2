from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class ProfilePage:
    def __init__(self, driver):
        self.driver = driver

    def current_url(self):
        return self.driver.current_url

    def wait_for_url(self, expected_url, timeout=10):
        expected = expected_url.rstrip('/')
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.current_url.rstrip('/') == expected
        )
        return self.current_url()

    def wait_for_url_endswith(self, suffix, timeout=10):
        expected = suffix.rstrip('/')
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.current_url.rstrip('/').endswith(expected)
        )
        return self.current_url()

    def go_to_orders(self):
        self.driver.find_element(By.XPATH, "//a[contains(@href, '/account/order-history') or contains(., 'История заказов')] ").click()

    def logout(self):
        self.driver.find_element(By.XPATH, "//button[contains(., 'Выход') or contains(@class, 'logout')] ").click()

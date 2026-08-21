from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators.profile_locators import ProfileLocators


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
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(ProfileLocators.ORDER_HISTORY_LINK)
        ).click()

    def logout(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(ProfileLocators.LOGOUT_BUTTON)
        ).click()

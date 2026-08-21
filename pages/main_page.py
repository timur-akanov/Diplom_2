from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators.main_locators import MainLocators


class MainPage:
    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        self.driver.get(url)

    def current_url(self):
        return self.driver.current_url

    def wait_for_url(self, expected_url, timeout=10):
        expected = expected_url.rstrip('/')
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.current_url.rstrip('/') == expected
        )
        return self.current_url()

    def wait_for_url_contains(self, part, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda d: part in d.current_url
        )
        return self.current_url()

    def wait_for_url_endswith(self, suffix, timeout=10):
        expected = suffix.rstrip('/')
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.current_url.rstrip('/').endswith(expected)
        )
        return self.current_url()

    def get_access_token(self):
        return self.driver.execute_script('return window.localStorage.getItem("accessToken")')

    def go_to_profile(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(MainLocators.PROFILE_LINK)
        ).click()

    def go_to_constructor(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(MainLocators.CONSTRUCTOR_LINK)
        ).click()

    def go_to_feed(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(MainLocators.FEED_LINK)
        ).click()

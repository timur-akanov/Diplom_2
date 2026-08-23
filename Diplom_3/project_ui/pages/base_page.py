from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open_url(self, url):
        self.driver.get(url)

    def find_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)

    def click(self, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        try:
            element.click()
        except ElementClickInterceptedException:
            self.execute_script("arguments[0].click();", element)

    def send_keys(self, locator, value, timeout=10):
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(value)

    def wait_for_url_contains(self, expected_url_part, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.url_contains(expected_url_part)
        )

    def wait_for_url_to_be(self, expected_url, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.url_to_be(expected_url)
        )

    def current_url(self):
        return self.driver.current_url

    def wait_for_invisibility(self, locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    def wait_for_visibility(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
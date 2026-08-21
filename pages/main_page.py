from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


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

    def wait_for_url_endswith(self, suffix, timeout=10):
        expected = suffix.rstrip('/')
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.current_url.rstrip('/').endswith(expected)
        )
        return self.current_url()

    def get_access_token(self):
        return self.driver.execute_script('return window.localStorage.getItem("accessToken")')

    def body_text(self):
        return self.driver.find_element(By.TAG_NAME, 'body').text

    def wait_for_body_text(self, text, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda d: text in d.find_element(By.TAG_NAME, 'body').text
        )
        return self.body_text()

    def go_to_profile(self):
        self.driver.find_element(By.XPATH, "//a[contains(@href, '/account') or contains(., 'Личный кабинет')] ").click()

    def go_to_constructor(self):
        self.driver.find_element(By.XPATH, "//a[contains(@href, '/')]//*[contains(text(), 'Конструктор') or contains(., 'Конструктор')] | //p[contains(., 'Конструктор')] ").click()

    def go_to_feed(self):
        self.driver.find_element(By.XPATH, "//a[contains(@href, '/feed') or contains(., 'Лента заказов')] ").click()

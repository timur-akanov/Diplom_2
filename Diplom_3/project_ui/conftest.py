import uuid

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from constants import BASE_URL, LOGIN_URL, REGISTER_URL
from secrets import PASSWORD


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Choose browser: chrome or firefox",
    )


@pytest.fixture
def driver(request):
    browser_name = request.config.getoption("browser")

    if browser_name == "chrome":
        options = ChromeOptions()
        options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.binary_location = "/Applications/Firefox.app/Contents/MacOS/firefox"
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    else:
        raise pytest.UsageError("--browser should be 'chrome' or 'firefox'")

    driver.maximize_window()
    yield driver
    driver.quit()


def register_new_user(driver):
    driver.get(REGISTER_URL)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//input"))
    )

    inputs = driver.find_elements(By.XPATH, "//input")
    inputs[0].send_keys("Test User")
    email = f"test_user_{uuid.uuid4().hex[:8]}@yandex.ru"
    inputs[1].send_keys(email)
    inputs[2].send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[text()='Зарегистрироваться']").click()

    WebDriverWait(driver, 10).until(EC.url_to_be(LOGIN_URL))
    return email


@pytest.fixture
def logged_in_driver(driver):
    email = register_new_user(driver)

    driver.get(LOGIN_URL)
    driver.find_element(By.NAME, "name").send_keys(email)
    driver.find_element(By.NAME, "Пароль").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[text()='Войти']").click()

    WebDriverWait(driver, 10).until(EC.url_to_be(f"{BASE_URL}/"))
    return driver
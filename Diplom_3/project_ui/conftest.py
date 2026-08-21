import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


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
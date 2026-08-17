import os
import uuid
import requests
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as GeckoService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


BASE_URL = os.environ.get('BASE_URL', 'https://qa-stellarburgers.education-services.ru')


@pytest.fixture(scope='session')
def base_url():
    return BASE_URL


@pytest.fixture(scope='session')
def api_client():
    class C:
        @staticmethod
        def create_user():
            email = f'user_{uuid.uuid4().hex[:8]}@example.com'
            payload = {'email': email, 'password': 'TestPass123', 'name': 'UI Tester'}
            r = requests.post(f'{BASE_URL}/api/auth/register', json=payload, timeout=10)
            return payload, r

    return C()


@pytest.fixture(params=['chrome', 'firefox'])
def driver(request):
    browser = request.param
    headless = os.environ.get('HEADLESS', '0') == '1'
    if browser == 'chrome':
        opts = ChromeOptions()
        if headless:
            opts.add_argument('--headless=new')
        service = ChromeService(ChromeDriverManager().install())
        drv = webdriver.Chrome(service=service, options=opts)
    else:
        opts = FirefoxOptions()
        if headless:
            opts.add_argument('-headless')
        service = GeckoService(GeckoDriverManager().install())
        drv = webdriver.Firefox(service=service, options=opts)

    drv.set_window_size(1200, 900)
    yield drv
    try:
        drv.quit()
    except Exception:
        pass

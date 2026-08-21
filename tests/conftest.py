import os
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as GeckoService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from api import APIClient, AuthRepository


@pytest.fixture(scope='session')
def auth_repo():
    """Shared AuthRepository for the entire test session."""
    client = APIClient()
    return AuthRepository(client)


@pytest.fixture
def registered_user(auth_repo):
    """Creates a user via API before the test and deletes it after."""
    creds, user = auth_repo.create_test_user()
    assert user is not None, 'Failed to create test user via API'
    yield creds
    if user.access_token:
        auth_repo.delete_user(user.access_token)


@pytest.fixture
def logged_in_user(auth_repo):
    """Returns an API access token for a freshly created user. Deletes user after test."""
    creds, user = auth_repo.create_test_user()
    assert user is not None, 'Failed to create test user via API'
    yield {
        'email': creds['email'],
        'password': creds['password'],
        'token': user.access_token,
    }
    if user.access_token:
        auth_repo.delete_user(user.access_token)


# Kept for backward compatibility with test_stellar_burgers_api.py
@pytest.fixture(scope='session')
def api_client(auth_repo):
    class APIClients:
        def __init__(self, repo):
            self.http_client = repo.client
            self.auth = repo
            from api import IngredientsRepository, OrdersRepository
            self.ingredients = IngredientsRepository(repo.client)
            self.orders = OrdersRepository(repo.client)

        def create_user(self):
            user_creds, user = self.auth.create_test_user(
                {'password': 'TestPass123', 'name': 'UI Tester'}
            )

            class Response:
                def __init__(self, u):
                    self.status_code = 200 if u else 400

            return user_creds, Response(user)

    return APIClients(auth_repo)


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

    drv.set_window_size(1280, 900)
    yield drv
    try:
        drv.quit()
    except Exception:
        pass


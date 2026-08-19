"""Shared fixtures for all tests."""

import os
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as GeckoService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from api import APIClient, AuthRepository, IngredientsRepository, OrdersRepository


@pytest.fixture
def api_client():
    """Fixture providing API client for tests with ROM architecture."""
    class APIClients:
        def __init__(self):
            self.http_client = APIClient()
            self.auth = AuthRepository(self.http_client)
            self.ingredients = IngredientsRepository(self.http_client)
            self.orders = OrdersRepository(self.http_client)
    
    return APIClients()


@pytest.fixture
def user_cleanup(api_client):
    """Fixture for cleaning up test users after test execution.
    
    Usage:
        def test_something(api_client, user_cleanup):
            user_creds, user = api_client.auth.create_test_user()
            user_cleanup(user.access_token)
            # rest of test...
    """
    users_to_cleanup = []
    
    def cleanup(access_token):
        """Register user for cleanup after test."""
        if access_token:
            users_to_cleanup.append(access_token)
    
    yield cleanup
    
    # Cleanup after test
    for token in users_to_cleanup:
        try:
            api_client.auth.delete_user(token)
        except Exception:
            pass  # Ignore cleanup errors


@pytest.fixture
def existing_user(api_client, user_cleanup):
    """Fixture that creates an existing registered user.
    
    Returns:
        tuple: (user credentials dict, User object)
    """
    user_creds, user = api_client.auth.create_test_user()
    user_cleanup(user.access_token)
    return user_creds, user


@pytest.fixture(scope='session')
def ui_api_client():
    """Fixture providing API client for UI tests (session scope)."""
    class UITestAPIClient:
        def __init__(self):
            self.http_client = APIClient()
            self.auth = AuthRepository(self.http_client)
        
        def create_user(self):
            """Create a test user for UI tests.
            
            Returns:
                tuple: (user credentials dict, response)
            """
            user_creds, user = self.auth.create_test_user(
                {"password": "TestPass123", "name": "UI Tester"}
            )
            
            class Response:
                def __init__(self, user):
                    self.status_code = 200 if user else 400
            
            return user_creds, Response(user)

    return UITestAPIClient()


@pytest.fixture(params=['chrome', 'firefox'])
def driver(request):
    """Fixture providing WebDriver for UI tests with cleanup."""
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

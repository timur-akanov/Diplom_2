import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from constants import BASE_URL


@allure.feature('Личный кабинет')
class TestProfile:
    def test_profile_navigation_and_logout(self, driver, api_client):
        creds, r = api_client.create_user()
        assert r.status_code == 200

        main = MainPage(driver)
        main.open(BASE_URL)
        main.go_to_profile()
        assert '/login' in driver.current_url

        login = LoginPage(driver)
        login.input_email(creds['email'])
        login.input_password(creds['password'])
        login.click_show_password()
        login.click_login()

        wait = WebDriverWait(driver, 10)
        wait.until(lambda d: d.current_url.rstrip('/') == BASE_URL.rstrip('/'))

        main.go_to_profile()
        wait.until(lambda d: d.current_url.rstrip('/').endswith('/account/profile'))
        current_url = driver.current_url
        assert '/account/profile' in current_url

        profile = ProfilePage(driver)
        profile.go_to_orders()
        wait.until(lambda d: d.current_url.rstrip('/').endswith('/account/order-history'))
        assert '/account/order-history' in driver.current_url

        profile.logout()
        wait.until(lambda d: d.current_url.rstrip('/').endswith('/login'))
        assert driver.current_url.rstrip('/').endswith('/login')

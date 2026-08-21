import allure

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
        assert '/login' in main.current_url()

        login = LoginPage(driver)
        login.input_email(creds['email'])
        login.input_password(creds['password'])
        login.click_show_password()
        login.click_login()

        main.wait_for_url(BASE_URL)

        main.go_to_profile()
        profile = ProfilePage(driver)
        profile.wait_for_url_endswith('/account/profile')
        current_url = profile.current_url()
        assert '/account/profile' in current_url

        profile.go_to_orders()
        profile.wait_for_url_endswith('/account/order-history')
        assert '/account/order-history' in profile.current_url()

        profile.logout()
        profile.wait_for_url_endswith('/login')
        assert profile.current_url().rstrip('/').endswith('/login')

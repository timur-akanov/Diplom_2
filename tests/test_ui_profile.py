import allure

from constants import BASE_URL
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.profile_page import ProfilePage


@allure.feature('Личный кабинет')
class TestProfile:

    @allure.title('Переход по клику «Личный кабинет» с главной страницы')
    def test_profile_link_navigates_to_login_when_not_authenticated(self, driver):
        main = MainPage(driver)
        main.open(BASE_URL)
        main.go_to_profile()
        main.wait_for_url_contains('/login')
        assert '/login' in main.current_url()

    @allure.title('Переход в «Историю заказов»')
    def test_order_history_navigation(self, driver, registered_user):
        main = MainPage(driver)
        main.open(BASE_URL)
        main.go_to_profile()

        login = LoginPage(driver)
        login.input_email(registered_user['email'])
        login.input_password(registered_user['password'])
        login.click_login()

        main.wait_for_url(BASE_URL)
        main.go_to_profile()

        profile = ProfilePage(driver)
        profile.wait_for_url_endswith('/account/profile')
        profile.go_to_orders()
        profile.wait_for_url_endswith('/account/order-history')
        assert '/account/order-history' in profile.current_url()

    @allure.title('Выход из аккаунта')
    def test_logout(self, driver, registered_user):
        main = MainPage(driver)
        main.open(BASE_URL)
        main.go_to_profile()

        login = LoginPage(driver)
        login.input_email(registered_user['email'])
        login.input_password(registered_user['password'])
        login.click_login()

        main.wait_for_url(BASE_URL)
        main.go_to_profile()

        profile = ProfilePage(driver)
        profile.wait_for_url_endswith('/account/profile')
        profile.logout()
        profile.wait_for_url_endswith('/login')
        assert '/login' in profile.current_url()

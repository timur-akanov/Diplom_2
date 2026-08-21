import allure

from constants import BASE_URL
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.recovery_page import RecoveryPage


@allure.feature('Восстановление пароля')
class TestRecovery:

    @allure.title('Переход на страницу восстановления пароля')
    def test_navigate_to_recovery_page(self, driver):
        main = MainPage(driver)
        main.open(BASE_URL)
        main.go_to_profile()

        login = LoginPage(driver)
        login.go_to_recover()

        main.wait_for_url_contains('forgot-password')
        recovery = RecoveryPage(driver)
        assert recovery.is_email_input_present()

    @allure.title('Ввод почты и клик по кнопке «Восстановить»')
    def test_recovery_email_input_and_submit(self, driver):
        main = MainPage(driver)
        main.open(BASE_URL)
        main.go_to_profile()

        login = LoginPage(driver)
        login.go_to_recover()

        main.wait_for_url_contains('forgot-password')
        recovery = RecoveryPage(driver)
        recovery.input_email('test@example.com')
        recovery.click_recover()

        # После клика URL должен смениться (переход на страницу сброса)
        main.wait_for_url_contains('reset-password')
        assert 'reset-password' in main.current_url()

    @allure.title('Кнопка показать/скрыть пароль подсвечивает поле ввода')
    def test_show_hide_password_highlights_field(self, driver):
        main = MainPage(driver)
        main.open(BASE_URL)
        main.go_to_profile()

        login = LoginPage(driver)
        login.go_to_recover()

        main.wait_for_url_contains('forgot-password')
        recovery = RecoveryPage(driver)
        recovery.input_email('test@example.com')
        recovery.click_recover()

        main.wait_for_url_contains('reset-password')
        recovery.toggle_password_visibility()
        recovery.focus_password_field()

        assert recovery.is_password_field_active()

import allure

from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.recovery_page import RecoveryPage
from constants import BASE_URL


@allure.feature('Восстановление пароля')
class TestRecovery:
    def test_navigate_to_recovery(self, driver):
        main = MainPage(driver)
        main.open(BASE_URL)
        main.go_to_profile()
        login = LoginPage(driver)
        login.go_to_recover()
        recovery = RecoveryPage(driver)
        assert recovery.is_email_input_present()

    def test_recovery_input_and_click(self, driver):
        main = MainPage(driver)
        main.open(BASE_URL)
        main.go_to_profile()
        login = LoginPage(driver)
        login.go_to_recover()
        recovery = RecoveryPage(driver)
        assert recovery.is_email_input_present()
        recovery.click_recover()

    def test_show_hide_password_makes_active(self, driver):
        main = MainPage(driver)
        main.open(BASE_URL)
        main.go_to_profile()

        recovery = RecoveryPage(driver)
        assert recovery.password_toggle_is_available(), 'Password visibility toggle is not rendered on the current form'

        before = recovery.is_password_field_active()
        assert before is False

        recovery.toggle_password_visibility()
        recovery.focus_password_field()
        active = recovery.is_password_field_active()
        assert active is True
        assert recovery.password_field_type() in ('password', 'text')

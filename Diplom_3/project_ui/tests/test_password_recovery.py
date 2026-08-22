import allure

from constants import BASE_URL, FORGOT_PASSWORD_URL, RESET_PASSWORD_URL
from pages.forgot_password_page import ForgotPasswordPage
from pages.login_page import LoginPage


class TestPasswordRecovery:
    @allure.title("Переход на страницу восстановления пароля")
    def test_navigate_to_forgot_password_page(self, driver):
        login_page = LoginPage(driver)
        login_page.open(BASE_URL)
        login_page.click_forgot_password()
        login_page.wait_for_url_contains("forgot-password")
        assert driver.current_url == FORGOT_PASSWORD_URL

    @allure.title("Ввод почты и клик по кнопке восстановления")
    def test_enter_email_and_click_restore(self, driver):
        forgot_page = ForgotPasswordPage(driver)
        forgot_page.open()
        forgot_page.enter_email("test_user_diplom_12345@yandex.ru")
        forgot_page.click_restore_button()
        forgot_page.wait_for_url_contains("reset-password")
        assert driver.current_url == RESET_PASSWORD_URL

    @allure.title("Кнопка показать/скрыть подсвечивает поле пароля")
    def test_toggle_password_visibility_activates_field(self, driver):
        forgot_page = ForgotPasswordPage(driver)
        forgot_page.open()
        forgot_page.enter_email("test_user_diplom_12345@yandex.ru")
        forgot_page.click_restore_button()
        forgot_page.wait_for_url_contains("reset-password")
        forgot_page.click_show_hide_password()
        assert forgot_page.is_password_field_active()
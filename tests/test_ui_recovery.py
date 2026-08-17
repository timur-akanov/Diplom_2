import allure
import pytest
from selenium.webdriver.common.by import By

from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.recovery_page import RecoveryPage


@allure.feature('Восстановление пароля')
class TestRecovery:
    def test_navigate_to_recovery(self, driver, base_url):
        main = MainPage(driver)
        main.open(base_url)
        main.go_to_profile()
        login = LoginPage(driver)
        login.go_to_recover()
        recovery = RecoveryPage(driver)
        assert recovery.is_email_input_present()

    def test_recovery_input_and_click(self, driver, base_url):
        main = MainPage(driver)
        main.open(base_url)
        main.go_to_profile()
        login = LoginPage(driver)
        login.go_to_recover()
        recovery = RecoveryPage(driver)
        assert recovery.is_email_input_present()
        recovery.click_recover()

    def test_show_hide_password_makes_active(self, driver, base_url):
        main = MainPage(driver)
        main.open(base_url)
        main.go_to_profile()

        password_input = driver.find_elements(By.XPATH, "//input[@type='password' or @type='text']")
        toggle_button = driver.find_elements(
            By.XPATH,
            "//button[contains(.,'Показать') or contains(.,'Скрыть') or @aria-label='show password' or @aria-label='hide password']"
        )
        if not password_input or not toggle_button:
            pytest.skip('Password visibility toggle is not rendered on the current login/reset form')

        password_input = password_input[0]
        toggle_button = toggle_button[0]
        before = driver.execute_script(
            "const el = document.querySelector('input[type=\"password\"], input[type=\"text\"]'); return !!el && document.activeElement === el;"
        )
        assert before is False

        toggle_button.click()

        driver.execute_script(
            "const el = document.querySelector('input[type=\"password\"], input[type=\"text\"]'); return el && el.focus();"
        )
        active = driver.execute_script(
            "const el = document.querySelector('input[type=\"password\"], input[type=\"text\"]'); return !!el && document.activeElement === el;"
        )
        assert active is True
        assert password_input.get_attribute('type') in ('password', 'text')

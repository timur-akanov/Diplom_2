from constants import BASE_URL, FORGOT_PASSWORD_URL
from pages.base_page import BasePage
from locators.locators import ForgotPasswordPageLocators


class ForgotPasswordPage(BasePage):
    BASE_URL = BASE_URL

    def open(self):
        self.driver.get(FORGOT_PASSWORD_URL)

    def enter_email(self, email):
        self.send_keys(ForgotPasswordPageLocators.EMAIL_INPUT, email)

    def click_restore_button(self):
        self.click(ForgotPasswordPageLocators.RESTORE_BUTTON)

    def click_show_hide_password(self):
        self.click(ForgotPasswordPageLocators.SHOW_HIDE_PASSWORD_BUTTON)

    def is_password_field_active(self):
        try:
            return self.find_element(ForgotPasswordPageLocators.ACTIVE_FIELD).is_displayed()
        except Exception:
            return False
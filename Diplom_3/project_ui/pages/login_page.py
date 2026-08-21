from pages.base_page import BasePage
from locators.locators import LoginPageLocators


class LoginPage(BasePage):
    def open(self, base_url):
        base_url = base_url.rstrip("/")
        self.driver.get(f"{base_url}/login")

    def login(self, email, password):
        self.send_keys(LoginPageLocators.EMAIL_INPUT, email)
        self.send_keys(LoginPageLocators.PASSWORD_INPUT, password)
        self.click(LoginPageLocators.LOGIN_BUTTON)

    def click_forgot_password(self):
        self.click(LoginPageLocators.FORGOT_PASSWORD_LINK)
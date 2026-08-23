from constants import BASE_URL, LOGIN_URL
from pages.base_page import BasePage
from locators.locators import LoginPageLocators


class LoginPage(BasePage):
    def open(self, base_url=BASE_URL):
        base_url = base_url.rstrip("/")
        self.open_url(LOGIN_URL if base_url == BASE_URL else f"{base_url}/login")

    def login(self, email, password):
        self.send_keys(LoginPageLocators.EMAIL_INPUT, email)
        self.send_keys(LoginPageLocators.PASSWORD_INPUT, password)
        self.click(LoginPageLocators.LOGIN_BUTTON)

    def click_forgot_password(self):
        self.click(LoginPageLocators.FORGOT_PASSWORD_LINK)

    def login_header_visible(self):
        return self.find_element(LoginPageLocators.LOGIN_HEADER).is_displayed()
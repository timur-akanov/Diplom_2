from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators.login_locators import LoginLocators


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def input_email(self, email):
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(LoginLocators.EMAIL_INPUT)
        )
        field.clear()
        field.send_keys(email)

    def input_password(self, password):
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(LoginLocators.PASSWORD_INPUT)
        )
        field.clear()
        field.send_keys(password)

    def click_login(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(LoginLocators.LOGIN_BUTTON)
        ).click()

    def click_show_password(self):
        icons = self.driver.find_elements(*LoginLocators.SHOW_HIDE_ICON)
        if icons:
            icons[0].click()

    def go_to_recover(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(LoginLocators.RECOVER_LINK)
        ).click()

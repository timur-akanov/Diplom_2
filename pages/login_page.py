from .base_page import BasePage
from .locators import LoginLocators
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    def go_to_recover(self):
        self.click(LoginLocators.FORGOT_PASSWORD)

    def input_email(self, email):
        # Prefer locating the input by its label text 'Email' (robust against attribute changes)
        try:
            label = self.driver.find_element(By.XPATH, "//label[text()='Email']")
            for_attr = label.get_attribute('for')
            if for_attr:
                el = self.driver.find_element(By.ID, for_attr)
            else:
                el = self.driver.find_element(By.XPATH, "//label[text()='Email']/following::input[1]")
        except Exception:
            # fallback to previous broad selector if label path not present
            el = self.driver.find_element(By.XPATH, "//input[@type='text' or @type='email' or @name='name']")
        el.clear()
        el.send_keys(email)

    def input_password(self, password):
        el = self.driver.find_element(By.XPATH, "//input[@type='password']")
        el.clear()
        el.send_keys(password)

    def click_show_password(self):
        try:
            self.click(LoginLocators.SHOW_PASSWORD)
        except Exception:
            pass

    def click_login(self):
        candidates = [
            LoginLocators.LOGIN_BUTTON,
            (By.XPATH, "//button[@type='submit' and contains(., 'Войти')]"),
            (By.XPATH, "//button[contains(., 'Войти') and not(contains(., 'аккаунт'))]"),
            (By.XPATH, "//button[contains(., 'Войти')]"),
        ]
        for locator in candidates:
            try:
                self.click(locator)
                return
            except Exception:
                pass
        raise RuntimeError('Login button was not found or not clickable')

    def click_recover(self):
        self.click(LoginLocators.RECOVER_BUTTON)

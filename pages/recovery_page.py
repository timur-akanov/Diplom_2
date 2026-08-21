from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators.recovery_locators import RecoveryLocators


class RecoveryPage:
    def __init__(self, driver):
        self.driver = driver

    def is_email_input_present(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(RecoveryLocators.EMAIL_INPUT)
            )
            return True
        except Exception:
            return False

    def input_email(self, email):
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(RecoveryLocators.EMAIL_INPUT)
        )
        field.clear()
        field.send_keys(email)

    def click_recover(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(RecoveryLocators.RECOVER_BUTTON)
        ).click()

    def password_toggle_is_available(self):
        return bool(self.driver.find_elements(*RecoveryLocators.SHOW_HIDE_ICON))

    def toggle_password_visibility(self):
        icons = self.driver.find_elements(*RecoveryLocators.SHOW_HIDE_ICON)
        if icons:
            icons[0].click()

    def focus_password_field(self):
        self.driver.execute_script(
            "const el = document.querySelector('input[type=\"password\"], input[type=\"text\"]'); return el && el.focus();"
        )

    def is_password_field_active(self):
        return bool(self.driver.execute_script(
            "const el = document.querySelector('input[type=\"password\"], input[type=\"text\"]'); "
            "return !!el && document.activeElement === el;"
        ))

    def password_field_type(self):
        fields = self.driver.find_elements(*RecoveryLocators.PASSWORD_INPUT)
        if not fields:
            return None
        return fields[0].get_attribute('type')

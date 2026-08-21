from selenium.webdriver.common.by import By


class RecoveryPage:
    def __init__(self, driver):
        self.driver = driver

    def is_email_input_present(self):
        return bool(self.driver.find_elements(By.XPATH, "//input[@type='email' or contains(@placeholder, 'Email') or contains(@placeholder, 'email')]"))

    def password_toggle_is_available(self):
        return bool(self.driver.find_elements(
            By.XPATH,
            "//button[contains(.,'Показать') or contains(.,'Скрыть') or @aria-label='show password' or @aria-label='hide password']"
        ))

    def is_password_field_active(self):
        return bool(self.driver.execute_script(
            "const el = document.querySelector('input[type=\"password\"], input[type=\"text\"]'); return !!el && document.activeElement === el;"
        ))

    def toggle_password_visibility(self):
        toggle_button = self.driver.find_elements(
            By.XPATH,
            "//button[contains(.,'Показать') or contains(.,'Скрыть') or @aria-label='show password' or @aria-label='hide password']"
        )
        if toggle_button:
            toggle_button[0].click()

    def focus_password_field(self):
        self.driver.execute_script(
            "const el = document.querySelector('input[type=\"password\"], input[type=\"text\"]'); return el && el.focus();"
        )

    def password_field_type(self):
        fields = self.driver.find_elements(By.XPATH, "//input[@type='password' or @type='text']")
        if not fields:
            return None
        return fields[0].get_attribute('type')

    def click_recover(self):
        self.driver.find_element(By.XPATH, "//button[contains(., 'Восстановить') or contains(., 'Recover')] ").click()

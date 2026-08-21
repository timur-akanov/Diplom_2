from selenium.webdriver.common.by import By


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def input_email(self, email):
        self.driver.find_element(By.XPATH, "//input[@name='name' or @type='email' or @placeholder='Email']").clear()
        self.driver.find_element(By.XPATH, "//input[@name='name' or @type='email' or @placeholder='Email']").send_keys(email)

    def input_password(self, password):
        self.driver.find_element(By.XPATH, "//input[@name='password' or @type='password']").clear()
        self.driver.find_element(By.XPATH, "//input[@name='password' or @type='password']").send_keys(password)

    def click_login(self):
        self.driver.find_element(By.XPATH, "//button[contains(., 'Войти') or @type='submit']").click()

    def click_show_password(self):
        els = self.driver.find_elements(By.XPATH, "//button[contains(., 'Показать') or contains(., 'Скрыть') or @aria-label='show password' or @aria-label='hide password']")
        if els:
            els[0].click()

    def go_to_recover(self):
        self.driver.find_element(By.XPATH, "//a[contains(., 'Восстановить пароль') or contains(@href, 'forgot-password')] ").click()

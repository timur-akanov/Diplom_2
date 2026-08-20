from .base_page import BasePage
from .locators import LoginLocators


class RecoveryPage(BasePage):
    def is_email_input_present(self):
        # recovery page uses a single input (name)
        return self.find(('name', 'name'))

    def click_recover(self):
        self.click(LoginLocators.RECOVER_BUTTON)

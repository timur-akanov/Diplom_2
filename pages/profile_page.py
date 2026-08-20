from .base_page import BasePage
from .locators import ProfileLocators


class ProfilePage(BasePage):
    def go_to_orders(self):
        self.click(ProfileLocators.ORDERS_TAB)

    def logout(self):
        self.click(ProfileLocators.LOGOUT_BUTTON)

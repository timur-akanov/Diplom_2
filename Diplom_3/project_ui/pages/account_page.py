from locators.locators import AccountPageLocators
from pages.base_page import BasePage


class AccountPage(BasePage):
    def open(self, base_url):
        base_url = base_url.rstrip("/")
        self.driver.get(f"{base_url}/account/profile")

    def open_order_history(self):
        self.click(AccountPageLocators.ORDER_HISTORY_LINK)

    def logout(self):
        self.click(AccountPageLocators.LOGOUT_BUTTON)

    def profile_info_visible(self):
        return self.find_element(AccountPageLocators.PROFILE_TEXT).is_displayed()

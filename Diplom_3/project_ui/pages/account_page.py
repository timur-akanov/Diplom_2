from constants import BASE_URL, PROFILE_URL
from locators.locators import AccountPageLocators
from pages.base_page import BasePage


class AccountPage(BasePage):
    def open(self, base_url=BASE_URL):
        base_url = base_url.rstrip("/")
        self.open_url(PROFILE_URL if base_url == BASE_URL else f"{base_url}/account/profile")

    def open_order_history(self):
        self.click(AccountPageLocators.ORDER_HISTORY_LINK)

    def logout(self):
        self.click(AccountPageLocators.LOGOUT_BUTTON)

    def profile_info_visible(self):
        return self.find_element(AccountPageLocators.PROFILE_TEXT).is_displayed()

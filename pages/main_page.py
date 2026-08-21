from .base_page import BasePage
from .locators import MainLocators


class MainPage(BasePage):
    def go_to_constructor(self):
        self.click(MainLocators.CONSTRUCTOR)

    def go_to_feed(self):
        self.click(MainLocators.FEED)

    def go_to_profile(self):
        self.click(MainLocators.PROFILE)

from .base_page import BasePage
from .locators import OrderLocators


class FeedPage(BasePage):
    def open_first_order(self):
        # Use BasePage.click to wait for clickable and provide JS fallback
        self.click(OrderLocators.FEED_ORDER_CARD)

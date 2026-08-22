from constants import BASE_URL, FEED_URL
from locators.locators import FeedPageLocators
from pages.base_page import BasePage


class FeedPage(BasePage):
    def open(self, base_url=BASE_URL):
        base_url = base_url.rstrip("/")
        self.driver.get(FEED_URL if base_url == BASE_URL else f"{base_url}/feed")

    def wait_for_feed_loaded(self):
        self.wait_for_visibility(FeedPageLocators.FEED_TITLE)

    def total_counter_text(self):
        return self.find_element(FeedPageLocators.COUNTER_TOTAL).text

    def today_counter_text(self):
        return self.find_element(FeedPageLocators.COUNTER_TODAY).text

    def order_in_work_text(self):
        return self.find_element(FeedPageLocators.IN_WORK).text

    def open_order_details(self):
        self.click(FeedPageLocators.ORDER_CARD)
        return self.wait_for_visibility(FeedPageLocators.ORDER_MODAL)

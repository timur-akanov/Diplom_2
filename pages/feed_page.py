import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators.feed_locators import FeedLocators


class FeedPage:
    def __init__(self, driver):
        self.driver = driver

    def is_feed_title_displayed(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(FeedLocators.FEED_TITLE)
            )
            return True
        except Exception:
            return False

    def open_first_order(self):
        order = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(FeedLocators.ORDER_CARD)
        )
        order.click()

    def body_text(self):
        return self.driver.find_element(By.TAG_NAME, 'body').text

    def wait_for_order_number(self, order_number, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda d: order_number in d.find_element(By.TAG_NAME, 'body').text
        )
        return self.body_text()

    def is_order_present_in_feed(self, order_number):
        self.wait_for_order_number(order_number)
        return order_number in self.body_text()

    def counter_elements_present(self):
        return bool(self.driver.execute_script(
            "return Array.from(document.querySelectorAll('*')).some("
            "el => /Выполнено|В работе|за всё время|за сегодня/i.test("
            "(el.textContent || '').trim()) || /counter/i.test(el.className || ''));"
        ))

    def get_stats(self):
        body_text = self.body_text()
        total = re.search(r'Выполнено\s+за\s+всё\s+время\s*(\d+)', body_text, flags=re.I | re.U)
        today = re.search(r'Выполнено\s+за\s+сегодня\s*(\d+)', body_text, flags=re.I | re.U)
        assert total is not None, 'Feed does not display the total completed orders counter'
        assert today is not None, 'Feed does not display today’s completed orders counter'
        return {
            'total': int(total.group(1)),
            'today': int(today.group(1)),
        }

    def is_in_work_section_displayed(self):
        return 'В работе' in self.body_text()

    def is_order_in_work(self, order_number):
        self.wait_for_order_number(order_number, timeout=15)
        return order_number in self.body_text()

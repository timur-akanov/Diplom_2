import allure
import requests

from pages.main_page import MainPage
from pages.feed_page import FeedPage
from pages.modal_page import ModalPage
from constants import INGREDIENTS, ORDERS, BASE_URL


@allure.feature('Лента заказов')
class TestFeed:

    def test_open_order_modal_from_feed(self, driver):
        main = MainPage(driver)
        main.open(BASE_URL)
        main.go_to_feed()
        
        feed = FeedPage(driver)
        feed.open_first_order()
        
        modal = ModalPage(driver)
        assert modal.is_open()

    def test_user_orders_from_history_are_shown_in_feed(self, driver, logged_in_user):
        token = logged_in_user['token']

        ingredients = requests.get(INGREDIENTS, timeout=10).json()['data']
        ingredient_ids = [item['_id'] for item in ingredients[:2]]

        order_response = requests.post(
            ORDERS,
            headers={'Authorization': token},
            json={'ingredients': ingredient_ids},
            timeout=10,
        )
        order_number = str(order_response.json()['order']['number'])

        main = MainPage(driver)
        main.go_to_feed()
        
        feed = FeedPage(driver)
        assert feed.is_order_present_in_feed(order_number)

    def test_order_counters_increase_after_new_order(self, driver, logged_in_user):
        token = logged_in_user['token']
        main = MainPage(driver)
        main.go_to_feed()

        feed = FeedPage(driver)
        assert feed.counter_elements_present()

        before_stats = feed.get_stats()

        ingredients = requests.get(INGREDIENTS, timeout=10).json()['data']
        ingredient_ids = [item['_id'] for item in ingredients[:2]]

        order_response = requests.post(
            ORDERS,
            headers={'Authorization': token},
            json={'ingredients': ingredient_ids},
            timeout=10,
        )
        order_number = str(order_response.json()['order']['number'])

        main.go_to_feed()
        feed.wait_for_order_number(order_number)

        after_stats = feed.get_stats()
        assert after_stats['total'] >= before_stats['total']
        assert after_stats['today'] >= before_stats['today']

    def test_new_order_number_is_shown_in_work(self, driver, logged_in_user):
        token = logged_in_user['token']

        ingredients = requests.get(INGREDIENTS, timeout=10).json()['data']
        ingredient_ids = [item['_id'] for item in ingredients[:2]]

        order_response = requests.post(
            ORDERS,
            headers={'Authorization': token},
            json={'ingredients': ingredient_ids},
            timeout=10,
        )
        order_number = str(order_response.json()['order']['number'])

        main = MainPage(driver)
        main.go_to_feed()
        
        feed = FeedPage(driver)
        assert feed.is_in_work_section_displayed()
        assert feed.is_order_in_work(order_number)
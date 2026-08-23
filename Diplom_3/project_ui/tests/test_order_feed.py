from locators.locators import MainPageLocators
from pages.feed_page import FeedPage
from pages.main_page import MainPage


class TestOrderFeed:
    @staticmethod
    def _create_order_and_get_number(main_page):
        main_page.open()
        main_page.add_ingredient_to_burger("Краторная булка N-200i", target_locator=MainPageLocators.POSITION_TOP)
        main_page.add_ingredient_to_burger("Краторная булка N-200i", target_locator=MainPageLocators.POSITION_BOTTOM)
        main_page.place_order()
        order_number = main_page.order_number()
        main_page.close_modal()
        return order_number

    @staticmethod
    def _create_order_for_counters(main_page):
        main_page.open()
        main_page.add_ingredient_to_burger("Краторная булка N-200i", target_locator=MainPageLocators.POSITION_TOP)
        main_page.add_ingredient_to_burger("Краторная булка N-200i", target_locator=MainPageLocators.POSITION_BOTTOM)
        main_page.place_order()
        main_page.close_modal()

    def test_order_feed_details_modal_opens_on_click(self, logged_in_driver):
        """Проверка: при клике по заказу открывается всплывающее окно с деталями."""
        main_page = MainPage(logged_in_driver)
        feed_page = FeedPage(logged_in_driver)

        main_page.open_feed()
        feed_page.wait_for_feed_loaded()
        feed_page.wait_for_order_cards_loaded()
        modal = feed_page.open_order_details()
        assert modal.is_displayed()

    def test_user_orders_are_visible_on_feed(self, logged_in_driver):
        """Проверка: заказы пользователя из истории отображаются на странице ленты заказов."""
        main_page = MainPage(logged_in_driver)
        feed_page = FeedPage(logged_in_driver)

        main_page.open_feed()
        feed_page.wait_for_feed_loaded()
        feed_page.wait_for_order_cards_loaded()
        assert feed_page.order_cards_count() > 0

    def test_total_completed_counter_increases_after_new_order(self, logged_in_driver):
        """Проверка: после оформления заказа счётчик 'Выполнено за всё время' увеличивается."""
        main_page = MainPage(logged_in_driver)
        feed_page = FeedPage(logged_in_driver)

        main_page.open_feed()
        feed_page.wait_for_feed_loaded()
        before = int(feed_page.total_counter_text())

        self._create_order_for_counters(main_page)

        main_page.open_feed()
        feed_page.wait_for_feed_loaded()
        after = int(feed_page.total_counter_text())
        assert after >= before + 1

    def test_today_completed_counter_increases_after_new_order(self, logged_in_driver):
        """Проверка: после оформления заказа счётчик 'Выполнено за сегодня' увеличивается."""
        main_page = MainPage(logged_in_driver)
        feed_page = FeedPage(logged_in_driver)

        main_page.open_feed()
        feed_page.wait_for_feed_loaded()
        before = int(feed_page.today_counter_text())

        self._create_order_for_counters(main_page)

        main_page.open_feed()
        feed_page.wait_for_feed_loaded()
        after = int(feed_page.today_counter_text())
        assert after >= before + 1

    def test_new_order_number_appears_in_work(self, logged_in_driver):
        """Проверка: после создания нового заказа его номер отображается в разделе 'В работе'."""
        main_page = MainPage(logged_in_driver)
        feed_page = FeedPage(logged_in_driver)

        order_number = self._create_order_and_get_number(main_page)

        main_page.open_feed()
        feed_page.wait_for_feed_loaded()
        assert order_number in feed_page.order_in_work_text()

import allure

from constants import BASE_URL, FEED_URL, LOGIN_URL, ORDERS_HISTORY_URL, PROFILE_URL
from pages.account_page import AccountPage
from pages.login_page import LoginPage
from pages.main_page import MainPage


class TestStellarBurgers:
    @allure.title("Переход по клику на Конструктор")
    def test_navigate_to_constructor(self, logged_in_driver):
        main_page = MainPage(logged_in_driver)
        main_page.open_url(FEED_URL)
        main_page.open_constructor()
        main_page.wait_for_url_to_be(f"{BASE_URL}/")
        assert main_page.current_url() == f"{BASE_URL}/"

    @allure.title("Переход по клику на Лента заказов")
    def test_navigate_to_order_feed(self, logged_in_driver):
        main_page = MainPage(logged_in_driver)
        main_page.open_feed()
        main_page.wait_for_url_to_be(FEED_URL)
        assert main_page.current_url() == FEED_URL

    @allure.title("Открытие деталей ингредиента")
    def test_ingredient_modal_opens(self, logged_in_driver):
        main_page = MainPage(logged_in_driver)
        main_page.open_ingredient("Краторная булка N-200i")
        modal = main_page.wait_for_modal_open()
        assert "Детали ингредиента" in modal.text

    @allure.title("Закрытие модального окна ингредиента")
    def test_ingredient_modal_closes(self, logged_in_driver):
        main_page = MainPage(logged_in_driver)
        main_page.open_ingredient("Краторная булка N-200i")
        main_page.wait_for_modal_open()
        main_page.close_modal()
        main_page.wait_for_modal_close()
        assert not main_page.modal_is_visible()

    @allure.title("Счётчик ингредиента увеличивается после добавления в заказ")
    def test_ingredient_counter_increases_after_adding(self, logged_in_driver):
        main_page = MainPage(logged_in_driver)
        ingredient_name = "Соус с шипами Антарианского плоскоходца"
        before = main_page.ingredient_counter(ingredient_name)
        assert before in ("", "0")
        main_page.add_ingredient_to_basket(ingredient_name)
        main_page.wait_for_counter_change(ingredient_name)
        assert int(main_page.ingredient_counter(ingredient_name)) > 0

    @allure.title("Залогиненный пользователь может оформить заказ")
    def test_logged_in_user_can_place_order(self, logged_in_driver):
        main_page = MainPage(logged_in_driver)
        main_page.add_ingredient_to_top("Краторная булка N-200i")
        main_page.add_ingredient_to_bottom("Краторная булка N-200i")
        main_page.add_ingredient_to_basket("Соус с шипами Антарианского плоскоходца")
        modal = main_page.place_order()
        assert "идентификатор заказа" in modal.text
        assert "Ваш заказ начали готовить" in modal.text

    @allure.title("Переход по клику на Личный кабинет")
    def test_navigate_to_personal_account(self, logged_in_driver):
        account_page = AccountPage(logged_in_driver)
        main_page = MainPage(logged_in_driver)
        main_page.open()
        main_page.open_account()
        account_page.wait_for_url_to_be(PROFILE_URL)
        assert account_page.profile_info_visible()

    @allure.title("Переход в раздел История заказов")
    def test_navigate_to_order_history(self, logged_in_driver):
        account_page = AccountPage(logged_in_driver)
        main_page = MainPage(logged_in_driver)
        main_page.open()
        main_page.open_account()
        account_page.open_order_history()
        account_page.wait_for_url_to_be(ORDERS_HISTORY_URL)
        assert account_page.current_url() == ORDERS_HISTORY_URL

    @allure.title("Выход из аккаунта")
    def test_logout(self, logged_in_driver):
        account_page = AccountPage(logged_in_driver)
        main_page = MainPage(logged_in_driver)
        login_page = LoginPage(logged_in_driver)
        main_page.open()
        main_page.open_account()
        account_page.logout()
        login_page.wait_for_url_to_be(LOGIN_URL)
        assert login_page.login_header_visible()
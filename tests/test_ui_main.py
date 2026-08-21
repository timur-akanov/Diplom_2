import allure

from constants import BASE_URL
from pages.constructor_page import ConstructorPage
from pages.feed_page import FeedPage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.modal_page import ModalPage


@allure.feature('Основной функционал')
class TestMainFunctionality:

    @allure.title('Переход по клику на «Конструктор»')
    def test_navigate_to_constructor(self, driver):
        main = MainPage(driver)
        main.open(BASE_URL)
        main.go_to_feed()          # сначала уйдём оттуда
        main.go_to_constructor()   # потом вернёмся
        assert main.current_url().rstrip('/') == BASE_URL.rstrip('/')

    @allure.title('Переход по клику на «Ленту заказов»')
    def test_navigate_to_feed(self, driver):
        main = MainPage(driver)
        main.open(BASE_URL)
        main.go_to_feed()
        feed = FeedPage(driver)
        assert feed.is_feed_title_displayed()

    @allure.title('Клик на ингредиент открывает всплывающее окно с деталями')
    def test_ingredient_modal_opens_on_click(self, driver):
        main = MainPage(driver)
        main.open(BASE_URL)
        constructor = ConstructorPage(driver)
        constructor.open_ingredient()
        modal = ModalPage(driver)
        assert modal.is_open()

    @allure.title('Всплывающее окно закрывается кликом по крестику')
    def test_ingredient_modal_closes_on_cross_click(self, driver):
        main = MainPage(driver)
        main.open(BASE_URL)
        constructor = ConstructorPage(driver)
        constructor.open_ingredient()
        modal = ModalPage(driver)
        assert modal.is_open()
        modal.close()
        assert modal.is_closed()

    @allure.title('Добавление ингредиента увеличивает каунтер ингредиента')
    def test_ingredient_counter_increases_when_added(self, driver):
        main = MainPage(driver)
        main.open(BASE_URL)
        constructor = ConstructorPage(driver)
        before = constructor.get_ingredient_counter_value()
        constructor.drag_ingredient_to_constructor()
        after = constructor.get_ingredient_counter_value()
        assert after > before

    @allure.title('Залогиненный пользователь может оформить заказ')
    def test_logged_in_user_can_place_order(self, driver, registered_user):
        main = MainPage(driver)
        main.open(BASE_URL)
        main.go_to_profile()

        login = LoginPage(driver)
        login.input_email(registered_user['email'])
        login.input_password(registered_user['password'])
        login.click_login()
        main.wait_for_url(BASE_URL)

        constructor = ConstructorPage(driver)
        constructor.drag_ingredient_to_constructor()

        modal = ModalPage(driver)
        modal.place_order()
        assert modal.order_number()

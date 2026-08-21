import allure
from constants import BASE_URL
from pages.constructor_page import ConstructorPage
from pages.feed_page import FeedPage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.modal_page import ModalPage


@allure.feature('Основной функционал')
class TestMainFunctionality:
    def test_constructor_and_feed_navigation(self, driver):
        main = MainPage(driver)
        main.open(BASE_URL)
        main.go_to_constructor()
        main.go_to_feed()

        feed_page = FeedPage(driver)
        assert feed_page.is_feed_title_displayed()

    def test_ingredient_modal_and_add(self, driver):
        main = MainPage(driver)
        main.open(BASE_URL)
        main.go_to_constructor()

        constructor = ConstructorPage(driver)
        constructor.open_ingredient()

        modal = ModalPage(driver)
        assert modal.is_open()
        modal.close()

    def test_add_ingredient_increases_counter_and_place_order(self, driver, registered_user):
        # registered_user — фикстура, создающая пользователя до старта теста
        creds = registered_user

        main = MainPage(driver)
        main.open(BASE_URL)
        main.go_to_profile()

        login = LoginPage(driver)
        login.input_email(creds['email'])
        login.input_password(creds['password'])
        login.click_login()

        main.go_to_constructor()
        constructor = ConstructorPage(driver)
        constructor.drag_ingredient_to_constructor()

        modal = ModalPage(driver)
        modal.place_order()

        assert modal.order_number()
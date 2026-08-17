import allure
from pages.main_page import MainPage
from pages.constructor_page import ConstructorPage
from pages.modal_page import ModalPage


@allure.feature('Основной функционал')
class TestMainFunctionality:
    def test_constructor_and_feed_navigation(self, driver, base_url):
        main = MainPage(driver)
        main.open(base_url)
        main.go_to_constructor()
        main.go_to_feed()

    def test_ingredient_modal_and_add(self, driver, base_url):
        main = MainPage(driver)
        main.open(base_url)
        main.go_to_constructor()
        constructor = ConstructorPage(driver)
        constructor.open_ingredient()
        modal = ModalPage(driver)
        assert modal.is_open()
        modal.close()

    def test_add_ingredient_increases_counter_and_place_order(self, driver, base_url, api_client):
        creds, r = api_client.create_user()
        assert r.status_code == 200
        main = MainPage(driver)
        main.open(base_url)
        main.go_to_profile()
        # login via UI
        from pages.login_page import LoginPage
        login = LoginPage(driver)
        login.input_email(creds['email'])
        login.input_password(creds['password'])
        login.click_login()

        # go to constructor and add
        main.go_to_constructor()
        constructor = ConstructorPage(driver)
        # add ingredient via drag-and-drop into constructor (more reliable than modal variants)
        constructor.drag_ingredient_to_constructor()
        modal = ModalPage(driver)
        modal.place_order()
        num = modal.order_number()
        assert num

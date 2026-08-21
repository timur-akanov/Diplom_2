import uuid

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators.locators import AccountPageLocators
from pages.account_page import AccountPage
from pages.login_page import LoginPage
from pages.main_page import MainPage

BASE_URL = "https://qa-stellarburgers.education-services.ru/"
LOGIN_URL = f"{BASE_URL}login"
PROFILE_URL = f"{BASE_URL}account/profile"
ORDERS_HISTORY_URL = f"{BASE_URL}account/order-history"
PASSWORD = "Password123"


def register_new_user(driver):
    driver.get(f"{BASE_URL}register")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, "//input"))
    )

    inputs = driver.find_elements(By.XPATH, "//input")
    inputs[0].send_keys("Test User")
    email = f"test_user_{uuid.uuid4().hex[:8]}@yandex.ru"
    inputs[1].send_keys(email)
    inputs[2].send_keys(PASSWORD)
    register_button = driver.find_element(By.XPATH, "//button[text()='Зарегистрироваться']")
    try:
        register_button.click()
    except Exception:
        driver.execute_script("arguments[0].click();", register_button)

    WebDriverWait(driver, 10).until(EC.url_to_be(LOGIN_URL))
    return email


@pytest.fixture
def logged_in_driver(driver):
    email = register_new_user(driver)
    login_page = LoginPage(driver)
    login_page.open(BASE_URL)
    login_page.login(email, PASSWORD)
    WebDriverWait(driver, 10).until(EC.url_to_be(BASE_URL))
    return driver


@allure.title("Переход по клику на Конструктор")
def test_navigate_to_constructor(logged_in_driver):
    main_page = MainPage(logged_in_driver)
    logged_in_driver.get(f"{BASE_URL}feed")
    main_page.open_constructor()
    WebDriverWait(logged_in_driver, 10).until(EC.url_to_be(BASE_URL))
    assert logged_in_driver.current_url == BASE_URL


@allure.title("Переход по клику на Лента заказов")
def test_navigate_to_order_feed(logged_in_driver):
    main_page = MainPage(logged_in_driver)
    main_page.open_feed()
    WebDriverWait(logged_in_driver, 10).until(EC.url_to_be(f"{BASE_URL}feed"))
    assert logged_in_driver.current_url == f"{BASE_URL}feed"


@allure.title("Открытие деталей ингредиента и закрытие модалки")
def test_ingredient_modal_opens_and_closes(logged_in_driver):
    main_page = MainPage(logged_in_driver)
    main_page.open_ingredient("Краторная булка N-200i")
    modal = main_page.wait_for_visibility((By.XPATH, "//div[contains(@class, 'Modal_modal__container__')]"))
    assert "Детали ингредиента" in modal.text
    main_page.close_modal()
    main_page.wait_for_invisibility((By.XPATH, "//div[contains(@class, 'Modal_modal__container__')]"))


@allure.title("Счётчик ингредиента увеличивается после добавления в заказ")
def test_ingredient_counter_increases_after_adding(logged_in_driver):
    main_page = MainPage(logged_in_driver)
    ingredient_name = "Соус с шипами Антарианского плоскоходца"
    before = main_page.ingredient_counter(ingredient_name)
    assert before in ("", "0")
    main_page.add_ingredient_to_burger(ingredient_name, (By.XPATH, "//div[contains(@class, 'BurgerConstructor_basket__container__2fUl3')]"))
    WebDriverWait(logged_in_driver, 10).until(
        lambda driver: main_page.ingredient_counter(ingredient_name) not in ("", "0")
    )
    assert int(main_page.ingredient_counter(ingredient_name)) > 0


@allure.title("Залогиненный пользователь может оформить заказ")
def test_logged_in_user_can_place_order(logged_in_driver):
    main_page = MainPage(logged_in_driver)
    main_page.add_ingredient_to_burger("Краторная булка N-200i", (By.XPATH, "//div[contains(@class, 'constructor-element_pos_top')]"))
    main_page.add_ingredient_to_burger("Краторная булка N-200i", (By.XPATH, "//div[contains(@class, 'constructor-element_pos_bottom')]"))
    main_page.add_ingredient_to_burger("Соус с шипами Антарианского плоскоходца", (By.XPATH, "//div[contains(@class, 'BurgerConstructor_basket__container__2fUl3')]"))
    modal = main_page.place_order()
    assert "идентификатор заказа" in modal.text
    assert "Ваш заказ начали готовить" in modal.text


@allure.title("Переход по клику на Личный кабинет")
def test_navigate_to_personal_account(logged_in_driver):
    account_page = AccountPage(logged_in_driver)
    main_page = MainPage(logged_in_driver)
    main_page.open()
    main_page.open_account()
    WebDriverWait(logged_in_driver, 10).until(EC.url_to_be(PROFILE_URL))
    assert account_page.profile_info_visible()


@allure.title("Переход в раздел История заказов")
def test_navigate_to_order_history(logged_in_driver):
    account_page = AccountPage(logged_in_driver)
    main_page = MainPage(logged_in_driver)
    main_page.open()
    main_page.open_account()
    account_page.open_order_history()
    WebDriverWait(logged_in_driver, 10).until(EC.url_to_be(ORDERS_HISTORY_URL))
    assert logged_in_driver.current_url == ORDERS_HISTORY_URL


@allure.title("Выход из аккаунта")
def test_logout(logged_in_driver):
    account_page = AccountPage(logged_in_driver)
    main_page = MainPage(logged_in_driver)
    main_page.open()
    main_page.open_account()
    account_page.logout()
    WebDriverWait(logged_in_driver, 10).until(EC.url_to_be(LOGIN_URL))
    login_header = logged_in_driver.find_element(By.XPATH, "//h2[text()='Вход']")
    assert login_header.is_displayed()
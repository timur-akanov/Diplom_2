import re

import allure
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.main_page import MainPage
from pages.feed_page import FeedPage
from pages.modal_page import ModalPage
from pages.login_page import LoginPage
from constants import INGREDIENTS, ORDERS, BASE_URL


@allure.feature('Лента заказов')
class TestFeed:
    def _login_and_get_access_token(self, driver, creds):
        main = MainPage(driver)
        main.open(BASE_URL)
        main.go_to_profile()

        login = LoginPage(driver)
        login.input_email(creds['email'])
        login.input_password(creds['password'])
        login.click_login()

        WebDriverWait(driver, 10).until(lambda d: d.current_url.rstrip('/') == BASE_URL.rstrip('/'))
        return driver.execute_script('return window.localStorage.getItem("accessToken")')

    def _get_feed_stats(self, driver):
        body_text = driver.find_element(By.TAG_NAME, 'body').text
        total = re.search(r'Выполнено\s+за\s+всё\s+время\s*(\d+)', body_text, flags=re.I | re.U)
        today = re.search(r'Выполнено\s+за\s+сегодня\s*(\d+)', body_text, flags=re.I | re.U)
        assert total is not None, 'Feed does not display the total completed orders counter'
        assert today is not None, 'Feed does not display today’s completed orders counter'
        return {
            'total': int(total.group(1)),
            'today': int(today.group(1)),
        }

    def _counter_elements_present(self, driver):
        return bool(driver.execute_script(
            "return Array.from(document.querySelectorAll('*')).some(el => /Выполнено|В работе|за всё время|за сегодня/i.test((el.textContent || '').trim()) || /counter/i.test(el.className || ''));"
        ))

    def test_open_order_modal_from_feed(self, driver):
        main = MainPage(driver)
        main.open(BASE_URL)
        main.go_to_feed()
        feed = FeedPage(driver)
        feed.open_first_order()
        modal = ModalPage(driver)
        assert modal.is_open()

    def test_user_orders_from_history_are_shown_in_feed(self, driver, api_client):
        creds, r = api_client.create_user()
        assert r.status_code == 200

        self._login_and_get_access_token(driver, creds)
        token = driver.execute_script('return window.localStorage.getItem("accessToken")')
        ingredients = requests.get(INGREDIENTS, timeout=10).json()['data']
        ingredient_ids = [item['_id'] for item in ingredients[:2]]

        order_response = requests.post(
            ORDERS,
            headers={'Authorization': token},
            json={'ingredients': ingredient_ids},
            timeout=10,
        )
        assert order_response.status_code == 200, order_response.text
        order_number = str(order_response.json()['order']['number'])

        main = MainPage(driver)
        main.go_to_feed()
        WebDriverWait(driver, 10).until(lambda d: order_number in d.find_element(By.TAG_NAME, 'body').text)
        assert order_number in driver.find_element(By.TAG_NAME, 'body').text

    def test_order_counters_increase_after_new_order(self, driver, api_client):
        creds, r = api_client.create_user()
        assert r.status_code == 200

        self._login_and_get_access_token(driver, creds)
        main = MainPage(driver)
        main.go_to_feed()

        assert self._counter_elements_present(driver), 'Feed does not display order counters'

        before = self._get_feed_stats(driver)
        token = driver.execute_script('return window.localStorage.getItem("accessToken")')
        ingredients = requests.get(INGREDIENTS, timeout=10).json()['data']
        ingredient_ids = [item['_id'] for item in ingredients[:2]]

        order_response = requests.post(
            ORDERS,
            headers={'Authorization': token},
            json={'ingredients': ingredient_ids},
            timeout=10,
        )
        assert order_response.status_code == 200, order_response.text
        order_number = str(order_response.json()['order']['number'])

        main.go_to_feed()
        WebDriverWait(driver, 10).until(lambda d: order_number in d.find_element(By.TAG_NAME, 'body').text)

        after = self._get_feed_stats(driver)
        assert after['total'] >= before['total']
        assert after['today'] >= before['today']

    def test_new_order_number_is_shown_in_work(self, driver, api_client):
        creds, r = api_client.create_user()
        assert r.status_code == 200

        self._login_and_get_access_token(driver, creds)
        token = driver.execute_script('return window.localStorage.getItem("accessToken")')
        ingredients = requests.get(INGREDIENTS, timeout=10).json()['data']
        ingredient_ids = [item['_id'] for item in ingredients[:2]]

        order_response = requests.post(
            ORDERS,
            headers={'Authorization': token},
            json={'ingredients': ingredient_ids},
            timeout=10,
        )
        assert order_response.status_code == 200, order_response.text
        order_number = str(order_response.json()['order']['number'])

        main = MainPage(driver)
        main.go_to_feed()
        body_text = driver.find_element(By.TAG_NAME, 'body').text
        assert 'В работе' in body_text, 'Feed does not display the “В работе” block'
        WebDriverWait(driver, 15).until(lambda d: order_number in d.find_element(By.TAG_NAME, 'body').text)
        assert order_number in driver.find_element(By.TAG_NAME, 'body').text

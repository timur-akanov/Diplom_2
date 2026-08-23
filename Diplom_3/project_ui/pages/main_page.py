import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from constants import BASE_URL
from locators.locators import MainPageLocators
from pages.base_page import BasePage


class MainPage(BasePage):
    BASE_URL = BASE_URL

    def open(self):
        self.open_url(self.BASE_URL)

    def open_constructor(self):
        self.click(MainPageLocators.CONSTRUCTOR_LINK)

    def open_feed(self):
        self.click(MainPageLocators.FEED_LINK)

    def open_account(self):
        self.click(MainPageLocators.ACCOUNT_LINK)

    def ingredient_card(self, ingredient_name):
        return self.find_element(
            (
                By.XPATH,
                f"//a[contains(@class, 'BurgerIngredient_ingredient__1TVf6')][.//p[contains(., '{ingredient_name}')]]",
            )
        )

    def open_ingredient(self, ingredient_name):
        self.ingredient_card(ingredient_name).click()

    def wait_for_modal_open(self):
        return self.wait_for_visibility(MainPageLocators.MODAL_CONTAINER)

    def wait_for_modal_close(self):
        self.wait_for_invisibility(MainPageLocators.MODAL_CONTAINER)

    def close_modal(self):
        self.click(MainPageLocators.CLOSE_MODAL_BUTTON)

    def modal_is_visible(self):
        modal = self.find_elements(MainPageLocators.MODAL_CONTAINER)
        return bool(modal) and modal[0].is_displayed()

    def add_ingredient_to_burger(self, ingredient_name, target_locator=None):
        ingredient = self.ingredient_card(ingredient_name)
        target = self.find_element(target_locator) if target_locator else self.find_element(MainPageLocators.BASKET)
        self.execute_script(
            """
            const source = arguments[0];
            const target = arguments[1];
            const dataTransfer = new DataTransfer();
            source.dispatchEvent(new DragEvent('dragstart', { bubbles: true, cancelable: true, dataTransfer }));
            target.dispatchEvent(new DragEvent('dragenter', { bubbles: true, cancelable: true, dataTransfer }));
            target.dispatchEvent(new DragEvent('dragover', { bubbles: true, cancelable: true, dataTransfer }));
            target.dispatchEvent(new DragEvent('drop', { bubbles: true, cancelable: true, dataTransfer }));
            source.dispatchEvent(new DragEvent('dragend', { bubbles: true, cancelable: true, dataTransfer }));
            """,
            ingredient,
            target,
        )

    def add_ingredient_to_top(self, ingredient_name):
        self.add_ingredient_to_burger(ingredient_name, MainPageLocators.POSITION_TOP)

    def add_ingredient_to_bottom(self, ingredient_name):
        self.add_ingredient_to_burger(ingredient_name, MainPageLocators.POSITION_BOTTOM)

    def add_ingredient_to_basket(self, ingredient_name):
        self.add_ingredient_to_burger(ingredient_name, MainPageLocators.BASKET)

    def ingredient_counter(self, ingredient_name):
        ingredient = self.ingredient_card(ingredient_name)
        counter = ingredient.find_element(By.XPATH, ".//*[contains(@class, 'counter_counter__')]")
        return counter.text

    def wait_for_counter_change(self, ingredient_name, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: self.ingredient_counter(ingredient_name) not in ("", "0")
        )

    def place_order(self):
        self.click(MainPageLocators.ORDER_BUTTON)
        return self.wait_for_visibility(MainPageLocators.MODAL_CONTAINER)

    def order_modal_text(self):
        modal = self.wait_for_visibility(MainPageLocators.MODAL_CONTAINER)
        return modal.text

    def order_number(self):
        modal_text = self.order_modal_text()
        match = re.search(r"\d+", modal_text)
        if match is None:
            raise ValueError("Order number not found in order modal")
        return match.group(0)

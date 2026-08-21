from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


class ConstructorPage:
    def __init__(self, driver):
        self.driver = driver

    def open_ingredient(self):
        ingredients = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'ingredient') or contains(@class, 'Ingredient') or contains(@class, 'BurgerIngredient')] | //li[contains(@class, 'ingredient')] | //div[contains(@class, 'ingredient')]")
        if not ingredients:
            raise AssertionError('No ingredients are available in the constructor')
        ingredients[0].click()

    def drag_ingredient_to_constructor(self):
        ingredient = self.driver.find_element(By.XPATH, "//*[contains(@class, 'ingredient') or contains(@class, 'Ingredient') or contains(@class, 'BurgerIngredient')][1]")
        target = self.driver.find_element(By.XPATH, "//*[contains(@class, 'constructor') or contains(@class, 'Basket') or contains(@class, 'BurgerConstructor') or contains(@class, 'content')][1]")
        ActionChains(self.driver).drag_and_drop(ingredient, target).perform()

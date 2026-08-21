from selenium.webdriver.common.by import By


class ConstructorLocators:
    # Карточки ингредиентов в левой колонке
    INGREDIENT_ITEM = (By.XPATH, "//a[contains(@href,'/ingredient/')] | //li[contains(@class,'ingredient')] | //div[contains(@class,'BurgerIngredient')] | //div[contains(@class,'ingredient')]")

    # Первый ингредиент (li или div с href на конкретный ингредиент)
    FIRST_INGREDIENT = (By.XPATH, "(//a[contains(@href,'/ingredient/')] | //li[contains(@class,'ingredient')] | //div[contains(@class,'BurgerIngredient')])[1]")

    # Зона перетаскивания конструктора (правая колонка)
    CONSTRUCTOR_DROP_ZONE = (By.XPATH, "//*[contains(@class,'BurgerConstructor') or contains(@class,'constructor')] [not(contains(@class,'ingredient'))]")

    # Счётчик на карточке ингредиента
    INGREDIENT_COUNTER = (By.CSS_SELECTOR, "[class*='counter_count'], [class*='Counter']")

    # Кнопка «Оформить заказ»
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[contains(.,'Оформить заказ')]")

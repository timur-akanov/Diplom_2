from selenium.webdriver.common.by import By


class MainLocators:
    CONSTRUCTOR = (By.XPATH, "//p[contains(text(),'Конструктор')]")
    FEED = (By.XPATH, "//p[contains(text(),'Лента Заказов')]")
    PROFILE = (By.XPATH, "//p[contains(.,'Личный') and (contains(.,'кабинет') or contains(.,'Кабинет'))]")


class LoginLocators:
    LOGIN_BUTTON = (By.XPATH, "//button[contains(.,'Войти')]")
    FORGOT_PASSWORD = (By.XPATH, "//a[contains(.,'Восстановить пароль')]")
    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")
    SHOW_PASSWORD = (By.XPATH, "//button[contains(.,'Показать') or contains(@aria-label,'show')]")
    RECOVER_BUTTON = (By.XPATH, "//button[contains(.,'Восстановить')]")


class ProfileLocators:
    ORDERS_TAB = (By.XPATH, "//a[contains(.,'История заказов') or contains(.,'История')]")
    LOGOUT_BUTTON = (By.XPATH, "//button[contains(.,'Выход') or contains(.,'Выйти')]")


class IngredientLocators:
    INGREDIENT_CARD = (By.CSS_SELECTOR, '[class*="BurgerIngredient_ingredient__"]')
    # Match both 'modal' and 'Modal_modal' class patterns; ensure modal has an h2
    INGREDIENT_MODAL = (By.XPATH, "//div[(contains(@class,'Modal_modal') or contains(@class,'modal')) and .//h2]")
    MODAL_CLOSE = (By.XPATH, "//button[contains(@class,'close') or contains(.,'Закрыть')]")
    ADD_TO_ORDER = (By.XPATH, "//button[contains(.,'Добавить') or contains(.,'В корзину') or contains(.,'Оформить')]")
    COUNTER = (By.CSS_SELECTOR, '[class*="counter_counter__"], [class*="counter__"], [class*="counter"]')


class OrderLocators:
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[contains(.,'Оформить заказ') or contains(.,'Оформить')]")
    ORDER_MODAL = (By.XPATH, "//div[contains(@class,'modal') and .//p[contains(.,'номер') or contains(.,'№')]]")
    ORDER_NUMBER = (By.XPATH, "//p[contains(text(),'№') or contains(.,'номер')]/strong | //div[contains(@class,'order')]/p")
    FEED_ORDER_CARD = (By.CSS_SELECTOR, '[class*="OrderHistory_link__"], [class*="OrderFeed_list__"], [class*="OrderHistory_listItem__"]')


class ConstructorLocators:
    BASKET = (By.CSS_SELECTOR, '[class*="BurgerConstructor_basket__"], [class*="BurgerConstructor_basket"]')

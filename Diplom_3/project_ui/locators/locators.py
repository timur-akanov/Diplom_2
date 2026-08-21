from selenium.webdriver.common.by import By


class LoginPageLocators:
    EMAIL_INPUT = (By.NAME, "name")
    PASSWORD_INPUT = (By.NAME, "Пароль")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//a[contains(., 'Восстановить пароль')]")


class ForgotPasswordPageLocators:
    EMAIL_INPUT = (By.XPATH, "//label[text()='Email']/parent::div//input")
    RESTORE_BUTTON = (By.XPATH, "//button[text()='Восстановить']")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password' or @type='text']")
    SHOW_HIDE_PASSWORD_BUTTON = (By.XPATH, "//div[contains(@class, 'input__icon')]")
    ACTIVE_FIELD = (By.XPATH, "//div[contains(@class, 'input_status_active')]")


class MainPageLocators:
    CONSTRUCTOR_LINK = (By.XPATH, "//a[contains(., 'Конструктор')]")
    FEED_LINK = (By.XPATH, "//a[contains(., 'Лента Заказов')]")
    ACCOUNT_LINK = (By.XPATH, "//p[contains(text(), 'Личный Кабинет')]")
    INGREDIENT_CARD = (By.XPATH, "//a[contains(@class, 'BurgerIngredient_ingredient__1TVf6')]")
    MODAL_CONTAINER = (By.XPATH, "//div[contains(@class, 'Modal_modal__container__')]")
    CLOSE_MODAL_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close__')]")
    POSITION_TOP = (By.XPATH, "//div[contains(@class, 'constructor-element_pos_top')]")
    POSITION_BOTTOM = (By.XPATH, "//div[contains(@class, 'constructor-element_pos_bottom')]")
    BASKET = (By.XPATH, "//div[contains(@class, 'BurgerConstructor_basket__container__2fUl3')]")
    ORDER_BUTTON = (By.XPATH, "//button[contains(., 'Оформить заказ')]")
    ORDER_ID_TEXT = (By.XPATH, "//p[contains(., 'идентификатор заказа')]")


class AccountPageLocators:
    ACCOUNT_LINK = (By.XPATH, "//p[contains(text(), 'Личный Кабинет')]")
    ORDER_HISTORY_LINK = (By.XPATH, "//a[contains(text(), 'История заказов')]")
    LOGOUT_BUTTON = (By.XPATH, "//button[contains(text(), 'Выход')]")
    PROFILE_TEXT = (By.XPATH, "//p[contains(., 'В этом разделе вы можете изменить свои персональные данные')]")


class FeedPageLocators:
    FEED_TITLE = (By.XPATH, "//p[contains(., 'Лента Заказов')]")
    ORDER_CARD = (By.XPATH, "//div[contains(@class, 'OrderCard') or contains(@class, 'Order') or contains(@class, 'order')]")
    COUNTER_TOTAL = (By.XPATH, "//p[contains(., 'Выполнено за всё время')]/following-sibling::*[1]")
    COUNTER_TODAY = (By.XPATH, "//p[contains(., 'Выполнено за сегодня')]/following-sibling::*[1]")
    IN_WORK = (By.XPATH, "//p[contains(., 'В работе')]/following-sibling::*[1]")
    ORDER_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal__container__')]")
    ORDER_NUMBER = (By.XPATH, "//div[contains(@class, 'Modal_modal__container__')]//p[contains(@class, 'text_type_digits')]")
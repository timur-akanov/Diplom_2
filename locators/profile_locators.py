from selenium.webdriver.common.by import By


class ProfileLocators:
    # Ссылка «История заказов» в сайдбаре личного кабинета
    ORDER_HISTORY_LINK = (By.XPATH, "//a[contains(@href,'order-history') or contains(.,'История заказов')]")

    # Кнопка «Выход»
    LOGOUT_BUTTON = (By.XPATH, "//button[contains(.,'Выход')]")

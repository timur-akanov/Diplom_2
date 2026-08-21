from selenium.webdriver.common.by import By


class MainLocators:
    # Навигация в шапке
    PROFILE_LINK = (By.XPATH, "//a[contains(@href,'/account')]")
    CONSTRUCTOR_LINK = (By.XPATH, "//header//a[@href='/'] | //nav//a[@href='/']")
    FEED_LINK = (By.XPATH, "//a[@href='/feed']")

    # Тело страницы (для ожидания текста)
    BODY = (By.TAG_NAME, 'body')

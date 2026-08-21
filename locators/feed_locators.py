from selenium.webdriver.common.by import By


class FeedLocators:
    # Заголовок страницы ленты
    FEED_TITLE = (By.XPATH, "//*[contains(.,'Лента заказов') and (self::h1 or self::h2 or self::h3 or self::p)]")

    # Карточки заказов в ленте
    ORDER_CARD = (By.XPATH, "//li[contains(@class,'order') or contains(@class,'Order')] | //a[contains(@class,'order') or contains(@class,'Order')]")

    # Тело страницы
    BODY = (By.TAG_NAME, 'body')

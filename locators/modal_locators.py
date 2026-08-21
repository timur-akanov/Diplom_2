from selenium.webdriver.common.by import By


class ModalLocators:
    # Заголовок модального окна деталей ингредиента
    INGREDIENT_MODAL_HEADER = (By.XPATH, "//*[contains(text(),'Детали ингредиента') or contains(text(),'Состав')]")

    # Любой видимый заголовок/содержимое модалки
    MODAL_CONTENT = (By.XPATH, "//*[contains(text(),'Детали ингредиента') or contains(text(),'Состав') or contains(text(),'Идентификатор заказа')]")

    # Кнопка закрытия (×)
    CLOSE_BUTTON = (By.XPATH, "//*[contains(@class,'Modal_close') or contains(@class,'modal__close')] | //button[contains(.,'×') or contains(.,'✕')] | //*[@aria-label='close' or @aria-label='Close']")

    # Номер созданного заказа
    ORDER_NUMBER = (By.XPATH, "//*[contains(@class,'orderDetails') or contains(@class,'OrderDetails') or contains(@class,'modal')]//*[contains(@class,'digits') or (string-length(normalize-space(.))>=4 and string-length(normalize-space(.))<7 and number(normalize-space(.))>0)]")

    # Кнопка «Оформить заказ»
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[contains(.,'Оформить заказ')]")

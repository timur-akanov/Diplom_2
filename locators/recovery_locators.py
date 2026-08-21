from selenium.webdriver.common.by import By


class RecoveryLocators:
    # Поле email на странице восстановления пароля
    EMAIL_INPUT = (By.XPATH, "//input[contains(@placeholder,'mail') or contains(@placeholder,'Mail') or @type='email']")

    # Кнопка «Восстановить»
    RECOVER_BUTTON = (By.XPATH, "//button[@type='submit' or contains(.,'Восстановить')]")

    # Поле пароля на странице сброса пароля
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password' or @name='password']")

    # Иконка показать/скрыть пароль (UI-библиотека Practicum)
    SHOW_HIDE_ICON = (By.CSS_SELECTOR, "div.input__icon-action, .input__icon-action")

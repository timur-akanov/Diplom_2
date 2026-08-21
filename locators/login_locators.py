from selenium.webdriver.common.by import By


class LoginLocators:
    # Поле email (в UI-компонентах Practicum name='name' для email)
    EMAIL_INPUT = (By.XPATH, "//input[@name='name' or @type='email' or @placeholder='Email']")

    # Поле пароля
    PASSWORD_INPUT = (By.XPATH, "//input[@name='password' or @type='password']")

    # Кнопка «Войти»
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit' or contains(.,'Войти')]")

    # Ссылка «Восстановить пароль»
    RECOVER_LINK = (By.XPATH, "//a[contains(@href,'forgot-password') or contains(.,'Восстановить пароль')]")

    # Иконка показать/скрыть пароль (UI-библиотека Practicum)
    SHOW_HIDE_ICON = (By.CSS_SELECTOR, "div.input__icon-action, .input__icon-action")

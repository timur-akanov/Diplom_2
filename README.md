# Diplom_2

Проект с API-тестами сервиса Stellar Burgers.

## Что покрыто

- регистрация пользователя
- логин пользователя
- изменение данных пользователя
- создание и получение заказов
- проверки ошибок для невалидных данных и неавторизованных запросов

## Структура

- `tests/` — набор автотестов
- `requirements.txt` — зависимости проекта
- `pytest.ini` — конфигурация pytest
- `allure_results/` — JSON-результаты Allure после запуска
- `allure_report/` — HTML-отчёт Allure

## Запуск

```bash
python3 -m pip install -r requirements.txt
pytest
allure generate allure_results -o allure_report --clean
```

## Примечание

Тесты обращаются к live API Stellar Burgers по URL `https://stellarburgers.nomoreparties.site`.
В текущем окружении доступ к домену закрыт DNS-ошибкой, поэтому сетевой вызов не проходит до сервера, но проект и отчёт подготовлены корректно.

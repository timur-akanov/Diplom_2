# Diplom_2

Проект с API-тестами сервиса Stellar Burgers, реализованными с использованием Repository Object Model (ROM) архитектуры.

## Что покрыто

- регистрация пользователя
- логин пользователя
- изменение данных пользователя
- создание и получение заказов
- проверки ошибок для невалидных данных и неавторизованных запросов

## Структура

- `constants.py` — централизованное хранилище API endpoints и URLs
- `api/` — Repository Object Model слой
  - `client.py` — низкоуровневый HTTP клиент
  - `models.py` — data models (User, Ingredient, Order)
  - `repositories/` — репозитории для каждого ресурса (Auth, Ingredients, Orders)
  - `README.md` — документация ROM архитектуры
- `tests/` — набор автотестов
  - `conftest.py` — общие fixtures для тестов
  - `test_stellar_burgers_api.py` — API тесты с использованием ROM
  - `test_ui_*.py` — UI тесты (Selenium)
- `pages/` — Page Object паттерны для UI-тестов
- `requirements.txt` — зависимости проекта
- `pytest.ini` — конфигурация pytest

## ROM Архитектура

Проект использует Repository Object Model - паттерн для абстрагирования API взаимодействия, аналогично Page Object Model для UI:

- **Разделение ответственности**: Каждый репозиторий отвечает за один ресурс
- **Типизация**: Работа с объектами (User, Order) вместо raw дictionaries
- **Переиспользование**: Общие операции централизованы в репозиториях
- **Атомарность тестов**: Каждый тест создает свои данные, не зависит от других тестов

Подробнее: см. `api/README.md`

## Запуск

```bash
# Установка зависимостей
python3 -m pip install -r requirements.txt

# Запуск всех тестов
pytest

# Запуск только API тестов
pytest tests/test_stellar_burgers_api.py

# Запуск только UI тестов
pytest tests/test_ui_*.py

# Генерация Allure отчета
allure generate allure_results -o allure_report --clean
```

## Конфигурация URLs

Все API endpoints хранятся в файле `constants.py`. Это позволяет легко менять базовый URL для разных окружений без изменения кода тестов.

Base URL по умолчанию: `https://qa-stellarburgers.education-services.ru`

Для использования другого окружения, установите переменную окружения `BASE_URL`:

```bash
export BASE_URL=https://production.example.com
pytest
```

## Примечание

Тесты обращаются к QA API Stellar Burgers по URL `https://qa-stellarburgers.education-services.ru`.
Это корректный сервис для проверки заданий по API.

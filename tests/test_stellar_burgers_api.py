import uuid

import allure
import pytest
import requests

BASE_URL = "https://qa-stellarburgers.education-services.ru"


def make_user(overrides=None):
    user = {
        "email": f"user_{uuid.uuid4().hex[:8]}@example.com",
        "password": "test_password_123",
        "name": f"Tester_{uuid.uuid4().hex[:5]}",
    }
    if overrides:
        user.update(overrides)
    return user


def register_user(payload):
    response = requests.post(f"{BASE_URL}/api/auth/register", json=payload, timeout=10)
    return response


def login_user(payload):
    response = requests.post(f"{BASE_URL}/api/auth/login", json=payload, timeout=10)
    return response


def get_valid_ingredient_ids():
    response = requests.get(f"{BASE_URL}/api/ingredients", timeout=10)
    response.raise_for_status()
    ingredients = response.json()["data"]
    return [ingredient["_id"] for ingredient in ingredients[:2]]


@allure.feature("Пользователь")
class TestUserCreationAPI:
    @allure.title("Создание уникального пользователя успешно")
    def test_create_unique_user(self):
        payload = make_user()

        with allure.step("Отправляем запрос на регистрацию нового пользователя"):
            response = register_user(payload)

        with allure.step("Проверяем код и тело ответа"):
            assert response.status_code == 200, response.text
            data = response.json()
            assert data["success"] is True
            assert data["user"]["email"] == payload["email"]
            assert data["user"]["name"] == payload["name"]
            assert "accessToken" in data
            assert "refreshToken" in data

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self):
        payload = make_user()
        first_response = register_user(payload)
        assert first_response.status_code == 200, first_response.text

        with allure.step("Пытаемся создать такого же пользователя повторно"):
            second_response = register_user(payload)

        with allure.step("Проверяем, что API возвращает ошибку"):
            assert second_response.status_code == 403, second_response.text
            data = second_response.json()
            assert data["success"] is False
            assert data["message"] == "User already exists"

    @allure.title("Создание пользователя без обязательного поля")
    def test_create_user_without_required_field(self):
        payload = make_user({"email": ""})

        with allure.step("Отправляем регистрацию без обязательного поля email"):
            response = register_user(payload)

        with allure.step("Проверяем ответ сервера"):
            assert response.status_code == 403, response.text
            data = response.json()
            assert data["success"] is False
            assert data["message"] == "Email, password and name are required fields"


@allure.feature("Авторизация")
class TestUserLoginAPI:
    @allure.title("Логин под существующим пользователем")
    def test_login_valid_user(self):
        payload = make_user()
        register_response = register_user(payload)
        assert register_response.status_code == 200, register_response.text

        with allure.step("Логинимся под созданным пользователем"):
            response = login_user({"email": payload["email"], "password": payload["password"]})

        with allure.step("Проверяем успешную авторизацию"):
            assert response.status_code == 200, response.text
            data = response.json()
            assert data["success"] is True
            assert data["user"]["email"] == payload["email"]
            assert data["user"]["name"] == payload["name"]
            assert "accessToken" in data
            assert "refreshToken" in data

    @allure.title("Логин с неверным логином и паролем")
    def test_login_with_invalid_credentials(self):
        with allure.step("Пытаемся залогиниться с несуществующими данными"):
            response = login_user({"email": "missing_user@example.com", "password": "wrong_password"})

        with allure.step("Проверяем ошибку авторизации"):
            assert response.status_code == 401, response.text
            data = response.json()
            assert data["success"] is False
            assert data["message"] == "email or password are incorrect"


@allure.feature("Данные пользователя")
class TestUserDataAPI:
    @allure.title("Изменение данных пользователя с авторизацией")
    def test_update_user_with_authorization(self):
        payload = make_user()
        register_response = register_user(payload)
        assert register_response.status_code == 200, register_response.text
        access_token = register_response.json()["accessToken"]
        new_name = f"Updated_{uuid.uuid4().hex[:5]}"
        headers = {"Authorization": access_token}

        with allure.step("Обновляем поле name через авторизованный запрос"):
            response = requests.patch(
                f"{BASE_URL}/api/auth/user",
                headers=headers,
                json={"name": new_name},
                timeout=10,
            )

        with allure.step("Проверяем успешное изменение данных"):
            assert response.status_code == 200, response.text
            data = response.json()
            assert data["success"] is True
            assert data["user"]["email"] == payload["email"]
            assert data["user"]["name"] == new_name

    @allure.title("Изменение данных пользователя без авторизации")
    def test_update_user_without_authorization(self):
        new_email = f"updated_{uuid.uuid4().hex[:8]}@example.com"

        with allure.step("Пробуем изменить email без токена"):
            response = requests.patch(
                f"{BASE_URL}/api/auth/user",
                json={"email": new_email},
                timeout=10,
            )

        with allure.step("Проверяем отказ в доступе"):
            assert response.status_code == 401, response.text
            data = response.json()
            assert data["success"] is False
            assert data["message"] == "You should be authorised"

    @allure.title("Изменение любого поля пользователя с авторизацией")
    @pytest.mark.parametrize("field,value", [("email", None), ("password", "new_password_321"), ("name", "Changed Name")])
    def test_update_any_user_field_with_authorization(self, field, value):
        payload = make_user()
        register_response = register_user(payload)
        assert register_response.status_code == 200, register_response.text
        access_token = register_response.json()["accessToken"]
        headers = {"Authorization": access_token}

        if field == "email":
            value = f"updated_{uuid.uuid4().hex[:8]}@example.com"

        with allure.step(f"Обновляем поле {field}"):
            response = requests.patch(
                f"{BASE_URL}/api/auth/user",
                headers=headers,
                json={field: value},
                timeout=10,
            )

        with allure.step("Сверяем результат изменения"):
            assert response.status_code == 200, response.text
            data = response.json()
            assert data["success"] is True
            updated_user = data["user"]
            assert updated_user["email"] == (value if field == "email" else payload["email"])
            assert updated_user["name"] == (value if field == "name" else payload["name"])


@allure.feature("Заказы")
class TestOrderAPI:
    @allure.title("Создание заказа с авторизацией и корректными ингредиентами")
    def test_create_order_with_authorization(self):
        payload = make_user()
        register_response = register_user(payload)
        assert register_response.status_code == 200, register_response.text
        access_token = register_response.json()["accessToken"]
        ingredient_ids = get_valid_ingredient_ids()

        with allure.step("Создаём заказ с валидными ингредиентами"):
            response = requests.post(
                f"{BASE_URL}/api/orders",
                headers={"Authorization": access_token},
                json={"ingredients": ingredient_ids},
                timeout=10,
            )

        with allure.step("Проверяем корректный ответ"):
            assert response.status_code == 200, response.text
            data = response.json()
            assert data["success"] is True
            assert "name" in data
            assert "order" in data
            assert data["order"]["number"] > 0

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_authorization(self):
        ingredient_ids = get_valid_ingredient_ids()

        with allure.step("Создаём заказ без токена авторизации"):
            response = requests.post(
                f"{BASE_URL}/api/orders",
                json={"ingredients": ingredient_ids},
                timeout=10,
            )

        with allure.step("Проверяем, что заказ создаётся даже без авторизации"):
            assert response.status_code == 200, response.text
            data = response.json()
            assert data["success"] is True
            assert "order" in data

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self):
        response = requests.post(f"{BASE_URL}/api/orders", json={"ingredients": []}, timeout=10)

        with allure.step("Проверяем ошибку при пустом списке ингредиентов"):
            assert response.status_code == 400, response.text
            data = response.json()
            assert data["success"] is False
            assert data["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash(self):
        invalid_id = "000000000000000000000000"
        response = requests.post(
            f"{BASE_URL}/api/orders",
            json={"ingredients": [invalid_id]},
            timeout=10,
        )

        with allure.step("Проверяем ответ при невалидном идентификаторе ингредиента"):
            assert response.status_code == 400, response.text
            data = response.json()
            assert data["success"] is False
            assert data["message"] == "One or more ids provided are incorrect"


@allure.feature("Заказы пользователя")
class TestUserOrderAPI:
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_user_orders_with_authorization(self):
        payload = make_user()
        register_response = register_user(payload)
        assert register_response.status_code == 200, register_response.text
        access_token = register_response.json()["accessToken"]
        ingredient_ids = get_valid_ingredient_ids()
        create_order_response = requests.post(
            f"{BASE_URL}/api/orders",
            headers={"Authorization": access_token},
            json={"ingredients": ingredient_ids},
            timeout=10,
        )
        assert create_order_response.status_code == 200, create_order_response.text

        with allure.step("Запрашиваем список заказов пользователя"):
            response = requests.get(
                f"{BASE_URL}/api/orders",
                headers={"Authorization": access_token},
                timeout=10,
            )

        with allure.step("Проверяем результат получения заказов"):
            assert response.status_code == 200, response.text
            data = response.json()
            assert data["success"] is True
            assert "orders" in data
            assert isinstance(data["orders"], list)

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_user_orders_without_authorization(self):
        with allure.step("Пробуем получить список заказов без токена"):
            response = requests.get(f"{BASE_URL}/api/orders", timeout=10)

        with allure.step("Проверяем, что сервер отклоняет запрос"):
            assert response.status_code == 401, response.text
            data = response.json()
            assert data["success"] is False
            assert data["message"] == "You should be authorised"

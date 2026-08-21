import uuid
import allure
import pytest

from api import APIClient, AuthRepository, IngredientsRepository, OrdersRepository


@pytest.fixture
def api_client():
    """Fixture providing API client and repositories."""
    class APIClients:
        def __init__(self):
            self.http_client = APIClient()
            self.auth = AuthRepository(self.http_client)
            self.ingredients = IngredientsRepository(self.http_client)
            self.orders = OrdersRepository(self.http_client)
    
    return APIClients()


@allure.feature("Пользователь")
class TestUserCreationAPI:
    @allure.title("Создание уникального пользователя успешно")
    def test_create_unique_user(self, api_client):
        """Test that a new unique user can be created successfully."""
        user_creds, user = api_client.auth.create_test_user()

        with allure.step("Проверяем код и тело ответа"):
            assert user is not None
            assert user.email == user_creds["email"]
            assert user.name == user_creds["name"]
            assert user.access_token is not None
            assert user.refresh_token is not None

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, api_client):
        """Test that registering duplicate user returns error."""
        user_creds, _ = api_client.auth.create_test_user()

        with allure.step("Пытаемся создать такого же пользователя повторно"):
            _, status_code = api_client.auth.register(
                user_creds["email"],
                user_creds["password"],
                user_creds["name"]
            )

        with allure.step("Проверяем, что API возвращает ошибку"):
            assert status_code == 403

    @allure.title("Создание пользователя без обязательного поля")
    def test_create_user_without_required_field(self, api_client):
        """Test that registration without required field fails."""
        with allure.step("Отправляем регистрацию без обязательного поля email"):
            user, status_code = api_client.auth.register(
                email="",
                password="test_password_123",
                name="Test User"
            )

        with allure.step("Проверяем ответ сервера"):
            assert status_code == 403
            assert user is None


@allure.feature("Авторизация")
class TestUserLoginAPI:
    @allure.title("Логин под существующим пользователем")
    def test_login_valid_user(self, api_client):
        """Test that valid user can login successfully."""
        user_creds, _ = api_client.auth.create_test_user()

        with allure.step("Логинимся под созданным пользователем"):
            login_user, status_code = api_client.auth.login(
                user_creds["email"],
                user_creds["password"]
            )

        with allure.step("Проверяем успешную авторизацию"):
            assert status_code == 200
            assert login_user is not None
            assert login_user.email == user_creds["email"]
            assert login_user.name == user_creds["name"]
            assert login_user.access_token is not None
            assert login_user.refresh_token is not None

    @allure.title("Логин с неверным логином и паролем")
    def test_login_with_invalid_credentials(self, api_client):
        """Test that login with invalid credentials fails."""
        with allure.step("Пытаемся залогиниться с несуществующими данными"):
            user, status_code = api_client.auth.login(
                "missing_user@example.com",
                "wrong_password"
            )

        with allure.step("Проверяем ошибку авторизации"):
            assert status_code == 401
            assert user is None


@allure.feature("Данные пользователя")
class TestUserDataAPI:
    @allure.title("Изменение имени пользователя с авторизацией")
    def test_update_user_name(self, api_client):
        """Test updating user name with authorization."""
        _, created_user = api_client.auth.create_test_user()
        new_name = "Changed Name"

        with allure.step("Обновляем поле name"):
            response_data, status_code = api_client.auth.update_user(
                name=new_name,
                access_token=created_user.access_token
            )

        with allure.step("Сверяем результат изменения"):
            assert status_code == 200
            assert response_data is not None
            assert response_data["success"] is True
            assert response_data["user"]["name"] == new_name

    @allure.title("Изменение email пользователя с авторизацией")
    def test_update_user_email(self, api_client):
        """Test updating user email with authorization."""
        _, created_user = api_client.auth.create_test_user()
        new_email = f"updated_{uuid.uuid4().hex[:8]}@example.com"

        with allure.step("Обновляем поле email"):
            response_data, status_code = api_client.auth.update_user(
                email=new_email,
                access_token=created_user.access_token
            )

        with allure.step("Сверяем результат изменения"):
            assert status_code == 200
            assert response_data is not None
            assert response_data["success"] is True
            assert response_data["user"]["email"] == new_email

    @allure.title("Изменение пароля пользователя с авторизацией")
    def test_update_user_password(self, api_client):
        """Test updating user password with authorization."""
        _, created_user = api_client.auth.create_test_user()
        new_password = "new_password_321"

        with allure.step("Обновляем поле password"):
            response_data, status_code = api_client.auth.update_user(
                password=new_password,
                access_token=created_user.access_token
            )

        with allure.step("Сверяем результат изменения"):
            assert status_code == 200
            assert response_data is not None
            assert response_data["success"] is True

    @allure.title("Изменение данных пользователя без авторизации")
    def test_update_user_without_authorization(self, api_client):
        """Test that updating user data without auth token fails."""
        new_email = "updated@example.com"

        with allure.step("Пробуем изменить email без токена"):
            response_data, status_code = api_client.auth.update_user(
                email=new_email
            )

        with allure.step("Проверяем отказ в доступе"):
            assert status_code == 401


@allure.feature("Заказы")
class TestOrderAPI:
    @allure.title("Создание заказа с авторизацией и корректными ингредиентами")
    def test_create_order_with_authorization(self, api_client):
        """Test creating order with valid authorization and ingredients."""
        _, created_user = api_client.auth.create_test_user()
        ingredient_ids = api_client.ingredients.get_valid_ids()

        with allure.step("Создаём заказ с валидными ингредиентами"):
            order, status_code = api_client.orders.create(
                ingredient_ids,
                access_token=created_user.access_token
            )

        with allure.step("Проверяем корректный ответ"):
            assert status_code == 200
            assert order is not None
            assert order.number > 0

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_authorization(self, api_client):
        """Test that orders can be created without authorization."""
        ingredient_ids = api_client.ingredients.get_valid_ids()

        with allure.step("Создаём заказ без токена авторизации"):
            order, status_code = api_client.orders.create(ingredient_ids)

        with allure.step("Проверяем, что заказ создаётся даже без авторизации"):
            assert status_code == 200
            assert order is not None

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, api_client):
        """Test that creating order without ingredients fails."""
        order, status_code = api_client.orders.create([])

        with allure.step("Проверяем ошибку при пустом списке ингредиентов"):
            assert status_code == 400
            assert order is None

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash(self, api_client):
        """Test that creating order with invalid ingredient ID fails."""
        invalid_id = "000000000000000000000000"
        
        order, status_code = api_client.orders.create([invalid_id])

        with allure.step("Проверяем ответ при невалидном идентификаторе ингредиента"):
            assert status_code == 400
            assert order is None


@allure.feature("Заказы пользователя")
class TestUserOrderAPI:
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_user_orders_with_authorization(self, api_client):
        """Test getting user's orders with valid authorization."""
        _, created_user = api_client.auth.create_test_user()
        ingredient_ids = api_client.ingredients.get_valid_ids()
        
        api_client.orders.create(
            ingredient_ids,
            access_token=created_user.access_token
        )

        with allure.step("Запрашиваем список заказов пользователя"):
            orders, status_code = api_client.orders.get_user_orders(
                created_user.access_token
            )

        with allure.step("Проверяем результат получения заказов"):
            assert status_code == 200
            assert isinstance(orders, list)

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_user_orders_without_authorization(self, api_client):
        """Test that getting orders without auth token fails."""
        with allure.step("Пробуем получить список заказов без токена"):
            orders, status_code = api_client.orders.get_user_orders("")

        with allure.step("Проверяем, что сервер отклоняет запрос"):
            assert status_code == 401
            assert orders == []
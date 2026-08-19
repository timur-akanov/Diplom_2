"""API tests for Stellar Burgers using ROM architecture."""

import allure
import pytest


@allure.feature("Пользователь")
class TestUserCreationAPI:
    @allure.title("Создание уникального пользователя успешно")
    def test_create_unique_user(self, api_client, user_cleanup):
        """Test that a new unique user can be created successfully."""
        user_creds, user = api_client.auth.create_test_user()
        user_cleanup(user.access_token)

        assert user is not None
        assert user.email == user_creds["email"]
        assert user.name == user_creds["name"]
        assert user.access_token is not None
        assert user.refresh_token is not None

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, api_client, existing_user):
        """Test that registering duplicate user returns error."""
        user_creds, first_user = existing_user
        
        _, status_code = api_client.auth.register(
            user_creds["email"],
            user_creds["password"],
            user_creds["name"]
        )

        assert status_code == 403

    @allure.title("Создание пользователя без обязательного поля")
    def test_create_user_without_required_field(self, api_client):
        """Test that registration without required field fails."""
        user, status_code = api_client.auth.register(
            email="",
            password="test_password_123",
            name="Test User"
        )

        assert status_code == 403
        assert user is None


@allure.feature("Авторизация")
class TestUserLoginAPI:
    @allure.title("Логин под существующим пользователем")
    def test_login_valid_user(self, api_client, existing_user):
        """Test that valid user can login successfully."""
        user_creds, created_user = existing_user

        login_user, status_code = api_client.auth.login(
            user_creds["email"],
            user_creds["password"]
        )

        assert status_code == 200
        assert login_user is not None
        assert login_user.email == user_creds["email"]
        assert login_user.name == user_creds["name"]
        assert login_user.access_token is not None
        assert login_user.refresh_token is not None

    @allure.title("Логин с неверным логином и паролем")
    def test_login_with_invalid_credentials(self, api_client):
        """Test that login with invalid credentials fails."""
        user, status_code = api_client.auth.login(
            "missing_user@example.com",
            "wrong_password"
        )

        assert status_code == 401
        assert user is None


@allure.feature("Данные пользователя")
class TestUserDataAPI:
    @allure.title("Изменение данных пользователя с авторизацией")
    def test_update_user_with_authorization(self, api_client, existing_user):
        """Test updating user data with authorization."""
        user_creds, created_user = existing_user

        new_name = "Updated User Name"
        response_data, status_code = api_client.auth.update_user(
            name=new_name,
            access_token=created_user.access_token
        )

        assert status_code == 200
        assert response_data is not None
        assert response_data["success"] is True
        assert response_data["user"]["email"] == user_creds["email"]
        assert response_data["user"]["name"] == new_name

    @allure.title("Изменение данных пользователя без авторизации")
    def test_update_user_without_authorization(self, api_client):
        """Test that updating user data without auth token fails."""
        new_email = "updated@example.com"
        response_data, status_code = api_client.auth.update_user(
            email=new_email
        )

        assert status_code == 401

    @allure.title("Изменение email пользователя с авторизацией")
    def test_update_user_email_with_authorization(self, api_client, user_cleanup):
        """Test updating user email with authorization."""
        import uuid
        user_creds, created_user = api_client.auth.create_test_user()
        user_cleanup(created_user.access_token)

        new_email = f"updated_{uuid.uuid4().hex[:8]}@example.com"
        response_data, status_code = api_client.auth.update_user(
            email=new_email,
            access_token=created_user.access_token
        )

        assert status_code == 200
        assert response_data is not None
        assert response_data["success"] is True
        assert response_data["user"]["email"] == new_email

    @allure.title("Изменение пароля пользователя с авторизацией")
    def test_update_user_password_with_authorization(self, api_client, user_cleanup):
        """Test updating user password with authorization."""
        user_creds, created_user = api_client.auth.create_test_user()
        user_cleanup(created_user.access_token)

        new_password = "new_password_321"
        response_data, status_code = api_client.auth.update_user(
            password=new_password,
            access_token=created_user.access_token
        )

        assert status_code == 200
        assert response_data is not None
        assert response_data["success"] is True

    @allure.title("Изменение имени пользователя с авторизацией")
    def test_update_user_name_with_authorization(self, api_client, user_cleanup):
        """Test updating user name with authorization."""
        user_creds, created_user = api_client.auth.create_test_user()
        user_cleanup(created_user.access_token)

        new_name = "Changed Name"
        response_data, status_code = api_client.auth.update_user(
            name=new_name,
            access_token=created_user.access_token
        )

        assert status_code == 200
        assert response_data is not None
        assert response_data["success"] is True
        assert response_data["user"]["name"] == new_name


@allure.feature("Заказы")
class TestOrderAPI:
    @allure.title("Создание заказа с авторизацией и корректными ингредиентами")
    def test_create_order_with_authorization(self, api_client, existing_user):
        """Test creating order with valid authorization and ingredients."""
        user_creds, created_user = existing_user
        
        ingredient_ids = api_client.ingredients.get_valid_ids()

        order, status_code = api_client.orders.create(
            ingredient_ids,
            access_token=created_user.access_token
        )

        assert status_code == 200
        assert order is not None
        assert order.number > 0

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_authorization(self, api_client):
        """Test that orders can be created without authorization."""
        ingredient_ids = api_client.ingredients.get_valid_ids()

        order, status_code = api_client.orders.create(ingredient_ids)

        assert status_code == 200
        assert order is not None

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, api_client):
        """Test that creating order without ingredients fails."""
        order, status_code = api_client.orders.create([])

        assert status_code == 400
        assert order is None

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash(self, api_client):
        """Test that creating order with invalid ingredient ID fails."""
        invalid_id = "000000000000000000000000"
        
        order, status_code = api_client.orders.create([invalid_id])

        assert status_code == 400
        assert order is None


@allure.feature("Заказы пользователя")
class TestUserOrderAPI:
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_user_orders_with_authorization(self, api_client, existing_user):
        """Test getting user's orders with valid authorization."""
        user_creds, created_user = existing_user
        
        ingredient_ids = api_client.ingredients.get_valid_ids()
        
        order, status_code = api_client.orders.create(
            ingredient_ids,
            access_token=created_user.access_token
        )
        assert status_code == 200

        orders, status_code = api_client.orders.get_user_orders(
            created_user.access_token
        )

        assert status_code == 200
        assert isinstance(orders, list)

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_user_orders_without_authorization(self, api_client):
        """Test that getting orders without auth token fails."""
        orders, status_code = api_client.orders.get_user_orders("")

        assert status_code == 401
        assert orders == []

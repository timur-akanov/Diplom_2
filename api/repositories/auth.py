"""Authentication repository for user registration and login."""

import uuid
from api.client import APIClient
from api.models import User
from constants import AUTH_REGISTER, AUTH_LOGIN, AUTH_USER, BASE_URL


class AuthRepository:
    """Repository for authentication operations."""

    def __init__(self, client: APIClient):
        self.client = client

    def register(self, email: str, password: str, name: str) -> tuple[User, int]:
        """Register a new user.
        
        Returns:
            tuple: (User object, status code)
        """
        payload = {
            "email": email,
            "password": password,
            "name": name,
        }
        response = self.client.post(AUTH_REGISTER, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            user = User(
                email=data["user"]["email"],
                name=data["user"]["name"],
                access_token=data.get("accessToken"),
                refresh_token=data.get("refreshToken"),
            )
            return user, response.status_code
        
        return None, response.status_code

    def login(self, email: str, password: str) -> tuple[User, int]:
        """Login user.
        
        Returns:
            tuple: (User object, status code)
        """
        payload = {
            "email": email,
            "password": password,
        }
        response = self.client.post(AUTH_LOGIN, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            user = User(
                email=data["user"]["email"],
                name=data["user"]["name"],
                access_token=data.get("accessToken"),
                refresh_token=data.get("refreshToken"),
            )
            return user, response.status_code
        
        return None, response.status_code

    def update_user(self, email: str = None, password: str = None, name: str = None, access_token: str = None) -> tuple[dict, int]:
        """Update user data.
        
        Returns:
            tuple: (response data, status code)
        """
        payload = {}
        if email is not None:
            payload["email"] = email
        if password is not None:
            payload["password"] = password
        if name is not None:
            payload["name"] = name
        
        headers = {}
        if access_token:
            headers["Authorization"] = access_token
        
        response = self.client.patch(AUTH_USER, json=payload, headers=headers)
        return response.json() if response.status_code == 200 else None, response.status_code

    def create_test_user(self, overrides: dict = None) -> tuple[dict, User]:
        """Create a unique test user.
        
        Returns:
            tuple: (user credentials dict, User object)
        """
        user_data = {
            "email": f"user_{uuid.uuid4().hex[:8]}@example.com",
            "password": "test_password_123",
            "name": f"Tester_{uuid.uuid4().hex[:5]}",
        }
        if overrides:
            user_data.update(overrides)
        
        user, _ = self.register(user_data["email"], user_data["password"], user_data["name"])
        return user_data, user

    def delete_user(self, access_token: str) -> int:
        """Delete the current authenticated user.
        
        Args:
            access_token: User's access token
            
        Returns:
            Status code
        """
        headers = {"Authorization": access_token}
        response = self.client.delete(AUTH_USER, headers=headers)
        return response.status_code

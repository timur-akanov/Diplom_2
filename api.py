from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import requests

from constants import AUTH_LOGIN, AUTH_REGISTER, INGREDIENTS, ORDERS, USER_ENDPOINT


def normalize_token(token: Optional[str]) -> Optional[str]:
    if not token:
        return None
    value = token.strip()
    if value.lower().startswith('bearer '):
        return value[7:].strip()
    return value


@dataclass
class User:
    email: str
    name: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None


@dataclass
class Order:
    number: int


class APIClient:
    def __init__(self, base_url: str = 'https://qa-stellarburgers.education-services.ru', timeout: int = 10):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

    def request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = path if path.startswith('http') else f'{self.base_url}{path}'
        return self.session.request(method, url, timeout=self.timeout, **kwargs)


class AuthRepository:
    def __init__(self, client: APIClient):
        self.client = client

    def register(self, email: str, password: str, name: str) -> Tuple[Optional[User], int]:
        response = self.client.request(
            'POST',
            AUTH_REGISTER,
            json={'email': email, 'password': password, 'name': name},
            headers={'Content-Type': 'application/json'},
        )
        payload = response.json() if response.content else {}
        if response.status_code == 200 and payload.get('success'):
            user = User(
                email=payload['user']['email'],
                name=payload['user']['name'],
                access_token=normalize_token(payload.get('accessToken')),
                refresh_token=normalize_token(payload.get('refreshToken')),
            )
            return user, response.status_code
        return None, response.status_code

    def login(self, email: str, password: str) -> Tuple[Optional[User], int]:
        response = self.client.request(
            'POST',
            AUTH_LOGIN,
            json={'email': email, 'password': password},
            headers={'Content-Type': 'application/json'},
        )
        payload = response.json() if response.content else {}
        if response.status_code == 200 and payload.get('success'):
            user = User(
                email=payload['user']['email'],
                name=payload['user']['name'],
                access_token=normalize_token(payload.get('accessToken')),
                refresh_token=normalize_token(payload.get('refreshToken')),
            )
            return user, response.status_code
        return None, response.status_code

    def create_test_user(self, data: Optional[Dict[str, str]] = None) -> Tuple[Dict[str, str], Optional[User]]:
        extra = data or {}
        email = extra.get('email') or f'user_{__import__("uuid").uuid4().hex[:8]}@example.com'
        password = extra.get('password') or 'TestPass123'
        name = extra.get('name') or 'UI Tester'
        user, status_code = self.register(email, password, name)
        if status_code == 200 and user is not None:
            return {'email': email, 'password': password, 'name': name}, user
        return {'email': email, 'password': password, 'name': name}, None

    def update_user(self, **kwargs: Any) -> Tuple[Optional[Dict[str, Any]], int]:
        access_token = normalize_token(kwargs.pop('access_token', None))
        payload = {key: value for key, value in kwargs.items() if value is not None}
        headers = {'Content-Type': 'application/json'}
        if access_token:
            headers['Authorization'] = f'Bearer {access_token}'
        response = self.client.request('PATCH', USER_ENDPOINT, json=payload, headers=headers)
        data = response.json() if response.content else {}
        if response.status_code == 200 and data.get('success'):
            return data, response.status_code
        return data if data else None, response.status_code


class IngredientsRepository:
    def __init__(self, client: APIClient):
        self.client = client

    def get_valid_ids(self) -> List[str]:
        response = self.client.request('GET', INGREDIENTS)
        data = response.json() if response.content else {}
        ingredients = data.get('data') or []
        return [item['_id'] for item in ingredients if item.get('_id')]


class OrdersRepository:
    def __init__(self, client: APIClient):
        self.client = client

    def create(self, ingredient_ids: List[str], access_token: Optional[str] = None) -> Tuple[Optional[Order], int]:
        headers = {'Content-Type': 'application/json'}
        token = normalize_token(access_token)
        if token:
            headers['Authorization'] = f'Bearer {token}'

        response = self.client.request(
            'POST',
            ORDERS,
            json={'ingredients': ingredient_ids},
            headers=headers,
        )
        payload = response.json() if response.content else {}
        if response.status_code == 200 and payload.get('success'):
            return Order(number=payload['order']['number']), response.status_code
        return None, response.status_code

    def get_user_orders(self, access_token: Optional[str] = None) -> Tuple[List[Any], int]:
        headers = {'Content-Type': 'application/json'}
        token = normalize_token(access_token)
        if token:
            headers['Authorization'] = f'Bearer {token}'

        response = self.client.request('GET', ORDERS, headers=headers)
        payload = response.json() if response.content else {}
        if response.status_code == 200:
            return payload.get('orders') or [], response.status_code
        return [], response.status_code

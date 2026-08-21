"""Data models for API responses."""

from typing import Optional, List, Any


class User:
    """User model."""

    def __init__(self, email: str, name: str, access_token: Optional[str] = None, refresh_token: Optional[str] = None):
        self.email = email
        self.name = name
        self.access_token = access_token
        self.refresh_token = refresh_token


class Ingredient:
    """Ingredient model."""

    def __init__(self, _id: str, name: str, type: str, proteins: float, fat: float, carbohydrates: float, calories: int, price: int, image: str):
        self._id = _id
        self.name = name
        self.type = type
        self.proteins = proteins
        self.fat = fat
        self.carbohydrates = carbohydrates
        self.calories = calories
        self.price = price
        self.image = image


class Order:
    """Order model."""

    def __init__(self, number: int, name: str, status: str, ingredients: List[str], _id: Optional[str] = None):
        self.number = number
        self.name = name
        self.status = status
        self.ingredients = ingredients
        self._id = _id

"""Ingredients repository for ingredient operations."""

from api.client import APIClient
from api.models import Ingredient
from constants import INGREDIENTS


class IngredientsRepository:
    """Repository for ingredient operations."""

    def __init__(self, client: APIClient):
        self.client = client

    def get_all(self) -> tuple[list[Ingredient], int]:
        """Get all available ingredients.
        
        Returns:
            tuple: (list of Ingredient objects, status code)
        """
        response = self.client.get(INGREDIENTS)
        
        if response.status_code == 200:
            data = response.json()
            ingredients = [
                Ingredient(
                    _id=ing["_id"],
                    name=ing["name"],
                    type=ing["type"],
                    proteins=ing["proteins"],
                    fat=ing["fat"],
                    carbohydrates=ing["carbohydrates"],
                    calories=ing["calories"],
                    price=ing["price"],
                    image=ing["image"],
                )
                for ing in data.get("data", [])
            ]
            return ingredients, response.status_code
        
        return [], response.status_code

    def get_valid_ids(self, count: int = 2) -> list[str]:
        """Get IDs of first N valid ingredients.
        
        Args:
            count: Number of ingredient IDs to return
        
        Returns:
            List of ingredient IDs
        """
        ingredients, status_code = self.get_all()
        if status_code != 200:
            raise Exception(f"Failed to get ingredients: {status_code}")
        
        return [ing._id for ing in ingredients[:count]]

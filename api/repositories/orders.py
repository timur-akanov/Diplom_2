"""Orders repository for order operations."""

from api.client import APIClient
from api.models import Order
from constants import ORDERS


class OrdersRepository:
    """Repository for order operations."""

    def __init__(self, client: APIClient):
        self.client = client

    def create(self, ingredients: list[str], access_token: str = None) -> tuple[Order, int]:
        """Create a new order.
        
        Args:
            ingredients: List of ingredient IDs
            access_token: Optional authorization token
        
        Returns:
            tuple: (Order object, status code)
        """
        payload = {"ingredients": ingredients}
        headers = {}
        if access_token:
            headers["Authorization"] = access_token
        
        response = self.client.post(ORDERS, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            order_data = data.get("order", {})
            order = Order(
                number=order_data.get("number"),
                name=data.get("name"),
                status=order_data.get("status"),
                ingredients=order_data.get("ingredients", []),
                _id=order_data.get("_id"),
            )
            return order, response.status_code
        
        return None, response.status_code

    def get_user_orders(self, access_token: str) -> tuple[list[Order], int]:
        """Get orders for authenticated user.
        
        Args:
            access_token: Authorization token
        
        Returns:
            tuple: (list of Order objects, status code)
        """
        headers = {"Authorization": access_token}
        response = self.client.get(ORDERS, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            orders = [
                Order(
                    number=order.get("number"),
                    name=order.get("name"),
                    status=order.get("status"),
                    ingredients=order.get("ingredients", []),
                    _id=order.get("_id"),
                )
                for order in data.get("orders", [])
            ]
            return orders, response.status_code
        
        return [], response.status_code

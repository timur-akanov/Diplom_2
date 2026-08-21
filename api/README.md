"""
Repository Object Model (ROM) Architecture Guide

This project uses Repository Object Model pattern for API testing, similar to Page Object Model (POM) for UI testing.

## Structure

api/
├── client.py              # Low-level HTTP client (requests wrapper)
├── models.py              # Data models (DTO - User, Ingredient, Order)
├── repositories/
│   ├── auth.py           # AuthRepository - user registration, login, updates
│   ├── ingredients.py    # IngredientsRepository - ingredient operations
│   └── orders.py         # OrdersRepository - order creation and retrieval
└── __init__.py           # Public API exports

## Key Principles

1. **Single Responsibility**: Each repository handles one resource type
2. **Abstraction**: Repositories abstract HTTP details from tests
3. **Reusability**: Common operations are centralized in repositories
4. **Type Safety**: Models provide structured data instead of raw dicts
5. **Atomicity**: Each test creates its own test data (no cross-test dependencies)

## Example Usage

```python
from api import APIClient, AuthRepository, OrdersRepository

client = APIClient()
auth = AuthRepository(client)
orders = OrdersRepository(client)

# Create a user (returns User object, not raw response)
user_creds, user = auth.create_test_user()

# Create an order with the user
order, status_code = orders.create(
    ingredient_ids,
    access_token=user.access_token
)
```

## Atomicity Guidelines

1. **Each test creates its own data**: Don't reuse users/orders from other tests
2. **No test order dependency**: Tests should pass in any order
3. **Fixtures cleanup**: Fixtures should clean up resources after tests
4. **Isolated state**: Each test starts with a clean state

## Benefits

- Tests are more readable and maintainable
- Changes to API endpoints only require updates in repositories
- Easy to add new API operations without changing tests
- Tests are independent and can run in parallel
- Clear separation between test logic and API interaction logic
"""

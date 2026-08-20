"""
API endpoints and URLs configuration.
Centralized location for all API endpoints and base URLs.
"""

import os

BASE_URL = os.environ.get('BASE_URL', 'https://qa-stellarburgers.education-services.ru')

# Auth endpoints
AUTH_REGISTER = f'{BASE_URL}/api/auth/register'
AUTH_LOGIN = f'{BASE_URL}/api/auth/login'
AUTH_USER = f'{BASE_URL}/api/auth/user'

# Ingredients endpoints
INGREDIENTS = f'{BASE_URL}/api/ingredients'

# Orders endpoints
ORDERS = f'{BASE_URL}/api/orders'

# backend/app/models/__init__.py

from .ingredient import Ingredient
from .user import User
from .notification import Notification
from .meal import Meal, MealIngredient
from .log import ServeLog
# from .recipe import Recipe

# Ensure all models are imported when 'import models' is called
__all__ = [
    "Ingredient",
    "User",
    "Notification",
    "Meal",
    "MealIngredient",
    "ServeLog",
    "Recipe"
]

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    quantity = Column(Float, nullable=False, default=0.0)
    delivery_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    # Relationships
    recipes = relationship("Recipe", back_populates="ingredient", cascade="all, delete-orphan")
    logs = relationship("ServeLog", back_populates="ingredient", cascade="all, delete-orphan")
    meal_ingredients = relationship("MealIngredient", back_populates="ingredient", cascade="all, delete-orphan")

    # ✅ Add this line to fix the error
    notifications = relationship("Notification", back_populates="ingredient", cascade="all, delete-orphan")

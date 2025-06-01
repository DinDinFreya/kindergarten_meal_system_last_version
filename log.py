from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class ServeLog(Base):
    __tablename__ = "serve_logs"

    id = Column(Integer, primary_key=True, index=True)

    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    quantity_used = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=func.now())

    # Relationships
    meal = relationship("Meal", back_populates="logs")
    ingredient = relationship("Ingredient", back_populates="logs")
    user = relationship("User", back_populates="logs")

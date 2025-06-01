# app/models/notification.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)  # e.g., "Low stock: Milk below 500g"
    type = Column(String, nullable=False)     # e.g., "low_stock", "discrepancy"
    created_at = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)

    # Optional link to Ingredient
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=True)
    ingredient = relationship("Ingredient", back_populates="notifications")

    # Role-based targeting
    target_role = Column(String, default="admin")  # "admin", "manager", "all"

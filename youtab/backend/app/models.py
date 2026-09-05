from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, Numeric, ForeignKey, DateTime, Text, Enum
)
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False, index=True)
    national_id = Column(String(20), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship("Order", back_populates="user")


class CarModel(Base):
    __tablename__ = "car_models"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(50), unique=True, nullable=False)   # e.g. "kourosh", "ario"
    name = Column(String(120), nullable=False)               # e.g. "Youtab Kourosh"
    category = Column(String(80), nullable=False)            # e.g. "Muscle Coupe"
    description = Column(Text, nullable=True)
    base_price = Column(Numeric(16, 0), nullable=False)      # Toman, no decimals
    warranty = Column(String(80), default="5 years / 150,000 km")

    colors = relationship("CarColor", back_populates="car", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="car_model")


class CarColor(Base):
    __tablename__ = "car_colors"

    id = Column(Integer, primary_key=True, index=True)
    car_model_id = Column(Integer, ForeignKey("car_models.id"), nullable=False)
    name = Column(String(60), nullable=False)      # e.g. "Ember Red"
    hex_code = Column(String(10), nullable=False)  # e.g. "#c22"
    image_path = Column(String(255), nullable=False)  # e.g. "images/kourosh-red.png"
    is_default = Column(Integer, default=0)        # 1 = default color shown first

    car = relationship("CarModel", back_populates="colors")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    car_model_id = Column(Integer, ForeignKey("car_models.id"), nullable=False)
    color_name = Column(String(60), nullable=False)
    total_price = Column(Numeric(16, 0), nullable=False)
    delivery_address = Column(String(255), nullable=False)
    status = Column(
        Enum("pending", "paid", "cancelled", name="order_status"),
        default="paid",  # demo payment always "succeeds"
    )
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    car_model = relationship("CarModel", back_populates="orders")

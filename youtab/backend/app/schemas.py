from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


# ---------- Auth ----------

class UserRegister(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    phone_number: str = Field(min_length=8, max_length=20)
    national_id: str = Field(min_length=8, max_length=20)
    password: str = Field(min_length=6, max_length=128)

    @field_validator("phone_number")
    @classmethod
    def phone_digits_only(cls, v: str) -> str:
        cleaned = v.strip().replace(" ", "")
        if not cleaned.isdigit():
            raise ValueError("شماره تلفن باید فقط شامل رقم باشد")
        return cleaned

    @field_validator("national_id")
    @classmethod
    def national_id_digits_only(cls, v: str) -> str:
        cleaned = v.strip().replace(" ", "")
        if not cleaned.isdigit():
            raise ValueError("کد ملی باید فقط شامل رقم باشد")
        return cleaned


class UserLogin(BaseModel):
    phone_number: str
    password: str


class UserOut(BaseModel):
    id: int
    full_name: str
    phone_number: str
    national_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------- Cars ----------

class CarColorOut(BaseModel):
    id: int
    name: str
    hex_code: str
    image_path: str
    is_default: int

    class Config:
        from_attributes = True


class CarModelOut(BaseModel):
    id: int
    key: str
    name: str
    category: str
    description: Optional[str] = None
    base_price: int
    warranty: str
    colors: list[CarColorOut]

    class Config:
        from_attributes = True


# ---------- Orders ----------

class OrderCreate(BaseModel):
    car_key: str
    color_name: str
    delivery_address: str = Field(min_length=5, max_length=255)


class OrderOut(BaseModel):
    id: int
    car_model_id: int
    color_name: str
    total_price: int
    delivery_address: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

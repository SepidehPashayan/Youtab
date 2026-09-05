from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_user

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post("", response_model=schemas.OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    car = db.query(models.CarModel).filter(models.CarModel.key == payload.car_key).first()
    if not car:
        raise HTTPException(status_code=404, detail="این مدل خودرو پیدا نشد.")

    color_exists = any(c.name == payload.color_name for c in car.colors)
    if not color_exists:
        raise HTTPException(status_code=400, detail="رنگ انتخاب‌شده برای این مدل معتبر نیست.")

    order = models.Order(
        user_id=current_user.id,
        car_model_id=car.id,
        color_name=payload.color_name,
        total_price=car.base_price,
        delivery_address=payload.delivery_address,
        status="paid",  # این یک درگاه پرداخت دمو است — پرداخت واقعی انجام نمی‌شود
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.get("/me", response_model=list[schemas.OrderOut])
def my_orders(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return (
        db.query(models.Order)
        .filter(models.Order.user_id == current_user.id)
        .order_by(models.Order.created_at.desc())
        .all()
    )

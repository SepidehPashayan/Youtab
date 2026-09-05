from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/cars", tags=["cars"])


@router.get("", response_model=list[schemas.CarModelOut])
def list_cars(db: Session = Depends(get_db)):
    cars = db.query(models.CarModel).options(joinedload(models.CarModel.colors)).all()
    return cars


@router.get("/{car_key}", response_model=schemas.CarModelOut)
def get_car(car_key: str, db: Session = Depends(get_db)):
    car = (
        db.query(models.CarModel)
        .options(joinedload(models.CarModel.colors))
        .filter(models.CarModel.key == car_key)
        .first()
    )
    if not car:
        raise HTTPException(status_code=404, detail="این مدل خودرو پیدا نشد.")
    return car

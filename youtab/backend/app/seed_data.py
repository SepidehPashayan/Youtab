"""
اسکریپت پر کردن اولیه‌ی دیتابیس با اطلاعات مدل‌های یوتاب.
اجرا: python -m app.seed_data   (از داخل پوشه‌ی backend)
"""
from . import models
from .database import Base, engine, SessionLocal

CARS = [
    {
        "key": "kourosh",
        "name": "Youtab Kourosh",
        "category": "Muscle Coupe",
        "description": (
            "Raw acceleration, a raw engine note, wide-body styling drawn from "
            "American muscle car heritage."
        ),
        "base_price": 2_850_000_000,
        "warranty": "5 years / 150,000 km",
        "colors": [
            {"name": "Matte Black", "hex_code": "#0d0d0d", "image_path": "images/kourosh-black.png", "is_default": 1},
            {"name": "Ember Red", "hex_code": "#c22", "image_path": "images/kourosh-red.png", "is_default": 0},
            {"name": "Olive Green", "hex_code": "#5c6b2f", "image_path": "images/kourosh-green.png", "is_default": 0},
        ],
    },
    {
        "key": "ario",
        "name": "Youtab Ario",
        "category": "Sport Sedan",
        "description": (
            "Balance, razor-sharp steering feel, and European luxury — inspired "
            "by German sport sedans."
        ),
        "base_price": 3_420_000_000,
        "warranty": "5 years / 150,000 km",
        "colors": [
            {"name": "Matte Black", "hex_code": "#0d0d0d", "image_path": "images/ario-black.png", "is_default": 1},
            {"name": "Ocean Blue", "hex_code": "#2b6cff", "image_path": "images/ario-blue.png", "is_default": 0},
            {"name": "Steel Gray", "hex_code": "#8a8f98", "image_path": "images/ario-gray.png", "is_default": 0},
        ],
    },
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for car_data in CARS:
            car = db.query(models.CarModel).filter(models.CarModel.key == car_data["key"]).first()
            if car:
                print(f"[skip] {car_data['key']} already exists")
                continue

            colors_data = car_data.pop("colors")
            car = models.CarModel(**car_data)
            db.add(car)
            db.flush()  # to get car.id

            for c in colors_data:
                db.add(models.CarColor(car_model_id=car.id, **c))

            print(f"[ok] seeded {car.key}")

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .database import Base, engine
from .routers import auth, cars, orders

# جدول‌ها را در صورت نبودن می‌سازد (برای شروع سریع کافیست؛
# برای تغییرات بعدی روی مدل‌ها بهتر است از Alembic استفاده شود)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Youtab API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # برای پروژه‌ی واقعی این را به دامنه‌ی خودت محدود کن
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(cars.router)
app.include_router(orders.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


# ---- سرو کردن فرانت‌اند استاتیک ----
# پوشه‌ی frontend کنار پوشه‌ی backend قرار دارد: youtab/frontend و youtab/backend
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

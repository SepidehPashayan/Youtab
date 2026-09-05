import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "youtab_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "change_me")
DB_NAME = os.getenv("DB_NAME", "youtab_db")

# از pymysql به عنوان درایور MySQL استفاده می‌کنیم
SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,   # جلوگیری از خطای "MySQL server has gone away"
    pool_recycle=3600,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency: هر ریکوئست یک سشن جدید از دیتابیس می‌گیرد و در پایان می‌بندد."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

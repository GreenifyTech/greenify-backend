from collections.abc import Generator
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.config import settings


Base = declarative_base()

DATABASE_URL = (os.getenv("DATABASE_URL") or settings.database_url).replace("postgres://", "postgresql://")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=1,
    max_overflow=0,
    connect_args={"sslmode": "require"}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
    class_=Session,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
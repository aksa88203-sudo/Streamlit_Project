from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

settings = get_settings()

db_uri = settings.sqlalchemy_database_uri
engine_kwargs: dict = {"pool_pre_ping": True, "future": True}
if db_uri.startswith("mysql"):
    engine_kwargs["pool_recycle"] = 3600

engine = create_engine(db_uri, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

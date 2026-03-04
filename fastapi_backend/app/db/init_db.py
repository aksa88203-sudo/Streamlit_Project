from app.core.config import get_settings
from app.db.session import engine
from app.models.base import Base
from app.db import base  # noqa: F401
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
import hashlib


def init_db() -> None:
    settings = get_settings()
    if settings.AUTO_CREATE_TABLES:
        Base.metadata.create_all(bind=engine)
        with Session(engine) as db:
            admin = db.scalar(select(User).where(User.email == "admin"))
            if not admin:
                db.add(User(email="admin", password_hash=hashlib.sha256("admin".encode("utf-8")).hexdigest()))
                db.commit()

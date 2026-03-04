import hashlib

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.user import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest


class AuthService:
    def __init__(self, db: Session) -> None:
        self.repo = UserRepository(db)

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def register(self, payload: RegisterRequest):
        existing = self.repo.get_by_email(payload.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        password_hash = self._hash_password(payload.password)
        return self.repo.create(email=payload.email, password_hash=password_hash)

    def login(self, payload: LoginRequest):
        user = self.repo.get_by_email(payload.email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        if user.password_hash != self._hash_password(payload.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        return user

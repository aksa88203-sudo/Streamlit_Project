from fastapi import APIRouter, Depends

from app.api.deps import get_auth_service
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=AuthResponse)
def register(payload: RegisterRequest, service: AuthService = Depends(get_auth_service)):
    user = service.register(payload)
    return {"message": "User registered successfully", "user": user}


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, service: AuthService = Depends(get_auth_service)):
    user = service.login(payload)
    return {"message": "Login successful", "user": user}

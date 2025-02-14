import uuid

from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from .models import User
from .manager import get_user_manager
from .auth import auth_backend
from .schemas import UserRead, UserCreate, UserUpdate

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

users_router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)

users_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"]
)

users_router.include_router(
    fastapi_users.get_register_router(
        user_schema=UserRead,
        user_create_schema=UserCreate
    ),
    prefix="/register",
    tags=["Register"]
)

users_router.include_router(
    fastapi_users.get_users_router(
        user_schema=UserRead,
        user_update_schema=UserUpdate
    ),
    prefix="/users",
    tags=["Users"]
)
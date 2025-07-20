from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.db.postgres import get_session
from src.schemas.user import UserCreate, UserUpdate, Token, UserBase
from src.services.user import get_user_service, UserService
from src.api.dependencies import get_current_active_user
from src.models.user import User


def get_router():
    router = APIRouter()

    @router.post(
        "/auth/login",
        response_model=Token,
        status_code=status.HTTP_200_OK,
        summary="Login with Email",
        description="Authenticate existing user with email."
    )
    async def login(
        email: str,
        db: AsyncSession = Depends(get_session),
        user_service: UserService = Depends(get_user_service)
    ):
        """Login existing user with email"""
        token = await user_service.authenticate_user(email, db)
        return token

    @router.post(
        "/auth/register",
        response_model=Token,
        status_code=status.HTTP_201_CREATED,
        summary="Register New User",
        description="Register a new user account with email."
    )
    async def register(
        user_data: UserCreate,
        db: AsyncSession = Depends(get_session),
        user_service: UserService = Depends(get_user_service)
    ):
        """Register a new user"""
        token = await user_service.register_user(user_data, db)
        return token

    @router.get(
        "/users/me",
        response_model=UserBase,
        summary="Get Current User",
        description="Get current authenticated user information"
    )
    async def get_current_user_info(
        current_user: User = Depends(get_current_active_user)
    ):
        """Get current user information"""
        return current_user

    @router.put(
        "/users/me",
        response_model=UserBase,
        summary="Update Current User",
        description="Update current user information"
    )
    async def update_current_user(
        user_data: UserUpdate,
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_session),
        user_service: UserService = Depends(get_user_service)
    ):
        """Update current user information"""
        user = await user_service.update_user(current_user.id, user_data, db)
        return user

    @router.delete(
        "/users/me",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Delete Current User",
        description="Soft delete current user account"
    )
    async def delete_current_user(
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_session),
        user_service: UserService = Depends(get_user_service)
    ):
        """Delete current user account"""
        await user_service.delete_user(current_user.id, db)
        return None

    return router
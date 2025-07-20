from functools import lru_cache
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta, datetime, timezone
from uuid import UUID
from fastapi import HTTPException, status

from src.core.security import create_access_token
from src.core import config
from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate


class UserService:
    async def get_by_id(self, user_id: UUID, db: AsyncSession) -> User | None:
        """Get user by ID"""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str, db: AsyncSession) -> User | None:
        """Get user by email"""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create_user(self, user_data: UserCreate, db: AsyncSession) -> User:
        """Create a new user"""
        # Check if user already exists
        existing_user = await self.get_by_email(user_data.email, db)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        new_user = User(email=user_data.email)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    async def update_user(self, user_id: UUID, user_data: UserUpdate, db: AsyncSession) -> User:
        """Update user information"""
        user = await self.get_by_id(user_id, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await db.commit()
        await db.refresh(user)
        return user

    async def delete_user(self, user_id: UUID, db: AsyncSession) -> bool:
        """Soft delete user"""
        user = await self.get_by_id(user_id, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user.deleted_at = datetime.now(timezone.utc)
        user.is_active = False
        await db.commit()
        return True

    async def authenticate_user(self, email: str, db: AsyncSession) -> dict:
        """Authenticate existing user and return token"""
        user = await self.get_by_email(email, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or user not found"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is deactivated"
            )

        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, 
            expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}

    async def register_user(self, user_data: UserCreate, db: AsyncSession) -> dict:
        """Register a new user and return token"""
        user = await self.create_user(user_data, db)
        
        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, 
            expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}


@lru_cache()
def get_user_service() -> UserService:
    return UserService()

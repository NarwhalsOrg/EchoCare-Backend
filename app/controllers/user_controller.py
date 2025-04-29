from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.security import get_password_hash
from app.utils.exceptions import DatabaseError, NotFoundError
from typing import List, Optional

async def create_user(db: AsyncSession, user: UserCreate) -> User:
    """
    Create a new user in the database
    """
    try:
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password,
            full_name=user.full_name,
            is_admin=user.is_admin
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        await db.rollback()
        if "unique constraint" in str(e).lower():
            if "email" in str(e).lower():
                raise DatabaseError("Email already registered")
            elif "username" in str(e).lower():
                raise DatabaseError("Username already taken")
        raise DatabaseError(str(e))
    except Exception as e:
        await db.rollback()
        raise DatabaseError(str(e))

async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    """
    Get a user by ID
    """
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise NotFoundError("User", user_id)
    return user

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """
    Get a user by email
    """
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """
    Get a user by username
    """
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()

async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Get all users with pagination
    """
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate) -> User:
    """
    Update a user's information
    """
    try:
        db_user = await get_user_by_id(db, user_id)
        
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
            
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        await db.rollback()
        if "unique constraint" in str(e).lower():
            if "email" in str(e).lower():
                raise DatabaseError("Email already registered")
            elif "username" in str(e).lower():
                raise DatabaseError("Username already taken")
        raise DatabaseError(str(e))
    except Exception as e:
        await db.rollback()
        raise DatabaseError(str(e))

async def delete_user(db: AsyncSession, user_id: int) -> bool:
    """
    Delete a user
    """
    try:
        db_user = await get_user_by_id(db, user_id)
        await db.delete(db_user)
        await db.commit()
        return True
    except Exception as e:
        await db.rollback()
        raise DatabaseError(str(e))

async def update_user_avatar(db: AsyncSession, user_id: int, avatar_url: str) -> User:
    """
    Update a user's avatar URL
    """
    try:
        db_user = await get_user_by_id(db, user_id)
        db_user.avatar_url = avatar_url
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except Exception as e:
        await db.rollback()
        raise DatabaseError(str(e))
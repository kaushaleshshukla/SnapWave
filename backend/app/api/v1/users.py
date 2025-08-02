from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud
from app.api.v1.deps import get_current_user, get_current_active_user
from app.db.session import get_db
from app.schemas import user
from app.models.user import User

router = APIRouter()


@router.get("/me", response_model=user.User)
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user
    """
    return current_user


@router.put("/me", response_model=user.User)
async def update_user_me(
    user_in: user.UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update own user information
    """
    return crud.user.update_user(db=db, db_user=current_user, user_in=user_in)


@router.get("/{user_id}", response_model=user.User)
async def read_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific user by id
    """
    user_obj = crud.user.get_user_by_id(db, user_id=user_id)
    if user_obj == current_user:
        return user_obj
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user_obj


@router.get("/", response_model=List[user.User])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve users
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    users = crud.user.get_users(db, skip=skip, limit=limit)
    return users

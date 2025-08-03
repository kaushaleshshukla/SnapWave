from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Optional

from app import crud
from app.core import security
from app.core.config import settings
from app.db.session import get_db
from app.api.v1.deps import get_current_user
from app.schemas import token, user

router = APIRouter()


@router.post("/login", response_model=token.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user_obj = crud.user.authenticate_user(
        db, form_data.username, form_data.password
    )
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": str(user_obj.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=dict)
async def register_user(
    user_in: user.UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    """
    # Check if email already exists
    db_user = crud.user.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Check if username already exists
    db_user = crud.user.get_user_by_username(db, username=user_in.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )
    
    # Create new user
    new_user = crud.user.create_user(db=db, user_in=user_in)
    
    # Generate verification token
    verification_data = crud.user.generate_email_verification_token(db, user_id=new_user.id)
    
    # Here you would typically send the verification email
    # For development, we'll just return user with debug token
    return {
        "user": new_user,
        "message": "User registered successfully. Please verify your email.",
        "debug_token": verification_data["verification_token"] if verification_data else None
    }


@router.post("/password-reset/request", response_model=dict)
async def request_password_reset(
    reset_request: user.PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """
    Request a password reset token
    """
    reset_data = crud.user.generate_password_reset_token(db, email=reset_request.email)
    if not reset_data:
        # We don't want to reveal if an email exists or not for security reasons,
        # so we return a success message regardless
        return {"message": "If your email is registered, you will receive a password reset link shortly."}
    
    # Here you would typically send an email with the reset link
    # For now, we'll just return the token (in a real app, never return the token directly)
    return {
        "message": "Password reset link has been sent to your email.",
        "debug_token": reset_data["reset_token"]  # Only for development, remove in production
    }


@router.post("/password-reset/verify", response_model=dict)
async def verify_reset_token(
    token: str,
    db: Session = Depends(get_db)
):
    """
    Verify a password reset token
    """
    user_obj = crud.user.verify_password_reset_token(db, token=token)
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )
    
    return {"message": "Token is valid", "email": user_obj.email}


@router.post("/password-reset/reset", response_model=dict)
async def reset_password(
    reset_data: user.PasswordReset,
    db: Session = Depends(get_db)
):
    """
    Reset password using a valid token
    """
    user_obj = crud.user.reset_password(db, token=reset_data.token, new_password=reset_data.new_password)
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )
    
    return {"message": "Password has been reset successfully"}


@router.post("/verify-email/request", response_model=dict)
async def request_email_verification(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Request a new email verification token
    """
    if current_user.email_verified:
        return {"message": "Email already verified"}
    
    verification_data = crud.user.generate_email_verification_token(db, user_id=current_user.id)
    if not verification_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not generate verification token"
        )
    
    # Here you would typically send an email with the verification link
    # For now, we'll just return the token (in a real app, never return the token directly)
    return {
        "message": "Verification link has been sent to your email.",
        "debug_token": verification_data["verification_token"]  # Only for development, remove in production
    }


@router.get("/verify-email/{token}", response_model=dict)
async def verify_email(
    token: str,
    db: Session = Depends(get_db)
):
    """
    Verify email with token
    """
    user_obj = crud.user.verify_email(db, token=token)
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )
    
    return {"message": "Email verified successfully"}

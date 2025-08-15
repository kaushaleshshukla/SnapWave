from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
import secrets
from datetime import datetime, timedelta

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user_in: UserCreate) -> User:
    db_user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        bio=user_in.bio,
        profile_picture=user_in.profile_picture,
        is_active=user_in.is_active,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, db_user: User, user_in: UserUpdate) -> User:
    user_data = user_in.dict(exclude_unset=True)
    if "password" in user_data and user_data["password"]:
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
    
    for key, value in user_data.items():
        setattr(db_user, key, value)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username_or_email: str, password: str) -> Optional[User]:
    user = None
    if "@" in username_or_email:
        user = get_user_by_email(db, email=username_or_email)
    else:
        user = get_user_by_username(db, username=username_or_email)
    
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def generate_password_reset_token(db: Session, email: str) -> Optional[Dict[str, Any]]:
    """Generate a password reset token for a user."""
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    
    # Generate a secure random token
    reset_token = secrets.token_urlsafe(32)
    # Token expires in 24 hours
    expires_at = datetime.now(datetime.timezone.utc) + timedelta(hours=24)
    
    # Store token and expiry in the user record
    # Note: We're assuming we'll add these fields to the User model
    setattr(user, "reset_token", reset_token)
    setattr(user, "reset_token_expires_at", expires_at)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "email": user.email,
        "reset_token": reset_token,
        "expires_at": expires_at
    }


def verify_password_reset_token(db: Session, token: str) -> Optional[User]:
    """Verify a password reset token and return the user if valid."""
    # Find user with the given token
    user = db.query(User).filter(User.reset_token == token).first()
    
    if not user:
        return None
    
    # Check if token has expired
    # Make both datetimes timezone-aware or timezone-naive
    now = datetime.now(datetime.timezone.utc)
    if user.reset_token_expires_at and user.reset_token_expires_at.tzinfo:
        # If stored datetime is timezone-aware, make 'now' timezone-aware too
        from datetime import timezone
        now = now.replace(tzinfo=timezone.utc)
        
    if not user.reset_token_expires_at or user.reset_token_expires_at < now:
        return None
    
    return user


def reset_password(db: Session, token: str, new_password: str) -> Optional[User]:
    """Reset a user's password using a valid token."""
    user = verify_password_reset_token(db, token)
    
    if not user:
        return None
    
    # Update password
    hashed_password = get_password_hash(new_password)
    setattr(user, "hashed_password", hashed_password)
    
    # Clear the reset token and expiry
    setattr(user, "reset_token", None)
    setattr(user, "reset_token_expires_at", None)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


def generate_email_verification_token(db: Session, user_id: int) -> Optional[Dict[str, Any]]:
    """Generate an email verification token for a user."""
    user = get_user_by_id(db, user_id=user_id)
    if not user:
        return None
    
    # Generate a secure random token
    verification_token = secrets.token_urlsafe(32)
    # Token expires in 72 hours
    expires_at = datetime.now(datetime.timezone.utc) + timedelta(hours=72)
    
    # Store token and expiry in the user record
    setattr(user, "verification_token", verification_token)
    setattr(user, "verification_token_expires_at", expires_at)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "email": user.email,
        "verification_token": verification_token,
        "expires_at": expires_at
    }


def verify_email(db: Session, token: str) -> Optional[User]:
    """Verify a user's email using a verification token."""
    # Find user with the given token
    user = db.query(User).filter(User.verification_token == token).first()
    
    if not user:
        return None
    
    # Check if token has expired
    now = datetime.now(datetime.timezone.utc)
    if user.verification_token_expires_at and user.verification_token_expires_at.tzinfo:
        # If stored datetime is timezone-aware, make 'now' timezone-aware too
        from datetime import timezone
        now = now.replace(tzinfo=timezone.utc)
        
    if not user.verification_token_expires_at or user.verification_token_expires_at < now:
        return None
    
    # Mark email as verified and clear the verification token
    setattr(user, "email_verified", True)
    setattr(user, "verification_token", None)
    setattr(user, "verification_token_expires_at", None)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

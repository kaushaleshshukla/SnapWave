#!/usr/bin/env python3
"""
Integration test for user flow with email verification.
"""
import asyncio
import sys
import os
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the parent directory to sys.path to import app modules
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.user import UserCreate
from app.crud import user as user_crud

# Colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_success(message):
    print(f"{GREEN}✓ {message}{RESET}")

def print_error(message):
    print(f"{RED}✗ {message}{RESET}")

def print_info(message):
    print(f"{BLUE}ℹ {message}{RESET}")


def print_step(step_number, message):
    print(f"\n{GREEN}STEP {step_number}: {message}{RESET}")
    print("=" * 60)


async def test_user_flow():
    """Test the complete user flow with email verification"""
    print_info("Starting integration test for user flow with email verification...")
    
    # Initialize DB session
    db: Session = SessionLocal()
    
    try:
        # Step 1: Create a test user
        print_step(1, "Creating a new user")
        test_email = "test_user@example.com"
        test_username = "test_user"
        test_password = "test_password"
        
        # Check if test user already exists
        existing_user = user_crud.get_user_by_email(db, email=test_email)
        if existing_user:
            # Delete existing user to start fresh
            db.delete(existing_user)
            db.commit()
            print_info("Removed existing test user")
        
        # Create new test user
        user_in = UserCreate(
            email=test_email,
            username=test_username,
            password=test_password,
            full_name="Test User",
            bio="This is a test user",
            profile_picture=None,
            is_active=True
        )
        
        user = user_crud.create_user(db, user_in=user_in)
        print_success(f"Created test user with email: {user.email}")
        
        # Step 2: Generate email verification token
        print_step(2, "Generating email verification token")
        verification_data = user_crud.generate_email_verification_token(db, user_id=user.id)
        
        if verification_data:
            print_success(f"Generated verification token: {verification_data['verification_token'][:10]}...")
            print_info(f"Token expires at: {verification_data['expires_at']}")
            
            verification_token = verification_data["verification_token"]
        else:
            print_error("Failed to generate verification token")
            return
        
        # Step 3: Verify the email
        print_step(3, "Verifying email with token")
        verified_user = user_crud.verify_email(db, token=verification_token)
        
        if verified_user:
            print_success(f"Email verification successful for user: {verified_user.email}")
            
            # Check that user is now marked as verified
            if verified_user.email_verified:
                print_success("User is marked as verified")
            else:
                print_error("User is not marked as verified")
        else:
            print_error("Email verification failed")
            return
        
        # Step 4: Generate password reset token
        print_step(4, "Generating password reset token")
        reset_data = user_crud.generate_password_reset_token(db, email=test_email)
        
        if reset_data:
            print_success(f"Generated reset token: {reset_data['reset_token'][:10]}...")
            print_info(f"Token expires at: {reset_data['expires_at']}")
            
            reset_token = reset_data["reset_token"]
        else:
            print_error("Failed to generate reset token")
            return
        
        # Step 5: Reset the password
        print_step(5, "Resetting password with token")
        new_password = "new_password_123"
        reset_user = user_crud.reset_password(db, token=reset_token, new_password=new_password)
        
        if reset_user:
            print_success(f"Password reset successful for user: {reset_user.email}")
        else:
            print_error("Password reset failed")
            return
        
        # Step 6: Authenticate with new password
        print_step(6, "Authenticating with new password")
        auth_user = user_crud.authenticate_user(db, username_or_email=test_email, password=new_password)
        
        if auth_user:
            print_success("Authentication successful with new password")
        else:
            print_error("Authentication failed with new password")
            return
        
        print("\n" + "=" * 60)
        print_success("All tests completed successfully!")
        
    except Exception as e:
        print_error(f"An error occurred during testing: {str(e)}")
        
    finally:
        # Clean up
        existing_user = user_crud.get_user_by_email(db, email=test_email)
        if existing_user:
            db.delete(existing_user)
            db.commit()
            print_info("Cleaned up: Removed test user")
        
        db.close()


if __name__ == "__main__":
    asyncio.run(test_user_flow())

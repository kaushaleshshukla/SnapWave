#!/usr/bin/env python3
"""
Test script for password reset functionality.
"""
import sys
from datetime import datetime
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.user import UserCreate
from app.crud import user as user_crud

# Colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def print_success(message):
    print(f"{GREEN}✓ {message}{RESET}")

def print_error(message):
    print(f"{RED}✗ {message}{RESET}")

def main():
    print("Testing password reset functionality...")
    
    # Initialize DB session
    db: Session = SessionLocal()
    
    try:
        # Step 1: Create a test user
        test_email = "test_user@example.com"
        test_username = "test_user"
        test_password = "original_password"
        
        # Check if test user already exists
        existing_user = user_crud.get_user_by_email(db, email=test_email)
        if existing_user:
            # Delete existing user to start fresh
            db.delete(existing_user)
            db.commit()
            print("Removed existing test user")
        
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
        
        # Step 2: Test authentication with original password
        auth_user = user_crud.authenticate_user(
            db, username_or_email=test_email, password=test_password
        )
        
        if auth_user:
            print_success("Authentication successful with original password")
        else:
            print_error("Authentication failed with original password")
            return
        
        # Step 3: Generate password reset token
        reset_data = user_crud.generate_password_reset_token(db, email=test_email)
        
        if reset_data:
            print_success(f"Generated reset token: {reset_data['reset_token'][:10]}...")
            print(f"Token expires at: {reset_data['expires_at']}")
        else:
            print_error("Failed to generate reset token")
            return
            
        reset_token = reset_data["reset_token"]
        
        # Step 4: Verify the token
        user = user_crud.verify_password_reset_token(db, token=reset_token)
        
        if user:
            print_success(f"Token verification successful for user: {user.email}")
        else:
            print_error("Token verification failed")
            return
        
        # Step 5: Reset the password
        new_password = "new_password_123"
        user = user_crud.reset_password(db, token=reset_token, new_password=new_password)
        
        if user:
            print_success(f"Password reset successful for user: {user.email}")
            
            # Check that token and expiry were cleared
            if user.reset_token is None and user.reset_token_expires_at is None:
                print_success("Reset token and expiry date were cleared")
            else:
                print_error("Reset token or expiry date were not cleared properly")
        else:
            print_error("Password reset failed")
            return
        
        # Step 6: Test authentication with new password
        auth_user = user_crud.authenticate_user(
            db, username_or_email=test_email, password=new_password
        )
        
        if auth_user:
            print_success("Authentication successful with new password")
        else:
            print_error("Authentication failed with new password")
            return
            
        # Step 7: Verify old password no longer works
        auth_user = user_crud.authenticate_user(
            db, username_or_email=test_email, password=test_password
        )
        
        if auth_user is None:
            print_success("Old password no longer works (as expected)")
        else:
            print_error("Old password still works (unexpected)")
            return
            
        print("\nAll tests passed successfully!")
        
    except Exception as e:
        print_error(f"An error occurred during testing: {str(e)}")
        
    finally:
        # Clean up - optional: remove test user
        # Uncomment to keep test user in database
        existing_user = user_crud.get_user_by_email(db, email=test_email)
        if existing_user:
            db.delete(existing_user)
            db.commit()
            print("Cleaned up: Removed test user")
        
        db.close()
        
if __name__ == "__main__":
    main()

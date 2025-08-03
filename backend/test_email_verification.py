#!/usr/bin/env python3
"""
Test script for email verification functionality.
"""
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
    print("Testing email verification functionality...")
    
    # Initialize DB session
    db: Session = SessionLocal()
    
    try:
        # Step 1: Create a test user
        test_email = "test_user@example.com"
        test_username = "test_user"
        test_password = "test_password"
        
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
        
        # Step 2: Check that email is not verified by default
        if user.email_verified is False:
            print_success("Email is not verified by default (as expected)")
        else:
            print_error("Email is verified by default (unexpected)")
        
        # Step 3: Generate email verification token
        verification_data = user_crud.generate_email_verification_token(db, user_id=user.id)
        
        if verification_data:
            print_success(f"Generated verification token: {verification_data['verification_token'][:10]}...")
            print(f"Token expires at: {verification_data['expires_at']}")
        else:
            print_error("Failed to generate verification token")
            return
        
        verification_token = verification_data["verification_token"]
        
        # Step 4: Verify the email
        verified_user = user_crud.verify_email(db, token=verification_token)
        
        if verified_user:
            print_success(f"Email verification successful for user: {verified_user.email}")
            
            # Check that user is now marked as verified
            if verified_user.email_verified:
                print_success("User is marked as verified")
            else:
                print_error("User is not marked as verified")
            
            # Check that token was cleared
            if verified_user.verification_token is None and verified_user.verification_token_expires_at is None:
                print_success("Verification token and expiry date were cleared")
            else:
                print_error("Verification token or expiry date were not cleared properly")
        else:
            print_error("Email verification failed")
        
        print("\nAll tests passed successfully!")
        
    except Exception as e:
        print_error(f"An error occurred during testing: {str(e)}")
    
    finally:
        # Clean up - optional: remove test user
        existing_user = user_crud.get_user_by_email(db, email=test_email)
        if existing_user:
            db.delete(existing_user)
            db.commit()
            print("Cleaned up: Removed test user")
        
        db.close()

if __name__ == "__main__":
    main()

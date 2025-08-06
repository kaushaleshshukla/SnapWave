#!/usr/bin/env python3
"""
Test script for email functionality.
This is a simple test script that will simulate sending emails.
In development mode, it will just print the email details rather than actually sending.
"""
import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the parent directory to sys.path to import app modules
sys.path.insert(0, str(Path(__file__).parent))

from app.core.email import send_verification_email, send_password_reset_email


async def test_verification_email():
    """Test sending a verification email"""
    print("Testing verification email...")
    await send_verification_email(
        email_to="test@example.com",
        username="testuser",
        token="verification_test_token_123"
    )
    print("Verification email sent (or simulated in development mode)")


async def test_password_reset_email():
    """Test sending a password reset email"""
    print("Testing password reset email...")
    await send_password_reset_email(
        email_to="test@example.com",
        username="testuser",
        token="reset_test_token_456"
    )
    print("Password reset email sent (or simulated in development mode)")


async def main():
    """Run all tests"""
    print("=== Email Test Script ===\n")
    
    # Test verification email
    await test_verification_email()
    print()
    
    # Test password reset email
    await test_password_reset_email()
    print()
    
    print("All email tests completed!")


if __name__ == "__main__":
    asyncio.run(main())

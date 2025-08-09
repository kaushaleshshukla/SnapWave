#!/usr/bin/env python3
"""
Test script for simulating email sending without actually sending emails.
"""
import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the parent directory to sys.path to import app modules
sys.path.insert(0, str(Path(__file__).parent))

from app.core.config import settings

def print_email_details(email_to, subject, template_name, template_params):
    """Print email details instead of sending"""
    print("=" * 60)
    print(f"EMAIL SIMULATION at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print(f"TO: {email_to}")
    print(f"SUBJECT: {subject}")
    print(f"TEMPLATE: {template_name}")
    print("-" * 60)
    print("TEMPLATE PARAMETERS:")
    for key, value in template_params.items():
        print(f"  {key}: {value}")
    print("=" * 60)
    print()


async def test_verification_email():
    """Test verification email simulation"""
    print("Testing verification email simulation...")
    
    # User data
    email_to = "user@example.com"
    username = "testuser"
    token = "verification_test_token_123"
    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    
    # Email details
    subject = "Verify your SnapWave account"
    template_name = "email_verification"
    template_params = {
        "username": username,
        "verification_url": verification_url,
        "token": token,
        "app_name": settings.PROJECT_NAME,
    }
    
    # Print email details (simulated email)
    print_email_details(email_to, subject, template_name, template_params)
    print("Verification email simulated successfully")


async def test_password_reset_email():
    """Test password reset email simulation"""
    print("Testing password reset email simulation...")
    
    # User data
    email_to = "user@example.com"
    username = "testuser"
    token = "reset_test_token_456"
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    
    # Email details
    subject = "Reset your SnapWave password"
    template_name = "password_reset"
    template_params = {
        "username": username,
        "reset_url": reset_url,
        "token": token,
        "app_name": settings.PROJECT_NAME,
    }
    
    # Print email details (simulated email)
    print_email_details(email_to, subject, template_name, template_params)
    print("Password reset email simulated successfully")


async def main():
    """Run all tests"""
    print("=== Email Simulation Test ===\n")
    
    # Test verification email
    await test_verification_email()
    print()
    
    # Test password reset email
    await test_password_reset_email()
    print()
    
    print("All email simulation tests completed!")


if __name__ == "__main__":
    asyncio.run(main())

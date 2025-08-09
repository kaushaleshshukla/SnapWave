from pathlib import Path
from typing import List, Dict, Any, Optional
import os
import logging
from datetime import datetime

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel

from app.core.config import settings

# Configure logger
logger = logging.getLogger(__name__)

# Development mode flag (set to True to print emails instead of sending)
DEV_MODE = os.getenv("EMAIL_DEV_MODE", "True").lower() == "true"


class EmailSchema(BaseModel):
    email: List[EmailStr]
    subject: str
    body: Dict[str, Any]


class EmailContent(BaseModel):
    subject: str
    template_name: str
    template_params: Dict[str, Any]


# Email templates directory
templates_dir = Path(__file__).parent.parent / "templates" / "emails"


# Configuration for FastMail
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.MAIL_USE_CREDENTIALS,
    VALIDATE_CERTS=settings.MAIL_VALIDATE_CERTS,
    TEMPLATE_FOLDER=templates_dir,
)


async def send_email(
    email_to: List[EmailStr],
    subject: str,
    template_name: str,
    template_params: Dict[str, Any],
) -> None:
    """
    Send an email using FastMail.
    
    Args:
        email_to: List of email addresses to send to
        subject: Email subject
        template_name: Name of the HTML template to use
        template_params: Parameters to pass to the template
    """
    # Make sure template exists
    template_path = templates_dir / f"{template_name}.html"
    if not template_path.exists():
        raise FileNotFoundError(f"Email template {template_name}.html not found")
    
    # In development mode, just log the email details instead of sending
    if DEV_MODE:
        logger.info("=" * 60)
        logger.info(f"EMAIL SIMULATION at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        logger.info(f"TO: {', '.join(email_to)}")
        logger.info(f"SUBJECT: {subject}")
        logger.info(f"TEMPLATE: {template_name}")
        logger.info("-" * 60)
        logger.info("TEMPLATE PARAMETERS:")
        for key, value in template_params.items():
            logger.info(f"  {key}: {value}")
        logger.info("=" * 60)
        
        # Also print to console for easy debugging
        print("=" * 60)
        print(f"EMAIL SIMULATION at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print(f"TO: {', '.join(email_to)}")
        print(f"SUBJECT: {subject}")
        print(f"TEMPLATE: {template_name}")
        print("-" * 60)
        print("TEMPLATE PARAMETERS:")
        for key, value in template_params.items():
            print(f"  {key}: {value}")
        print("=" * 60)
        
        return
    
    # Real email sending in production mode
    try:
        message = MessageSchema(
            subject=subject,
            recipients=email_to,
            template_body=template_params,
            subtype=MessageType.html,
        )
        
        fm = FastMail(conf)
        await fm.send_message(message, template_name=f"{template_name}.html")
        logger.info(f"Email sent to {', '.join(email_to)}, subject: {subject}")
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        raise


async def send_verification_email(email_to: str, username: str, token: str) -> None:
    """Send an email verification link."""
    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    
    await send_email(
        email_to=[email_to],
        subject="Verify your SnapWave account",
        template_name="email_verification",
        template_params={
            "username": username,
            "verification_url": verification_url,
            "token": token,
            "app_name": settings.PROJECT_NAME,
        },
    )


async def send_password_reset_email(email_to: str, username: str, token: str) -> None:
    """Send a password reset link."""
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    
    await send_email(
        email_to=[email_to],
        subject="Reset your SnapWave password",
        template_name="password_reset",
        template_params={
            "username": username,
            "reset_url": reset_url,
            "token": token,
            "app_name": settings.PROJECT_NAME,
        },
    )

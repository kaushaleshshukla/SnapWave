# Script file for database initialization and initial migration

import asyncio
import logging
from sqlalchemy.ext.asyncio import create_async_engine
import os
from app.db.session import Base
from app.core.config import settings

# Import all models to ensure they are registered with Base
from app.models.user import User  # Import all models here

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init_db():
    # Create tables in the database
    # In a real production application, you would use Alembic migrations
    # instead of create_all directly
    try:
        # Use an async version of the engine for init
        engine = create_async_engine(settings.DATABASE_URL)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


if __name__ == "__main__":
    logger.info("Creating database tables...")
    asyncio.run(init_db())

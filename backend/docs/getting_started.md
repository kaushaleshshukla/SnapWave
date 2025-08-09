# SnapWave Backend: Getting Started Guide

This guide will walk you through the process of setting up and running the SnapWave backend application.

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- Git (for cloning the repository)
- MinIO (optional, for media storage)

## Setting Up the Development Environment

### 1. Clone the Repository

If you haven't already cloned the repository:

```bash
git clone https://github.com/kaushaleshshukla/SnapWave.git
cd SnapWave
```

### 2. Set Up the Virtual Environment

Navigate to the backend directory and set up a virtual environment:

```bash
cd backend

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

Your terminal prompt should change to indicate that the virtual environment is active.

### 3. Install Dependencies

With the virtual environment activated, install the required dependencies:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the backend directory:

```bash
touch .env
```

Open the file and add the following configuration (adjust as needed):

```
# Database settings
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/snapwave

# Security settings
SECRET_KEY=your_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours

# Email settings (for development)
EMAIL_DEV_MODE=True
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
MAIL_FROM=your_email@example.com
MAIL_FROM_NAME=SnapWave
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
MAIL_USE_CREDENTIALS=True
MAIL_VALIDATE_CERTS=True

# Frontend URL (for links in emails)
FRONTEND_URL=http://localhost:3000

# Storage settings (for MinIO/S3)
STORAGE_ENDPOINT=localhost:9000
STORAGE_ACCESS_KEY=minioaccess
STORAGE_SECRET_KEY=miniosecret
STORAGE_BUCKET_NAME=snapwave
STORAGE_USE_HTTPS=False
```

### 5. Start the PostgreSQL Database Server

Ensure your PostgreSQL server is running before continuing:

#### macOS
```bash
# Start PostgreSQL server on macOS (if installed with Homebrew)
brew services start postgresql
# or
pg_ctl -D /usr/local/var/postgres start
```

#### Linux (Ubuntu/Debian)
```bash
# Start PostgreSQL server on Linux
sudo service postgresql start
# or
sudo systemctl start postgresql
```

#### Windows
On Windows, PostgreSQL typically runs as a service that starts automatically.
You can check the service status in the Services application.

### 6. Set Up the Database

Create a PostgreSQL database for the application:

```bash
# Using psql
psql -U postgres
```

In the PostgreSQL prompt:

```sql
CREATE DATABASE snapwave;
CREATE USER snapwave_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE snapwave TO snapwave_user;
\q
```

Then run the database migrations:

```bash
# Inside the backend directory with the virtual environment activated
alembic upgrade head
```

## Starting the Server

### Development Server

First, ensure all required services are running:

1. **PostgreSQL** database server (as described in previous steps)
2. **MinIO** (if you're working with media uploads):
   ```bash
   # If installed with Docker
   docker run -p 9000:9000 -p 9001:9001 -e "MINIO_ROOT_USER=minioaccess" -e "MINIO_ROOT_PASSWORD=miniosecret" minio/minio server /data --console-address ":9001"
   ```

Then start the FastAPI server with auto-reload:

```bash
# Make sure your virtual environment is activated
cd /path/to/SnapWave/backend
source venv/bin/activate

# Start the server with auto-reload
uvicorn app.main:app --reload
```

This will start the server at http://127.0.0.1:8000.

Alternatively, you can use the built-in script:

```bash
# Make the script executable first (if needed)
chmod +x start_server.py

# Run the script
./start_server.py
```

### Production Server

For production deployment:

```bash
# Without auto-reload and with production workers
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Or using Gunicorn with Uvicorn workers (recommended for production)
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

Make sure all required services (PostgreSQL, MinIO/S3) are properly configured and running in your production environment.

## Accessing the API

Once the server is running, you can access:

- API documentation: http://127.0.0.1:8000/docs
- Alternative documentation: http://127.0.0.1:8000/redoc
- Health check: http://127.0.0.1:8000/health

## API Structure

The API is organized with a version prefix `/api/v1` followed by resource-specific endpoints:

- Authentication: `/api/v1/auth/*`
- Users: `/api/v1/users/*`
- Media: `/api/v1/media/*` 
- Social interactions: `/api/v1/interactions/*`

## Testing

### Running Tests

To run tests, use:

```bash
# From the backend directory with virtual environment activated
pytest
```

### Testing Email Functionality

To test the email functionality specifically:

```bash
# Run the test script for email service
python tests/test_email_service.py
```

Or use API endpoints with the server running:

```bash
# Register a user (triggers verification email)
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "Password123!",
    "full_name": "Test User"
  }'

# Request password reset (triggers reset email)
curl -X POST http://localhost:8000/api/v1/auth/password-reset/request \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com"
  }'
```

When running in development mode (`EMAIL_DEV_MODE=True`), emails will be logged to the console rather than actually sent.

## Troubleshooting

### Common Issues

1. **Database connection errors**:
   - Check that PostgreSQL is running (`pg_isready` command will tell you)
   - Verify the DATABASE_URL in your .env file
   - Ensure the database and user exist with proper permissions
   - Try connecting with `psql` to rule out network/authentication issues

2. **Import errors when starting the server**:
   - Ensure you're in the correct directory (backend/)
   - Make sure all dependencies are installed
   - Check that your virtual environment is activated

3. **JWT authentication issues**:
   - Verify that SECRET_KEY is set in your .env file
   - Check token expiration settings

4. **Email sending issues**:
   - In production, check your SMTP settings
   - For Gmail, you may need to use an App Password
   - In development, set EMAIL_DEV_MODE=True to log instead of send

## Architecture

The backend follows a layered architecture:

- **API Layer**: FastAPI routes in app/api/
- **Service Layer**: Business logic in app/services/
- **Data Access Layer**: CRUD operations in app/crud/
- **Models**: Database models in app/models/
- **Schemas**: Pydantic schemas for validation in app/schemas/

For a more detailed overview of the entire system architecture, refer to the main [ARCHITECTURE.md](../../ARCHITECTURE.md) file.

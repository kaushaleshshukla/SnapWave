# SnapWave Backend

This is the backend service for SnapWave, a scalable media sharing platform.

## Development Setup

### Prerequisites

- Python 3.9+
- PostgreSQL
- MinIO (for object storage)

### Environment Setup

1. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the `backend` directory:

```
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/snapwave
```

### Database Setup

1. Create PostgreSQL database:

```bash
createdb snapwave
```

2. Initialize the database:

```bash
# Using Alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Running the API Server

```bash
./start_server.py
```

Or:

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access the interactive API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing the API

### Authentication

1. Register a new user:

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com", "username":"testuser", "password":"password123", "full_name":"Test User"}'
```

2. Get an access token:

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"
```

3. Use the access token to access protected endpoints:

```bash
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Project Structure

- `app/`: Main application package
  - `api/`: API endpoints
    - `v1/`: API version 1
      - `auth.py`: Authentication endpoints
      - `users.py`: User management endpoints
      - `deps.py`: Dependency functions
  - `core/`: Core functionality
    - `config.py`: Application configuration
    - `security.py`: Security utilities
  - `crud/`: Database operations
    - `user.py`: User CRUD operations
  - `db/`: Database utilities
    - `session.py`: Database session management
    - `init_db.py`: Database initialization
  - `models/`: SQLAlchemy models
    - `user.py`: User model
  - `schemas/`: Pydantic schemas
    - `user.py`: User schemas
    - `token.py`: Authentication token schemas
  - `main.py`: Application entry point

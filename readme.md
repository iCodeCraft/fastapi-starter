# 🚀 FastAPI Starter

> A production-ready FastAPI boilerplate with PostgreSQL, SQLAlchemy (async), JWT authentication, and comprehensive documentation. Perfect for building scalable APIs with modern Python practices.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A modern, scalable FastAPI boilerplate that provides everything you need to build production-ready APIs. Features async database operations, JWT authentication, comprehensive logging, Docker support, and extensive documentation.

## ✨ Features

- **FastAPI** - Modern, fast web framework for building APIs
- **PostgreSQL** - Robust relational database
- **SQLAlchemy 2.0** - Async ORM with type safety
- **Alembic** - Database migrations
- **JWT Authentication** - Secure token-based authentication
- **Pydantic** - Data validation and serialization
- **Docker** - Containerized deployment
- **Comprehensive Logging** - Structured logging configuration
- **CORS Support** - Cross-origin resource sharing
- **Health Checks** - Application monitoring endpoints

## 🛠️ Tech Stack

- **Python 3.11**
- **FastAPI 0.104+**
- **SQLAlchemy 2.0+**
- **PostgreSQL**
- **Alembic**
- **Pydantic 2.5+**
- **Uvicorn**
- **Docker**

## 📁 Project Structure

```
fastapi-starter/
├── alembic/                 # Database migrations
│   ├── versions/           # Migration files
│   ├── env.py             # Alembic environment
│   └── script.py.mako     # Migration template
├── src/
│   ├── api/               # API routes and dependencies
│   │   ├── dependencies.py # Authentication and dependencies
│   │   └── v1/            # API version 1
│   │       └── user.py    # User endpoints
│   ├── core/              # Core configuration
│   │   ├── config.py      # Application settings
│   │   ├── logger.py      # Logging configuration
│   │   └── security.py    # JWT authentication
│   ├── db/                # Database configuration
│   │   └── postgres.py    # PostgreSQL connection
│   ├── models/            # SQLAlchemy models
│   │   └── user.py        # User model
│   ├── schemas/           # Pydantic schemas
│   │   └── user.py        # User schemas
│   └── services/          # Business logic
│       └── user.py        # User service
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── alembic.ini           # Alembic configuration
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL
- Docker (optional)

### 1. Clone the repository

```bash
git clone <repository-url>
cd fastapi-starter
```

### 2. Set up environment

```bash
# Copy environment file
cp .env\ example .env

# Edit .env with your configuration
nano .env
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up database

```bash
# Create PostgreSQL database
createdb fastapi_starter

# Run migrations
alembic upgrade head
```

### 5. Run the application

```bash
python main.py
```

The API will be available at:
- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🐳 Docker Deployment

### Build and run with Docker

```bash
# Build the image
docker build -t fastapi-starter .

# Run the container
docker run -p 8000:8000 --env-file .env fastapi-starter
```

### Docker Compose (recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f app
```

## 📚 API Documentation

### Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### Endpoints

#### Authentication

- `POST /api/v1/users/auth/login` - Login with email
- `POST /api/v1/users/auth/register` - Register new user with email

#### User Management

- `GET /api/v1/users/me` - Get current user info
- `PUT /api/v1/users/me` - Update current user
- `DELETE /api/v1/users/me` - Delete current user

#### System

- `GET /health` - Health check
- `GET /` - Root endpoint

### Example Usage

#### 1. Register New User

```bash
curl -X POST "http://localhost:8000/api/v1/users/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com"}'
```

#### 2. Login

```bash
curl -X POST "http://localhost:8000/api/v1/users/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com"}'
```

#### 3. Get Current User

```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
     -H "Authorization: Bearer <your-token>"
```

#### 4. Update User

```bash
curl -X PUT "http://localhost:8000/api/v1/users/me" \
     -H "Authorization: Bearer <your-token>" \
     -H "Content-Type: application/json" \
     -d '{"email": "newemail@example.com"}'
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PROJECT_NAME` | Application name | `fastapi-starter` |
| `PROJECT_HOST` | Host to bind to | `127.0.0.1` |
| `PROJECT_PORT` | Port to bind to | `8000` |
| `POSTGRES_USER` | PostgreSQL username | `postgres` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `postgres` |
| `POSTGRES_SERVER` | PostgreSQL server | `localhost` |
| `POSTGRES_PORT` | PostgreSQL port | `5432` |
| `POSTGRES_DB` | PostgreSQL database | `fastapi_starter` |
| `SECRET_KEY` | JWT secret key | `your-very-secret-and-long-key-that-is-hard-to-guess-at-least-32-characters` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `43200` (30 days) |

## 🗄️ Database Migrations

### Create a new migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations

```bash
alembic upgrade head
```

### Rollback migration

```bash
alembic downgrade -1
```

## 🧪 Testing

### Run tests (when implemented)

```bash
pytest
```

### Run with coverage

```bash
pytest --cov=src
```

## 📝 Logging

The application uses structured logging with the following levels:
- **DEBUG**: Detailed information for debugging
- **INFO**: General information about application flow
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failed operations

## 🔒 Security

- JWT tokens for authentication
- Password hashing (when implemented)
- CORS configuration
- Input validation with Pydantic
- SQL injection protection with SQLAlchemy

## 🚀 Production Deployment

### Environment Setup

1. Set `PROJECT_HOST=0.0.0.0` for external access
2. Configure proper CORS origins
3. Use strong `SECRET_KEY`
4. Set up proper database credentials
5. Configure logging for production

### Performance

- Use async/await for database operations
- Implement connection pooling
- Add caching layer (Redis) if needed
- Monitor with health checks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the logs for debugging information

---

**⭐ Star this repository if you find it helpful!**

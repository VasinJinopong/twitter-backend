# Twitter Backend API

A Twitter-like backend API built with FastAPI, PostgreSQL, and JWT authentication.

## Features

- User authentication (Register, Login, JWT)
- User management (CRUD operations)
- Post management (CRUD operations)
- Role-based access control
- Database relationships (1:M User-Post)
- Comprehensive error handling

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT + OAuth2
- **Password Hashing**: bcrypt
- **Validation**: Pydantic
- **Testing**: pytest
- **Containerization**: Docker

## Project Structure
```
twitter-backend/
├── app/
│   ├── core/
│   │   ├── config.py          # Settings from .env
│   │   └── security.py        # JWT & password hashing
│   ├── dependencies/
│   │   └── auth.py            # Auth dependency injection
│   ├── models/
│   │   ├── user.py            # User SQLAlchemy model
│   │   └── post.py            # Post SQLAlchemy model
│   ├── routers/
│   │   ├── auth.py            # Auth endpoints
│   │   ├── users.py           # User endpoints
│   │   └── posts.py           # Post endpoints
│   ├── schemas/
│   │   ├── user.py            # User validation schemas
│   │   └── post.py            # Post validation schemas
│   ├── database.py            # Database connection & session
│   └── main.py                # FastAPI app setup
├── tests/
│   ├── test_auth.py           # Auth tests
│   └── test_dependencies.py   # Dependency tests
├── docker-compose.yml         # PostgreSQL + pgAdmin
├── .env                       # Environment variables (git ignored)
├── .env.example               # Environment template
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## API Endpoints

### Auth
- `POST /api/v1/auth/register` - Register user
- `POST /api/v1/auth/login` - Login user

### Users
- `GET /api/v1/users/me` - Get current user (requires auth)
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/me` - Update current user (requires auth)
- `DELETE /api/v1/users/me` - Delete current user (requires auth)

### Posts
- `POST /api/v1/posts` - Create post (requires auth)
- `GET /api/v1/posts` - Get all posts (paginated)
- `GET /api/v1/posts/{id}` - Get single post
- `PUT /api/v1/posts/{id}` - Update post (owner only)
- `DELETE /api/v1/posts/{id}` - Delete post (owner only)
- `GET /api/v1/posts/user/{id}` - Get user's posts

## Installation

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- Git

### Setup

1. **Clone repository**
```bash
git clone <repo-url>
cd twitter-backend
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
# On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Start PostgreSQL with Docker**
```bash
docker-compose up -d
```

6. **Run server**
```bash
python -m app.main
```

Server runs on `http://localhost:8000`

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing

### Run unit tests
```bash
pytest tests/ -v -s
```

### Test with Postman
1. Register user
2. Login to get token
3. Use token in Authorization header for protected endpoints

## Database Management

### pgAdmin
Access at `http://localhost:5050`

⚠️ **IMPORTANT - Change default credentials in production:**
- Default Email: admin@example.com
- Default Password: admin

Edit in `docker-compose.yml`:
```yaml
pgadmin:
  environment:
    PGADMIN_DEFAULT_EMAIL: your_email@example.com
    PGADMIN_DEFAULT_PASSWORD: your_secure_password
```

### PostgreSQL Connection
- Host: postgres
- Port: 5432
- Database: twitter_db
- User: twitter_user
- Password: twitter_password (change in production)

## Environment Variables

Create `.env` file (copy from `.env.example`):
```env
# Database
DATABASE_URL=postgresql://twitter_user:twitter_password@localhost:5432/twitter_db

# JWT
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API
API_V1_STR=/api/v1
PROJECT_NAME=Twitter Backend API
DEBUG=True
CORS_ORIGINS=["*"]
```

## Authentication

All protected endpoints require JWT token in Authorization header:
```
Authorization: Bearer <access_token>
```

Token obtained from login endpoint. Token expires after 30 minutes by default.

## Error Handling

- `400 Bad Request` - Invalid input or validation error
- `401 Unauthorized` - Missing or invalid credentials
- `403 Forbidden` - Not authorized (e.g., not post owner)
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Development

### Code Style
- Follow PEP 8
- Use type hints
- Write docstrings

### Git Workflow
```bash
git add -A
git commit -m "feat: description"
git push origin main
```

### Running in Development
```bash
# With auto-reload
python -m app.main

# Or with uvicorn directly
uvicorn app.main:app --reload
```

## Deployment

### Docker Build
```bash
docker build -t twitter-backend .
docker run -p 8000:8000 --env-file .env twitter-backend
```

### Production Checklist
- [ ] Change SECRET_KEY to secure random value
- [ ] Set DEBUG=False
- [ ] Change pgAdmin credentials
- [ ] Change PostgreSQL password
- [ ] Use environment variables for all secrets
- [ ] Set up HTTPS
- [ ] Configure CORS for frontend domain

## Future Features

- [ ] Like/Comment system
- [ ] Follow users
- [ ] Search functionality
- [ ] Notifications
- [ ] Trending posts
- [ ] Admin dashboard
- [ ] Email verification
- [ ] Password reset

## Troubleshooting

### PostgreSQL Connection Failed
```bash
docker-compose ps  # Check if postgres is running
docker-compose logs postgres  # View logs
```

### Port Already in Use
```bash
# Change port in docker-compose.yml
# Or kill process using port
lsof -i :8000  # Check what's using port 8000
```

## License

MIT License

## Author

Vasin Jinopong

## Support

For issues or questions, please open an issue on GitHub.


## Test CICD
[x] Test

## Testing

Run tests:
```bash
pytest -v
```

Test coverage:
```bash
pytest --cov=app tests/
```
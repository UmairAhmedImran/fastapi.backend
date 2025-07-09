# Social Media API

A RESTful API built with FastAPI that provides core functionality for a social media platform.

## Features

- User authentication with JWT tokens
- CRUD operations for posts
- Voting system for posts
- User management
- Database migrations with Alembic
- PostgreSQL integration

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Alembic**: Database migration tool
- **PostgreSQL**: Relational database
- **Pydantic**: Data validation and settings management
- **JWT**: Authentication using JSON Web Tokens
- **Bcrypt**: Password hashing

## Prerequisites

- Python 3.8+
- PostgreSQL

## Installation

1. Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:

```
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your_password
DATABASE_NAME=your_db_name
DATABASE_USERNAME=your_username
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTE=30
```

5. Run database migrations

```bash
alembic upgrade head
```

## Running the Application

Start the server with:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:

- Interactive API documentation: `http://localhost:8000/docs`
- Alternative API documentation: `http://localhost:8000/redoc`

## API Endpoints

### Authentication

- `POST /login` - User login

### Users

- `POST /users` - Create a new user
- `GET /users/{id}` - Get user by ID

### Posts

- `GET /posts` - Get all posts (with pagination, search, and limit)
- `POST /posts` - Create a new post
- `GET /posts/{id}` - Get a specific post
- `DELETE /posts/{id}` - Delete a post
- `PUT /posts/{id}` - Update a post

### Votes

- `POST /votes` - Vote or unvote a post

## Database Schema

The application uses the following main tables:

- `users`: Stores user information
- `posts`: Stores post content with foreign key to users
- `votes`: Junction table for post votes with composite primary key

## Development

### Database Migrations

To create a new migration after model changes:

```bash
alembic revision --autogenerate -m "description"
```

To apply migrations:

```bash
alembic upgrade head
```

To revert migrations:

```bash
alembic downgrade -1
```

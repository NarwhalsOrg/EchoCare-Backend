# Healthcare API

A FastAPI backend for a healthcare application with Supabase as the database.

## Features

- User authentication with JWT
- File uploads for avatars and prescriptions using Supabase Storage
- Patient management
- Appointment scheduling
- Prescription management
- AI-assisted diagnosis and medication tools
- Comprehensive error handling
- Docker support

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Supabase**: Open source Firebase alternative (PostgreSQL, Auth, Storage)
- **SQLModel**: ORM for FastAPI and SQLAlchemy
- **Python-Jose**: JWT token handling
- **Passlib**: Password hashing with bcrypt
- **Docker**: Containerization

## Project Structure

```
healthcare-api/
├── app/
│   ├── AItool/                  # AI-assisted tools
│   ├── core/                    # Core functionality (config, security, dependencies)
│   ├── db/                      # Database connections and ORM
│   ├── demoData/                # Sample data for development
│   ├── models/                  # Pydantic and SQLModel models
│   ├── routes/                  # API endpoints
│   ├── utils/                   # Utility functions
│   └── main.py                  # Application entry point
├── supabase/
│   └── migrations/              # Database migrations
├── .env.example                 # Environment variables template
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose configuration
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.8+
- Supabase account
- Docker and Docker Compose (optional)

### Environment Setup

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Update the `.env` file with your Supabase credentials and other settings.

### Running with Docker

```bash
docker-compose up -d
```

### Running without Docker

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## Supabase Setup

1. Create a new Supabase project
2. Update your `.env` file with the Supabase URL and anon key
3. Run the migrations in the `supabase/migrations` directory

## Authentication

The API uses JWT tokens for authentication:

1. Register a new user: `POST /api/auth/register`
2. Login: `POST /api/auth/login`
3. Use the returned access token in the Authorization header: `Bearer <token>`

## File Uploads

The API supports file uploads for:

- User avatars: `POST /api/users/me/avatar`
- Prescription files: `POST /api/prescriptions/{prescription_id}/upload`

Files are stored in Supabase Storage buckets.

## License

This project is licensed under the MIT License.
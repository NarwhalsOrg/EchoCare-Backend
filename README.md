# Healthcare API

A FastAPI backend for a healthcare application with Supabase integration.

## Features

- User authentication with JWT
- File uploads for avatars and prescriptions using Supabase Storage
- Patient management
- Appointment scheduling
- Prescription management
- Role-based access control
- Exception handling
- ORM with SQLAlchemy
- AI tools for medical assistance

## Tech Stack

- FastAPI
- SQLAlchemy (ORM)
- Supabase (Storage)
- PostgreSQL
- JWT Authentication
- Docker

## Project Structure

```
healthcare-api/
├── app/
│   ├── AItools/              # AI-related tools
│   ├── controllers/          # Business logic
│   ├── db/                   # Database configuration
│   ├── demoData/             # Demo data for testing
│   ├── models/               # SQLAlchemy models
│   ├── routes/               # API endpoints
│   ├── schemas/              # Pydantic schemas
│   └── utils/                # Utility functions
├── .env.example              # Environment variables example
├── .gitignore                # Git ignore file
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker Compose configuration
├── main.py                   # Application entry point
├── README.md                 # Project documentation
└── requirements.txt          # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.8+
- Docker and Docker Compose (optional)
- Supabase account

### Environment Setup

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Update the `.env` file with your Supabase credentials and other configuration.

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

### Seeding Demo Data

To populate the database with demo data:

```bash
python -m app.demoData.seed
```

## API Documentation

Once the server is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Authentication

The API uses JWT tokens for authentication. To authenticate:

1. Register a user: `POST /api/auth/register`
2. Login to get a token: `POST /api/auth/login`
3. Use the token in the Authorization header: `Authorization: Bearer <token>`

## File Uploads

The API supports file uploads for:

- User avatars: `POST /api/users/me/avatar`
- Patient avatars: `POST /api/patients/{patient_id}/avatar`
- Prescription files: `POST /api/prescriptions/{prescription_id}/file`

Files are stored in Supabase Storage buckets.

## License

This project is licensed under the MIT License.
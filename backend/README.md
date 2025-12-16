# Backend (FastAPI)

REST API for Marketing IQ platform.

## Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── core/                # Core utilities (config, database)
│   ├── models/              # Database models
│   ├── api/                 # API route handlers
│   ├── middleware/          # Custom middleware
│   ├── queries/             # Database query layer
│   ├── oauth/               # OAuth integrations
│   └── utils/               # Utility functions
├── tests/                   # Tests
├── alembic/                 # Database migrations
├── Dockerfile
└── requirements.txt
```

## Setup

```bash
# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Run API
uvicorn app.main:app --reload
```

## API Docs

- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

# Longhorn Studies Backend

This is a Python Flask backend with SQLAlchemy ORM for database management.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables (optional):
```bash
cp .env.example .env
# Edit .env file with your configuration
```

## Running the Server

```bash
python app.py
```

The server will start on `http://localhost:8000`

## API Endpoints

### Health Check
- **GET** `/api/health` - Check if the API is running

### Items
- **GET** `/api/items` - Get all items
- **GET** `/api/items/<id>` - Get a specific item
- **POST** `/api/items` - Create a new item
  ```json
  {
    "name": "Item name",
    "description": "Optional description"
  }
  ```
- **PUT** `/api/items/<id>` - Update an item
  ```json
  {
    "name": "Updated name",
    "description": "Updated description"
  }
  ```
- **DELETE** `/api/items/<id>` - Delete an item

### Users
- **GET** `/api/users` - Get all users
- **POST** `/api/users` - Create a new user
  ```json
  {
    "username": "username",
    "email": "email@example.com"
  }
  ```

## Database

The application uses SQLite by default for development. The database file will be created automatically as `longhorn_studies.db` when you first run the application.

To use a different database (PostgreSQL, MySQL, etc.), update the `DATABASE_URL` in your `.env` file.

## Project Structure

```
backend/
├── app.py              # Flask application initialization
├── models.py           # SQLAlchemy database models
├── routes.py           # API route definitions
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Middleware

The application includes:
- **CORS**: Configured to allow cross-origin requests from the frontend
- **Request Logging**: Logs all incoming requests with timestamps
- **Error Handlers**: Custom error handlers for 400, 404, and 500 errors

## Development

The application runs in debug mode by default for development. For production:

1. Set `FLASK_ENV=production` in your `.env` file
2. Change the `SECRET_KEY` to a secure random value
3. Use a production-grade database (PostgreSQL recommended)
4. Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```

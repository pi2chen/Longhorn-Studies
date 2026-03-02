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

### Study Spots
- **GET** `/api/study_spots` - Get all study spots
- **GET** `/api/study_spots/<id>` - Get a specific study spot
- **POST** `/api/study_spots` - Create a new study spot (requires: abbreviation, study_spot_name, address, noise_level, capacity, spot_type, access_hours, near_food, reservable, description, pictures)
  ```json
  {
    "abbreviation": "PCL",
    "study_spot_name": "3rd Floor",
    "building_name": "Perry-Castañeda Library",
    "address": "101 E 21st St",
    "floor": 3,
    "tags": ["quiet", "wifi"],
    "pictures": ["https://example.com/pcl1.jpg"],
    "noise_level": "Low",
    "capacity": 100,
    "spot_type": ["Open Area", "Library"],
    "access_hours": [
      ["08:00", "22:00"],
      ["08:00", "22:00"],
      ["08:00", "22:00"],
      ["08:00", "22:00"],
      ["08:00", "18:00"],
      ["10:00", "16:00"],
      ["00:00", "00:00"]
    ],
    "near_food": true,
    "additional_properties": null,
    "reservable": false,
    "description": "Main campus library."
  }
  ```
- **PUT** `/api/study_spots/<id>` - Update a study spot (send only fields to update)
- **DELETE** `/api/study_spots/<id>` - Delete a study spot

`GET /api/study_spots*` responses return `pictures` as backend image API URLs in the format:
`/api/study_spots/<id>/images/<image_index>`

### Images
- **GET** `/api/study_spots/<id>/images/<image_index>` - Proxy an image by study spot ID and picture index (recommended for frontend use)
- **GET** `/api/image_proxy?url=<encoded_remote_url>` - Proxy a remote image URL directly (useful for one-off testing/debugging)

### Uploading and Accessing Images
This backend stores image **URLs** in the database (it does not accept raw image file uploads).

1. Host each image at a publicly accessible URL (Google Drive public links are supported and normalized).
2. Create or update a study spot with those URLs in the `pictures` array via:
   - `POST /api/study_spots`
   - `PUT /api/study_spots/<id>`
3. Read the study spot from:
   - `GET /api/study_spots`
   - `GET /api/study_spots/<id>`
4. Use each returned `pictures` value directly in the frontend. These values are backend API endpoints like:
   - `http://localhost:8000/api/study_spots/1/images/0`
5. Optional: For a specific source URL, you can also access it through:
   - `GET /api/image_proxy?url=<encoded_remote_url>`

## Database

The application uses SQLite by default for development. The database file will be created automatically as `longhorn_studies.db` when you first run the application.

To use a different database (PostgreSQL, MySQL, etc.), update the `DATABASE_URL` in your `.env` file.

## Project Structure

```
backend/
├── app.py              # Flask application initialization
├── models.py           # SQLAlchemy database models
├── routes.py           # API route definitions
├── scripts/            # Utility scripts
│   ├── update_db.sh    # POST one study spot
│   ├── delete_db.sh    # DELETE a study spot by ID
│   ├── update_fields.sh # PUT partial update
│   ├── test_crud_db.sh # End-to-end CRUD verification
├── requirements.txt   # Python dependencies
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

To normalize existing image links in the database:

```bash
cd backend
source venv/bin/activate
python scripts/normalize_picture_links.py
```

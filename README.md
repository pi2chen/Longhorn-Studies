# Longhorn Studies

A full-stack application with React Native frontend and Python Flask backend with SQLAlchemy database.

## Project Structure

```
Longhorn-Studies/
├── frontend/           # React Native application (Expo)
│   ├── App.js         # Main app component with API integration
│   ├── package.json   # Node.js dependencies
│   ├── app.json       # Expo configuration
│   └── README.md      # Frontend documentation
│
├── backend/           # Python Flask API with SQLAlchemy
│   ├── app.py         # Flask application setup
│   ├── models.py      # Database models
│   ├── routes.py      # API endpoints
│   ├── requirements.txt  # Python dependencies
│   └── README.md      # Backend documentation
│
└── README.md          # This file
```

## Quick Start

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the server:
   ```bash
   python app.py
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Choose your platform:
   - Press `w` for web browser
   - Press `a` for Android emulator
   - Press `i` for iOS simulator
   - Scan QR code with Expo Go app on your phone

## Features

### Frontend
- ✅ React Native with Expo for cross-platform support (Web, iOS, Android)
- ✅ Pre-configured with axios for API communication
- ✅ Sample UI with CRUD operations
- ✅ Responsive design with StyleSheet
- ✅ Error handling and loading states

### Backend
- ✅ Flask REST API with Blueprint architecture
- ✅ SQLAlchemy ORM with SQLite database (easily switchable to PostgreSQL/MySQL)
- ✅ CORS middleware configured for frontend communication
- ✅ Request logging middleware
- ✅ Comprehensive error handling
- ✅ RESTful endpoints for Study Spots
- ✅ Health check endpoint

## API Endpoints

### Health Check
- `GET /api/health` - Verify API status

### Study Spots
- `GET /api/study_spots` - Get all study spots
- `GET /api/study_spots/<id>` - Get a specific study spot
- `POST /api/study_spots` - Create a new study spot
- `PUT /api/study_spots/<id>` - Update a study spot
- `DELETE /api/study_spots/<id>` - Delete a study spot

## Database Models

### StudySpot
- id (Integer, Primary Key)
- abbreviation (String, Required)
- study_spot_name (String, Required)
- building_name (String, Optional)
- address (String, Required)
- floor (Integer, Optional)
- tags (JSON array of strings)
- noise_level (String, Required)
- capacity (Integer, Required)
- spot_type (JSON array of strings, Required)
- access_hours (JSON array of 7 `[open, close]` pairs in `HH:MM`, Monday-Sunday, Required)
- near_food (Boolean, Required)
- additional_properties (Text, Optional)
- reservable (Boolean, Required)
- description (Text, Required)
- pictures (JSON array of strings, Required)

## Development

### Running Both Services

For the best development experience, run both frontend and backend simultaneously:

1. **Terminal 1** - Backend:
   ```bash
   cd backend
   python app.py
   ```

2. **Terminal 2** - Frontend:
   ```bash
   cd frontend
   npm start
   ```

The frontend will automatically connect to the backend API at `http://localhost:8000/api`.

## Technology Stack

### Frontend
- React 18.2.0
- React Native 0.72.6
- Expo ~49.0.15
- Axios for HTTP requests

### Backend
- Python 3.8+
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-CORS 4.0.0
- SQLAlchemy 2.0.23

## Configuration

### Backend Configuration
Edit `backend/.env` (copy from `.env.example`):
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - Flask secret key
- `PORT` - Server port (default: 8000)

### Frontend Configuration
Edit `frontend/App.js`:
- `API_BASE_URL` - Backend API URL (default: `http://localhost:8000/api`)

## Development Workflow
### Branch naming conventions + Conventional Commits
We follow the Conventional Commits specification for commit messages. This ensures a consistent commit history and enables automated versioning and changelog generation.

### Branch Naming Conventions 
```
<type>/<short-description>
```
Examples: 
- feature/{feature-name}
- fix/{bug-description}
- docs/{documentation-change}
### Commit Message
Follow this structure for commit messages
```
<type>(<scope>): <subject>
```
Where:
```type``` has one of the following:
- feat: New features
- fix: Bug fixes
- docs: Documentation changes
- style: Code formatting only
- refactor: Code changes without behavior change
- test: Adding or updating tests
- chore: Build process or tooling updates

### PR process
- Fork or branch from main
- Create a PR with a clear description
- Ensure checks pass (build, lint, test)
- Request review before merging

## Development Workflow
### Branch naming conventions + Conventional Commits
We follow the Conventional Commits specification for commit messages. This ensures a consistent commit history and enables automated versioning and changelog generation.

### Branch Naming Conventions 
```
<type>/<short-description>
```
Examples: 
- feature/{feature-name}
- fix/{bug-description}
- docs/{documentation-change}
### Commit Message
Follow this structure for commit messages
```
<type>(<scope>): <subject>
```
Where:
```type``` has one of the following:
- feat: New features
- fix: Bug fixes
- docs: Documentation changes
- style: Code formatting only
- refactor: Code changes without behavior change
- test: Adding or updating tests
- chore: Build process or tooling updates

### PR process
- Fork or branch from main
- Create a PR with a clear description
- Ensure checks pass (build, lint, test)
- Request review before merging

## License

MIT

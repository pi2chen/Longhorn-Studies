# Longhorn Studies - Complete Setup Guide

This guide will walk you through setting up both the frontend and backend for the Longhorn Studies application.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Backend Setup](#backend-setup)
3. [Frontend Setup](#frontend-setup)
4. [Testing the Application](#testing-the-application)
5. [Troubleshooting](#troubleshooting)

## Prerequisites

### Backend Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment support

### Frontend Requirements
- Node.js 14.x or higher
- npm (comes with Node.js)
- Expo CLI (will be installed automatically)

### Optional
- Git (for cloning and version control)
- A code editor (VS Code, PyCharm, etc.)

## Backend Setup

### Step 1: Navigate to Backend Directory
```bash
cd backend
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment (Optional)
```bash
cp .env.example .env
# Edit .env file if needed
```

### Step 6: Start the Backend Server
```bash
python app.py
```

The backend will be available at: `http://localhost:8000`

**Verify it's working:**
```bash
curl http://localhost:8000/api/health
```

You should see:
```json
{
  "status": "healthy",
  "message": "Longhorn Studies API is running",
  "timestamp": "..."
}
```

## Frontend Setup

### Step 1: Navigate to Frontend Directory
```bash
cd frontend
```

### Step 2: Install Dependencies
```bash
npm install
```

This will install all required packages including React, React Native, Expo, and Axios.

### Step 3: Start the Development Server
```bash
npm start
```

This will start the Expo development server and show you a QR code.

### Step 4: Choose Your Platform

Once the Expo server starts, you can:

**Web (Easiest to test):**
- Press `w` in the terminal
- Your default browser will open with the app

**Mobile Device (iOS/Android):**
- Install "Expo Go" from App Store (iOS) or Play Store (Android)
- Scan the QR code shown in the terminal
- The app will load on your device

**iOS Simulator (macOS only):**
- Press `i` in the terminal
- Requires Xcode to be installed

**Android Emulator:**
- Press `a` in the terminal
- Requires Android Studio to be installed

## Testing the Application

### Backend Tests

Run the integration test script:
```bash
# Make sure backend is running first
cd backend
python app.py

# In another terminal:
bash test_integration.sh
```

### Manual Testing

1. **Start the backend:**
   ```bash
   cd backend
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   python app.py
   ```

2. **Start the frontend:**
   ```bash
   cd frontend
   npm start
   # Press 'w' for web
   ```

3. **Test the flow:**
   - The frontend will load and automatically try to fetch items
   - Try adding a new item using the input field
   - Click "Add" to create an item
   - Click "Delete" to remove an item
   - Click "Refresh Items" to reload the list

### API Endpoints

You can test the API directly:

```bash
# Health check
curl http://localhost:8000/api/health

# Get all items
curl http://localhost:8000/api/items

# Create an item
curl -X POST http://localhost:8000/api/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Item", "description": "Test description"}'

# Get specific item
curl http://localhost:8000/api/items/1

# Update an item
curl -X PUT http://localhost:8000/api/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Item"}'

# Delete an item
curl -X DELETE http://localhost:8000/api/items/1
```

## Troubleshooting

### Backend Issues

**Problem: Port 8000 is already in use**
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9
# Or change the port in backend/app.py
```

**Problem: Module not found**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
```

**Problem: Database error**
```bash
# Delete the database and let it recreate
rm instance/longhorn_studies.db
python app.py
```

### Frontend Issues

**Problem: Network request failed**
- Make sure the backend is running on port 8000
- Check the `API_BASE_URL` in `frontend/App.js`
- If testing on a physical device, use your computer's IP address instead of localhost

**Problem: npm install fails**
```bash
# Clear npm cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Problem: Expo won't start**
```bash
# Clear Expo cache
npx expo start -c
```

**Problem: Can't connect from mobile device**
- Make sure your computer and phone are on the same WiFi network
- Update `API_BASE_URL` in `App.js` to use your computer's IP:
  ```javascript
  const API_BASE_URL = 'http://YOUR_COMPUTER_IP:8000/api';
  ```

### Database Issues

**Problem: Need to reset the database**
```bash
cd backend
rm instance/longhorn_studies.db
python app.py  # Will recreate the database
```

**Problem: Want to use PostgreSQL instead of SQLite**
1. Install PostgreSQL and create a database
2. Update `.env` file:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/database_name
   ```
3. Install psycopg2:
   ```bash
   pip install psycopg2-binary
   ```

## Development Workflow

### Typical Development Session

1. **Start backend:**
   ```bash
   cd backend
   source venv/bin/activate
   python app.py
   ```

2. **Start frontend (in new terminal):**
   ```bash
   cd frontend
   npm start
   ```

3. **Make changes:**
   - Backend changes: Server will auto-reload
   - Frontend changes: Expo will hot-reload automatically

4. **Test changes:**
   - Use the web interface or mobile app
   - Check backend logs in terminal
   - Use browser developer tools for frontend debugging

### Recommended IDE Setup

**VS Code Extensions:**
- Python
- Pylance
- React Native Tools
- ESLint
- Prettier

**PyCharm/IntelliJ:**
- Python support (built-in)
- React Native console plugin

## Next Steps

After getting everything running, consider:

1. **Add authentication:**
   - Implement JWT tokens
   - Add login/signup pages
   - Protect API routes

2. **Improve the UI:**
   - Add more styling
   - Implement navigation
   - Add loading indicators

3. **Expand the API:**
   - Add more models
   - Implement relationships
   - Add pagination

4. **Deploy:**
   - Deploy backend to Heroku/AWS/DigitalOcean
   - Deploy frontend to Expo
   - Set up continuous deployment

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [React Native Documentation](https://reactnative.dev/)
- [Expo Documentation](https://docs.expo.dev/)
- [Axios Documentation](https://axios-http.com/)

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the logs in both terminals
3. Check that all dependencies are installed correctly
4. Ensure both frontend and backend are running

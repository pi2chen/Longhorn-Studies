# Quick Start Guide

Get up and running with Longhorn Studies in 5 minutes!

## Prerequisites
- Python 3.8+ installed
- Node.js 14+ installed (for frontend, optional)

## Backend Quick Start

```bash
# 1. Navigate to backend
cd backend

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
python app.py
```

✅ Backend running at: http://localhost:8000

Test it:
```bash
curl http://localhost:8000/api/health
```

## Frontend Quick Start

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Start the app
npm start

# 4. Press 'w' for web browser
```

✅ Frontend running in your browser!

## Quick API Test

With backend running:

```bash
# Create an item
curl -X POST http://localhost:8000/api/items \
  -H "Content-Type: application/json" \
  -d '{"name": "My First Item", "description": "Hello!"}'

# Get all items
curl http://localhost:8000/api/items

# Delete an item
curl -X DELETE http://localhost:8000/api/items/1
```

## Common Commands

### Backend
```bash
cd backend
source venv/bin/activate
python app.py
```

### Frontend
```bash
cd frontend
npm start      # Start development server
npm run web    # Run on web directly
```

### Testing
```bash
# Integration test (requires backend running)
bash test_integration.sh
```

## Troubleshooting

**Backend won't start?**
- Make sure virtual environment is activated
- Check Python version: `python --version` (need 3.8+)

**Frontend won't start?**
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again

**Can't connect frontend to backend?**
- Make sure backend is running on port 8000
- Check `API_BASE_URL` in `frontend/App.js`

## Project Structure

```
Longhorn-Studies/
├── backend/           # Python Flask API
│   ├── app.py        # Main application
│   ├── models.py     # Database models
│   └── routes.py     # API endpoints
│
└── frontend/         # React Native app
    ├── App.js        # Main app component
    └── package.json  # Dependencies
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/items` | Get all items |
| POST | `/api/items` | Create item |
| GET | `/api/items/:id` | Get item |
| PUT | `/api/items/:id` | Update item |
| DELETE | `/api/items/:id` | Delete item |
| GET | `/api/users` | Get all users |
| POST | `/api/users` | Create user |

## Need More Help?

- 📖 See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions
- 📖 See [README.md](README.md) for complete documentation
- 📖 See `backend/README.md` for backend details
- 📖 See `frontend/README.md` for frontend details

## Configuration

### Backend (.env)
```bash
DATABASE_URL=sqlite:///longhorn_studies.db
SECRET_KEY=your-secret-key-here
FLASK_ENV=development  # Change to 'production' for production
```

### Frontend (App.js)
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

---

**Happy Coding! 🤘 Hook 'em Horns!**

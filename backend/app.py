from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///longhorn_studies.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize database
from database import db
db.init_app(app)

# Import routes after db initialization to avoid circular imports
from routes import api_bp

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')

# Create database tables
with app.app_context():
    db.create_all()
    logging.info("Database tables created successfully")

if __name__ == '__main__':
    # WARNING: Debug mode should be disabled in production
    # Set FLASK_ENV=production in .env for production deployment
    debug_mode = os.getenv('FLASK_ENV', 'development') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=8000)

from flask import Blueprint, request, jsonify
from database import db
from models import Item, User
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Create Blueprint
api_bp = Blueprint('api', __name__)


# Middleware for logging requests
@api_bp.before_request
def log_request():
    """Log all incoming requests."""
    logger.info(f"{request.method} {request.path}")


# Error handlers
@api_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Resource not found'}), 404


@api_bp.errorhandler(400)
def bad_request(error):
    """Handle 400 errors."""
    return jsonify({'error': 'Bad request'}), 400


@api_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


# Health check endpoint
@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return jsonify({
        'status': 'healthy',
        'message': 'Longhorn Studies API is running',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


# Item endpoints
@api_bp.route('/items', methods=['GET'])
def get_items():
    """
    Get all items from the database.
    """
    try:
        items = Item.query.all()
        return jsonify([item.to_dict() for item in items]), 200
    except Exception as e:
        logger.error(f"Error fetching items: {str(e)}")
        return jsonify({'error': 'Failed to fetch items'}), 500


@api_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """
    Get a specific item by ID.
    """
    try:
        item = Item.query.get_or_404(item_id)
        return jsonify(item.to_dict()), 200
    except Exception as e:
        logger.error(f"Error fetching item {item_id}: {str(e)}")
        return jsonify({'error': 'Item not found'}), 404


@api_bp.route('/items', methods=['POST'])
def create_item():
    """
    Create a new item.
    Expected JSON: { "name": "Item name", "description": "Optional description" }
    """
    try:
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({'error': 'Name is required'}), 400
        
        item = Item(
            name=data['name'],
            description=data.get('description', '')
        )
        
        db.session.add(item)
        db.session.commit()
        
        logger.info(f"Created item: {item.name} (ID: {item.id})")
        return jsonify(item.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating item: {str(e)}")
        return jsonify({'error': 'Failed to create item'}), 500


@api_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """
    Update an existing item.
    Expected JSON: { "name": "New name", "description": "New description" }
    """
    try:
        item = Item.query.get_or_404(item_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if 'name' in data:
            item.name = data['name']
        if 'description' in data:
            item.description = data['description']
        
        item.updated_at = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"Updated item: {item.name} (ID: {item.id})")
        return jsonify(item.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating item {item_id}: {str(e)}")
        return jsonify({'error': 'Failed to update item'}), 500


@api_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """
    Delete an item by ID.
    """
    try:
        item = Item.query.get_or_404(item_id)
        item_name = item.name
        db.session.delete(item)
        db.session.commit()
        
        logger.info(f"Deleted item: {item_name} (ID: {item_id})")
        return jsonify({'message': 'Item deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting item {item_id}: {str(e)}")
        return jsonify({'error': 'Failed to delete item'}), 500


# User endpoints
@api_bp.route('/users', methods=['GET'])
def get_users():
    """
    Get all users from the database.
    """
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        return jsonify({'error': 'Failed to fetch users'}), 500


@api_bp.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user.
    Expected JSON: { "username": "username", "email": "email@example.com" }
    """
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'email' not in data:
            return jsonify({'error': 'Username and email are required'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        user = User(
            username=data['username'],
            email=data['email']
        )
        
        db.session.add(user)
        db.session.commit()
        
        logger.info(f"Created user: {user.username} (ID: {user.id})")
        return jsonify(user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating user: {str(e)}")
        return jsonify({'error': 'Failed to create user'}), 500

import jwt
from functools import wraps
from flask import request, jsonify
from models.user import User
from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask import current_app

def encode_token(user_id, is_admin):
    """
    Generates the JWT token
    """
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),  # Token expires in 1 day
            'iat': datetime.utcnow(),
            'sub': user_id,
            'is_admin': is_admin
        }
        return jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return None

def decode_token(token):
    """
    Decodes the JWT token
    """
    try:
        payload = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
        return payload['sub'], payload['is_admin']
    except jwt.ExpiredSignatureError:
        return None, "Token has expired"
    except jwt.InvalidTokenError:
        return None, "Invalid token"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        token = token.split(" ")[1]  # Bearer token format
        user_id, is_admin = decode_token(token)
        if not user_id:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(user_id=user_id, *args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        token = token.split(" ")[1]  # Bearer token format
        user_id, is_admin = decode_token(token)
        if not user_id:
            return jsonify({'message': 'Token is invalid!'}), 401
        if not is_admin:
            return jsonify({'message': 'Admin access required!'}), 403

        return f(*args, **kwargs)
    return decorated

def hash_password(password):
    """
    Hashes the password
    """
    return generate_password_hash(password)

def verify_password(password, hashed_password):
    """
    Verifies a hashed password
    """
    return check_password_hash(hashed_password, password)

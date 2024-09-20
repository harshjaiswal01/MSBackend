from flask import request, jsonify
from services import user_service
from utils.util import token_required, admin_required, encode_token, decode_token
from database import db
from models.user import User

@token_required
def get_user(user_id, id):
    user, error = user_service.get_user(id)
    if error:
        return jsonify(error), 404
    return jsonify(user), 200

@token_required
def update_user_to_admin(user_id, id):
    success, error = user_service.update_user_to_admin(id)
    if error:
        return jsonify(error), 400
    return jsonify(success), 200

def register_user():
    user_data = request.json
    user, error = user_service.register_user(user_data)
    if error:
        return jsonify(error), 400
    return jsonify(user), 201

def login_user():
    credentials = request.json
    user_info, error = user_service.login_user(credentials)
    if error:
        return jsonify(error), 401
    return jsonify(user_info), 200

@token_required
def update_user_name(user_id):
    name_data = request.json
    success, error = user_service.update_user_name(user_id, name_data)
    if error:
        return jsonify(error), 400
    return jsonify(success), 200

def forgot_password():
    user_data = request.json
    user = db.session.query(User).filter_by(email=user_data['email']).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    response, error = user_service.send_reset_code(user_data['email'])

    if error:
        return jsonify(error), 400
    return jsonify(response), 200

def reset_password():
    data = request.json
    response, error = user_service.verify_reset_code(
        email=data['email'],
        reset_code=data['reset_code'],
        new_password=data['new_password']
    )
    if error:
        return jsonify(error), 400
    return jsonify(response), 200

@token_required
def change_password(user_id):
    data = request.json
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not old_password or not new_password:
        return jsonify({"error": "Old and new password required"}), 400

    response, error = user_service.change_password(user_id, old_password, new_password)
    if error:
        return jsonify(error), 400
    return jsonify(response), 200

# @token_required
def refresh_token():
    data = request.get_json()
    refresh_token = data.get('refresh_token')

    if not refresh_token:
        return jsonify({"error": "Refresh token is required"}), 400

    user_id, is_admin = decode_token(refresh_token)
    if not user_id:
        return jsonify({"error": "Invalid refresh token"}), 401

    new_access_token = encode_token(user_id, is_admin)  # Issue new access token

    return jsonify({"access_token": new_access_token}), 200

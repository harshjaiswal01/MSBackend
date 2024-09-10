from flask import request, jsonify
from services import user_service
from utils.util import token_required, admin_required

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
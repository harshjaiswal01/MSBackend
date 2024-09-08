from flask import request, jsonify
from services import user_details_service
from utils.util import token_required

@token_required
def create_user_details():
    user_id = request.user_id
    data = request.json
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    
    user_details, error = user_details_service.create_user_details(user_id=user_id, details_data=data)
    if error:
        return jsonify(error), 400
    return jsonify(user_details), 201

@token_required
def update_user_details(id):
    data = request.json
    user_details, error = user_details_service.update_user_details(id, data)
    if error:
        return jsonify(error), 400
    return jsonify(user_details), 200

@token_required
def get_user_details(id):
    user_details, error = user_details_service.get_user_details(id)
    if error:
        return jsonify(error), 404
    return jsonify(user_details), 200

from flask import request, jsonify
from services import vision_board_service
from utils.util import token_required

@token_required
def create_vision_board(user_id):
    data = request.json
    is_admin = request.headers.get('Is-Admin', False)  # Or another way to check if the user is an admin

    if is_admin:
        vision_board, error = vision_board_service.create_vision_board(data, None)  # Admin-created board
    else:
        vision_board, error = vision_board_service.create_vision_board(data, user_id)  # User-created board

    if error:
        return jsonify(error), 400
    return jsonify(vision_board), 201

@token_required
def get_vision_board(vision_board_id):
    vision_board, error = vision_board_service.get_vision_board(vision_board_id)
    if error:
        return jsonify(error), 404
    return jsonify(vision_board), 200

@token_required
def update_vision_board(vision_board_id):
    data = request.json
    vision_board, error = vision_board_service.update_vision_board(vision_board_id, data)
    if error:
        return jsonify(error), 400
    return jsonify(vision_board), 200

@token_required
def delete_vision_board(vision_board_id):
    response, error = vision_board_service.delete_vision_board(vision_board_id)
    if error:
        return jsonify(error), 400
    return jsonify(response), 200

@token_required
def get_user_vision_boards(user_id):
    vision_boards, error = vision_board_service.get_user_vision_boards(user_id)
    if error:
        return jsonify(error), 404
    return jsonify(vision_boards), 200

@token_required
def add_user_vision_board(user_id):
    data = request.json
    vision_board, error = vision_board_service.add_user_vision_board(user_id, data['vision_board_id'])
    if error:
        return jsonify(error), 400
    return jsonify(vision_board), 201

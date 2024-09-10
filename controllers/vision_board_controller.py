from flask import request, jsonify
from services import vision_board_service
from utils.util import token_required

@token_required
def create_vision_board(user_id):
    data = request.json
    print("Vision Data: ", data)

    # Call the service to create the vision board. The service will handle the admin check.
    vision_board, error = vision_board_service.create_vision_board(data, user_id)
    
    if error:
        return jsonify(error), 400
    return jsonify(vision_board), 201

@token_required
def get_vision_board(user_id, vision_board_id):
    vision_board, error = vision_board_service.get_vision_board(vision_board_id)
    if error:
        return jsonify(error), 404
    return jsonify(vision_board), 200

@token_required
def update_vision_board(user_id, vision_board_id):
    data = request.json
    print("Controller Data", data)

    # Call the service to update the vision board
    vision_board, error = vision_board_service.update_vision_board(vision_board_id, data)
    if error:
        return jsonify(error), 400
    return jsonify(vision_board), 200

@token_required
def delete_user_vision_board(user_id, vision_board_id):
    # Only allows deletion of user-created boards, not admin-created boards
    response, error = vision_board_service.delete_user_vision_board(user_id, vision_board_id)
    if error:
        return jsonify(error), 400
    return jsonify(response), 200

@token_required
def get_all_vision_boards(user_id):
    # Retrieve all vision boards for the user (both admin-created and user-created)
    vision_boards, error = vision_board_service.get_all_vision_boards_for_user(user_id)
    if error:
        return jsonify(error), 404
    return jsonify(vision_boards), 200

@token_required
def get_subscribed_vision_boards(user_id):
    # Call the service to get all subscribed boards
    vision_boards, error = vision_board_service.get_subscribed_vision_boards(user_id)
    if error:
        return jsonify(error), 404
    return jsonify(vision_boards), 200

@token_required
def add_user_vision_board(user_id):
    data = request.json
    # Subscribe the user to a vision board
    vision_board, error = vision_board_service.add_user_vision_board(user_id, data['vision_board_id'])
    if error:
        return jsonify(error), 400
    return jsonify(vision_board), 201

@token_required
def unsubscribe_from_vision_board(user_id):
    data = request.json
    # Unsubscribe the user from a vision board
    vision_board, error = vision_board_service.unsubscribe_from_vision_board(user_id, data['vision_board_id'])
    if error:
        return jsonify(error), 400
    return jsonify(vision_board), 200

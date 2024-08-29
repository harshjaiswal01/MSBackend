from flask import request, jsonify
from services import content_item_service
from utils.util import token_required

@token_required
def add_content_item(vision_board_id):
    data = request.json
    content_item, error = content_item_service.add_content_item(
        vision_board_id, data['content_url'], data['content_type']
    )
    if error:
        return jsonify(error), 400
    return jsonify(content_item), 201

@token_required
def update_content_item(content_item_id):
    data = request.json
    content_item, error = content_item_service.update_content_item(content_item_id, data)
    if error:
        return jsonify(error), 400
    return jsonify(content_item), 200

@token_required
def delete_content_item(content_item_id):
    response, error = content_item_service.delete_content_item(content_item_id)
    if error:
        return jsonify(error), 400
    return jsonify(response), 200

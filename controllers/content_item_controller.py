from flask import request, jsonify
from services import content_item_service
from utils.util import token_required

@token_required
def add_content_item(user_id, vision_board_id):
    data = request.json
    content_item, error = content_item_service.add_content_item(
        vision_board_id, data['content_url'], data['content_type']
    )
    if error:
        return jsonify(error), 400
    return jsonify(content_item), 201

@token_required
def update_content_item(user_id, content_item_id):
    data = request.json
    content_item, error = content_item_service.update_content_item(content_item_id, data)
    if error:
        return jsonify(error), 400
    return jsonify(content_item), 200

@token_required
def delete_content_item(user_id, content_item_id):
    response, error = content_item_service.delete_content_item(content_item_id)
    if error:
        return jsonify(error), 400
    return jsonify(response), 200

@token_required
def get_content_items(user_id, vision_board_id):
    # Get pagination parameters from the request, default to page 1 and 10 items per page
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Call the service to get paginated content
    content_items, error = content_item_service.get_content_items_for_vision_board(vision_board_id, page, per_page)
    if error:
        return jsonify(error), 400
    return jsonify(content_items), 200

@token_required
def add_custom_article(user_id, vision_board_id):
    data = request.json
    title = data.get('title')
    body = data.get('body')
    description = data.get('description', None)
    main_image_url = data.get('main_image_url', None)

    if not title or not body:
        return jsonify({"error": "Title and body are required"}), 400

    content_item, error = content_item_service.add_custom_article(
        vision_board_id=vision_board_id,
        title=title,
        body=body,
        description=description,
        main_image_url=main_image_url
    )

    if error:
        return jsonify(error), 400
    return jsonify(content_item), 201
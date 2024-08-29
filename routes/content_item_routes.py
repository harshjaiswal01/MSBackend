from flask import Blueprint
from controllers import content_item_controller

content_item_bp = Blueprint('content_item_bp', __name__)

content_item_bp.route('/vision-boards/<int:vision_board_id>/content', methods=['POST'])(content_item_controller.add_content_item)
content_item_bp.route('/vision-boards/content/<int:content_item_id>', methods=['PUT'])(content_item_controller.update_content_item)
content_item_bp.route('/vision-boards/content/<int:content_item_id>', methods=['DELETE'])(content_item_controller.delete_content_item)

from flask import Blueprint
from controllers import vision_board_controller

vision_board_bp = Blueprint('vision_board_bp', __name__)

vision_board_bp.route('/vision-boards', methods=['POST'])(vision_board_controller.create_vision_board)
vision_board_bp.route('/vision-boards/<int:vision_board_id>', methods=['GET'])(vision_board_controller.get_vision_board)
vision_board_bp.route('/vision-boards/<int:vision_board_id>', methods=['PUT'])(vision_board_controller.update_vision_board)
vision_board_bp.route('/vision-boards/<int:vision_board_id>', methods=['DELETE'])(vision_board_controller.delete_vision_board)
vision_board_bp.route('/users/<int:user_id>/vision-boards', methods=['GET'])(vision_board_controller.get_user_vision_boards)
vision_board_bp.route('/users/<int:user_id>/vision-boards', methods=['POST'])(vision_board_controller.add_user_vision_board)

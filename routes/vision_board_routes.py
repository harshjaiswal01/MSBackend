from flask import Blueprint
from controllers import vision_board_controller

# Create a Blueprint for vision board-related routes
vision_board_bp = Blueprint('vision_board_bp', __name__)

# Route to create a vision board (handled by both users and admins)
vision_board_bp.route('/vision-boards', methods=['POST'])(vision_board_controller.create_vision_board)

# Route to get a specific vision board by its ID
vision_board_bp.route('/vision-boards/<int:vision_board_id>', methods=['GET'])(vision_board_controller.get_vision_board)

# Route to update a specific vision board by its ID
vision_board_bp.route('/vision-boards/<int:vision_board_id>', methods=['PUT'])(vision_board_controller.update_vision_board)

# Route to delete a specific vision board by its ID (only allows deletion of user-created boards)
vision_board_bp.route('/users/vision-boards/<int:vision_board_id>', methods=['DELETE'])(vision_board_controller.delete_user_vision_board)

# Route to get all vision boards for a user (admin-created and user-created)
vision_board_bp.route('/users/vision-boards/all', methods=['GET'])(vision_board_controller.get_all_vision_boards)

# Route to get all vision boards a user is subscribed to (admin-created unless unsubscribed)
vision_board_bp.route('/users/vision-boards/subscribed', methods=['GET'])(vision_board_controller.get_subscribed_vision_boards)

# Route to allow a user to add themselves to a vision board subscription
vision_board_bp.route('/users/vision-boards', methods=['POST'])(vision_board_controller.add_user_vision_board)

# Route to allow a user to unsubscribe from an admin-created vision board
vision_board_bp.route('/users/vision-boards/unsubscribe', methods=['POST'])(vision_board_controller.unsubscribe_from_vision_board)

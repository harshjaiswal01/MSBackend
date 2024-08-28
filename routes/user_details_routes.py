from flask import Blueprint
from controllers import user_details_controller

user_details_bp = Blueprint('user_details_bp', __name__)

user_details_bp.route('/user_details', methods=['POST'])(user_details_controller.create_user_details)
user_details_bp.route('/user_details/<int:id>', methods=['PUT'])(user_details_controller.update_user_details)
user_details_bp.route('/user_details/<int:id>', methods=['GET'])(user_details_controller.get_user_details)

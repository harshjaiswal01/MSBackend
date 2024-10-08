from flask import Blueprint
from controllers import user_controller
from controllers import google_oauth_controller

user_bp = Blueprint('user_bp', __name__)

# User-related routes
user_bp.route('/users/<int:id>', methods=['GET'])(user_controller.get_user)
user_bp.route('/users/<int:id>/admin', methods=['PUT'])(user_controller.update_user_to_admin)
user_bp.route('/register', methods=['POST'])(user_controller.register_user)
user_bp.route('/login', methods=['POST'])(user_controller.login_user)
user_bp.route('/users/<int:id>/update-name', methods=['PUT'])(user_controller.update_user_name)
user_bp.route('/forgot-password', methods=['POST'])(user_controller.forgot_password)
user_bp.route('/reset-password', methods=['POST'])(user_controller.reset_password)
user_bp.route('/change-password', methods=['PUT'])(user_controller.change_password)
user_bp.route('/refresh-token', methods=['POST'])(user_controller.refresh_token)

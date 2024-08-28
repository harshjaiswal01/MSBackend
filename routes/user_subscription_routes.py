from flask import Blueprint
from controllers import user_subscription_controller

user_subscription_bp = Blueprint('user_subscription_bp', __name__)

user_subscription_bp.route('/users/<int:user_id>/subscriptions', methods=['PUT'])(user_subscription_controller.update_subscription)

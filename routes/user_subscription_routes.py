from flask import Blueprint
from controllers import user_subscription_controller

user_subscription_bp = Blueprint('user_subscription_bp', __name__)

user_subscription_bp.route('/users/subscriptions', methods=['PUT'])(user_subscription_controller.update_subscription)
user_subscription_bp.route('/users/subscriptions', methods=['GET'])(user_subscription_controller.get_subscription_status)

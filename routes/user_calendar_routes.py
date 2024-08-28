from flask import Blueprint
from controllers import user_calendar_controller

user_calendar_bp = Blueprint('user_calendar_bp', __name__)

user_calendar_bp.route('/users/<int:user_id>/calendar', methods=['GET'])(user_calendar_controller.get_user_calendar)
user_calendar_bp.route('/users/<int:user_id>/calendar/custom', methods=['POST'])(user_calendar_controller.add_custom_event)

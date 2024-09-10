from flask import Blueprint
from controllers import user_calendar_controller

user_calendar_bp = Blueprint('user_calendar_bp', __name__)

user_calendar_bp.route('/calendar', methods=['GET'])(user_calendar_controller.get_user_calendar)
user_calendar_bp.route('/calendar/custom', methods=['POST'])(user_calendar_controller.add_custom_event)
user_calendar_bp.route('/calendar/custom/<int:event_id>', methods=['PUT'])(user_calendar_controller.update_custom_event)
user_calendar_bp.route('/calendar/custom/<int:event_id>', methods=['DELETE'])(user_calendar_controller.delete_custom_event)
user_calendar_bp.route('/calendar/export', methods=['GET'])(user_calendar_controller.export_user_calendar)

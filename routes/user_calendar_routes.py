from flask import Blueprint
from controllers import user_calendar_controller

user_calendar_bp = Blueprint('user_calendar_bp', __name__)

# Get all events for a user
user_calendar_bp.route('/users/<int:user_id>/calendar', methods=['GET'])(user_calendar_controller.get_user_calendar)

# Add a custom event to a user's calendar
user_calendar_bp.route('/users/<int:user_id>/calendar/custom', methods=['POST'])(user_calendar_controller.add_custom_event)

# Update a custom event in a user's calendar
user_calendar_bp.route('/users/<int:user_id>/calendar/custom/<int:event_id>', methods=['PUT'])(user_calendar_controller.update_custom_event)

# Delete a custom event from a user's calendar
user_calendar_bp.route('/users/<int:user_id>/calendar/custom/<int:event_id>', methods=['DELETE'])(user_calendar_controller.delete_custom_event)

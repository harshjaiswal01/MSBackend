# routes/reference_calendar_routes.py
from flask import Blueprint
from controllers import reference_calendar_controller

reference_calendar_bp = Blueprint('reference_calendar_bp', __name__)

reference_calendar_bp.route('/reference_calendar', methods=['POST'])(reference_calendar_controller.create_entry)
reference_calendar_bp.route('/reference_calendar/<int:id>', methods=['GET'])(reference_calendar_controller.get_entry)
reference_calendar_bp.route('/reference_calendar/<int:id>', methods=['PUT'])(reference_calendar_controller.update_entry)
reference_calendar_bp.route('/reference_calendar/<int:id>', methods=['DELETE'])(reference_calendar_controller.delete_entry)
reference_calendar_bp.route('/reference_calendar', methods=['GET'])(reference_calendar_controller.get_all_entries)

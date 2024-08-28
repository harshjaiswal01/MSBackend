from flask import request, jsonify
from services import user_calendar_service
from utils.util import token_required

@token_required
def get_user_calendar(user_id):
    events = user_calendar_service.get_user_calendar(user_id)
    return jsonify(events), 200

@token_required
def add_custom_event(user_id):
    event_data = request.json
    event = user_calendar_service.add_custom_event(user_id, event_data)
    return jsonify(event), 201

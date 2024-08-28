from flask import request, jsonify
from services import reference_calendar_service
from utils.util import admin_required, token_required

# @admin_required
def create_entry():
    # return "Route is working", 200
    data = request.json
    entry, error = reference_calendar_service.create_reference_calendar_event(data)
    if error:
        return jsonify(error), 400
    return jsonify(entry), 201

@token_required
def get_entry(id):
    entry, error = reference_calendar_service.get_reference_calendar_event(id)
    if error:
        return jsonify(error), 404
    return jsonify(entry), 200

@admin_required
def update_entry(id):
    data = request.json
    entry, error = reference_calendar_service.update_reference_calendar(id, data)
    if error:
        return jsonify(error), 400
    return jsonify(entry), 200

@admin_required
def delete_entry(id):
    success, error = reference_calendar_service.delete_reference_calendar_event(id)
    if error:
        return jsonify(error), 404
    return jsonify(success), 200

@token_required
def get_all_entries():
    entries, error = reference_calendar_service.get_all_reference_calendar_events()
    if error:
        return jsonify(error), 400
    return jsonify(entries), 200

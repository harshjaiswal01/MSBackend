from flask import request, jsonify
from services import reference_calendar_service
from utils.util import admin_required, token_required
from models.user import User
from database import db

def is_admin(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    return user.role.name == 'admin'

# @admin_required
@token_required
def create_entry(user_id):
    if not is_admin(user_id):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    entry, error = reference_calendar_service.create_reference_calendar_event(data)
    if error:
        return jsonify(error), 400
    return jsonify(entry), 201

@token_required
def get_entry(user_id):
    entry, error = reference_calendar_service.get_reference_calendar_event(user_id=user_id)
    if error:
        return jsonify(error), 404
    return jsonify(entry), 200

@admin_required
def update_entry(user_id):
    data = request.json
    entry, error = reference_calendar_service.update_reference_calendar(user_id, data)
    if error:
        return jsonify(error), 400
    return jsonify(entry), 200

@admin_required
def delete_entry(user_id):
    success, error = reference_calendar_service.delete_reference_calendar_event(user_id)
    if error:
        return jsonify(error), 404
    return jsonify(success), 200

@token_required
def get_all_entries(user_id):
    entries, error = reference_calendar_service.get_all_reference_calendar_events()
    if error:
        return jsonify(error), 400
    return jsonify(entries), 200

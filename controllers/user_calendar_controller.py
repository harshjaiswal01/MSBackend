from flask import request, jsonify, Response
from services import user_calendar_service
from utils.util import token_required

@token_required
def get_user_calendar(user_id):
    events, error = user_calendar_service.get_user_calendar(user_id)
    if error:
        return jsonify(error), 404
    return jsonify(events), 200

@token_required
def add_custom_event(user_id):
    event_data = request.json
    event, error = user_calendar_service.add_custom_calendar_event(user_id, event_data)
    if error:
        return jsonify(error), 400
    return jsonify(event), 201

@token_required
def update_custom_event(user_id, event_id):
    event_data = request.json
    event, error = user_calendar_service.update_custom_calendar_event(event_id, event_data)
    if error:
        return jsonify(error), 404
    return jsonify(event), 200

@token_required
def delete_custom_event(user_id, event_id):
    message, error = user_calendar_service.delete_custom_calendar_event(event_id)
    if error:
        return jsonify(error), 404
    return jsonify(message), 200

@token_required
def update_event_location(user_id, event_id):
    data = request.json
    event, error = user_calendar_service.update_event_location(event_id, data['location'])
    if error:
        return jsonify(error), 400
    return jsonify(event), 200

@token_required
def export_user_calendar(user_id):
    """
    Export user calendar events as an iCalendar (.ics) file.
    """
    try:
        # Call the service to generate the ICS file
        ics_file = user_calendar_service.export_calendar_to_ics(user_id)
        
        # Return the ICS file as a response
        return Response(
            ics_file,
            mimetype='text/calendar',
            headers={
                'Content-Disposition': 'attachment; filename=user_calendar.ics'
            }
        )
    except Exception as e:
        return {"error": str(e)}, 500
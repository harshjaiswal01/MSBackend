from database import db
from models.reference_calendar import ReferenceCalendar
from models.schemas.reference_calendar_schema import reference_calendar_schema, reference_calendars_schema
from services.user_calendar_service import update_all_user_calendars_on_reference_change

def get_reference_calendar_event(event_id):
    """
    Retrieve a specific reference calendar event by ID.
    """
    event = db.session.query(ReferenceCalendar).filter_by(id=event_id).first()
    if not event:
        return None, {"error": "Reference calendar event not found"}
    return reference_calendar_schema.dump(event), None

def get_all_reference_calendar_events():
    """
    Retrieve all reference calendar events.
    """
    events = db.session.query(ReferenceCalendar).all()
    return reference_calendars_schema.dump(events), None

def create_reference_calendar_event(event_data):
    """
    Create a new reference calendar event.
    """
    new_event = ReferenceCalendar(
        description=event_data['description'],
        day_of_pregnancy=event_data['day_of_pregnancy']
    )
    db.session.add(new_event)
    db.session.commit()

    # Trigger recalculation of all user calendars
    update_all_user_calendars_on_reference_change()

    return reference_calendar_schema.dump(new_event), None

def update_reference_calendar(event_id, data):
    """
    Update an existing reference calendar event.
    """
    event = db.session.query(ReferenceCalendar).filter_by(id=event_id).first()
    if not event:
        return None, {"error": "Reference event not found"}

    event.description = data.get('description', event.description)
    event.day_of_pregnancy = data.get('day_of_pregnancy', event.day_of_pregnancy)

    db.session.commit()

    # Trigger recalculation of all user calendars
    update_all_user_calendars_on_reference_change()

    return reference_calendar_schema.dump(event), None

def delete_reference_calendar_event(event_id):
    """
    Delete a reference calendar event by ID.
    """
    event = db.session.query(ReferenceCalendar).filter_by(id=event_id).first()
    if not event:
        return None, {"error": "Reference calendar event not found"}

    db.session.delete(event)
    db.session.commit()

    # Trigger recalculation of all user calendars
    update_all_user_calendars_on_reference_change()

    return {"message": "Event deleted successfully"}

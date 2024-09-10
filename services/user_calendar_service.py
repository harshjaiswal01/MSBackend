from datetime import timedelta
from database import db
from models.user_calendar import UserCalendar
from models.reference_calendar import ReferenceCalendar
from models.user_details import UserDetails
from models.schemas.user_calendar_schema import user_calendar_schema, user_calendars_schema
from icalendar import Calendar, Event
import io

def calculate_trimesters(due_date):
    """
    Calculate the start and end dates for each trimester based on the due date.
    """
    first_trimester_end = due_date - timedelta(days=196)
    second_trimester_end = due_date - timedelta(days=84)
    third_trimester_end = due_date
    return first_trimester_end, second_trimester_end, third_trimester_end

def populate_user_calendar(user_details):
    """
    Populate the user's calendar based on the reference calendar and due date.
    """
    user_calendar_events = []

    # Fetch reference calendar events
    reference_events = db.session.query(ReferenceCalendar).all()

    # Calculate trimesters
    first_trimester_end, second_trimester_end, third_trimester_end = calculate_trimesters(user_details.due_date)

    # Remove old calendar entries for the user
    db.session.query(UserCalendar).filter_by(user_id=user_details.user_id).delete()

    for event in reference_events:
        event_date = user_details.due_date - timedelta(days=280 - event.day_of_pregnancy)
        user_calendar_event = UserCalendar(
            user_id=user_details.user_id,
            event_date=event_date,
            title=event.title,
            description=event.description
        )
        user_calendar_events.append(user_calendar_event)

    # Save the new events
    db.session.bulk_save_objects(user_calendar_events)
    db.session.commit()

def update_user_calendar_on_due_date_change(user_id):
    """
    Recalculate the user's calendar when the due date changes.
    """
    user_details = db.session.query(UserDetails).filter_by(user_id=user_id).first()
    if user_details:
        populate_user_calendar(user_details)

def update_all_user_calendars_on_reference_change():
    """
    Recalculate all users' calendars when the reference calendar is updated.
    """
    users = db.session.query(UserDetails).all()
    for user_details in users:
        populate_user_calendar(user_details)

def get_user_calendar(user_id):
    """
    Retrieve all calendar events for a specific user.
    """
    events = db.session.query(UserCalendar).filter_by(user_id=user_id).all()
    if not events:
        return None, {"error": "No calendar events found for this user"}
    return user_calendars_schema.dump(events), None

def add_custom_calendar_event(user_id, event_data):
    """
    Add a custom event to the user's calendar.
    """
    custom_event = UserCalendar(
        user_id=user_id,
        event_date=event_data['event_date'],
        description=event_data['description'],
        title = event_data['title'],
        location = event_data['location']
    )
    db.session.add(custom_event)
    db.session.commit()
    return user_calendar_schema.dump(custom_event), None

def update_custom_calendar_event(event_id, event_data):
    """
    Update a custom event in the user's calendar.
    """
    event = db.session.query(UserCalendar).filter_by(id=event_id).first()
    if not event:
        return None, {"error": "Custom event not found"}

    event.event_date = event_data.get('event_date', event.event_date)
    event.description = event_data.get('description', event.description)

    db.session.commit()
    return user_calendar_schema.dump(event), None

def delete_custom_calendar_event(event_id):
    """
    Delete a custom event from the user's calendar.
    """
    event = db.session.query(UserCalendar).filter_by(id=event_id).first()
    if not event:
        return None, {"error": "Custom event not found"}

    db.session.delete(event)
    db.session.commit()
    return {"message": "Custom event deleted successfully"}, None

def update_event_location(event_id, location):
    event = db.session.query(UserCalendar).filter_by(id=event_id).first()
    if not event:
        return None, {"error": "Event not found"}

    event.location = location
    db.session.commit()
    return user_calendar_schema.dump(event), None

def export_calendar_to_ics(user_id):
    """
    Export user's calendar events as an iCalendar (.ics) format.
    """
    # Get all calendar events for the user
    events = get_user_calendar_events(user_id)
    print("\n")
    print(events)
    print("\n")
    if not events:
        return None  # Return None if no events are found

    # Create an iCalendar object
    cal = Calendar()
    cal.add('prodid', '-//My Calendar App//mxm.dk//')
    cal.add('version', '2.0')

    # Add each event to the iCalendar object
    for event in events:
        if isinstance(event, dict):  # Make sure event is a dictionary
            ical_event = Event()
            ical_event.add('summary', event.get('title'))  # Title as 'summary'
            ical_event.add('dtstart', event.get('event_date'))  # Start date
            ical_event.add('description', event.get('description'))  # Description
            ical_event.add('location', event.get('location'))  # Location

            # Add the event to the calendar
            cal.add_component(ical_event)

    # Convert the calendar to string (ICS format)
    ics_file = io.BytesIO()
    ics_file.write(cal.to_ical())
    ics_file.seek(0)

    return ics_file
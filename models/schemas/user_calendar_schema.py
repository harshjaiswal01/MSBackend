from marshmallow import Schema, fields

class UserCalendarSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    event_date = fields.Date(required=True)
    title = fields.Str(required=True, validate=lambda x: len(x) <= 255)  # New title field
    description = fields.Str(required=True, validate=lambda x: len(x) <= 255)
    location = fields.Str(required=False)  # New location field


user_calendar_schema = UserCalendarSchema()
user_calendars_schema = UserCalendarSchema(many=True)

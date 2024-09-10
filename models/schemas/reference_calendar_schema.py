from marshmallow import Schema, fields, validate

class ReferenceCalendarSchema(Schema):
    id = fields.Int(dump_only=True)
    day_of_pregnancy = fields.Int(required=True, validate=validate.Range(min=1))
    title = fields.Str(required=True, validate=validate.Length(max=255))  # New title field
    description = fields.Str(required=True, validate=validate.Length(max=255))


reference_calendar_schema = ReferenceCalendarSchema()
reference_calendars_schema = ReferenceCalendarSchema(many=True)

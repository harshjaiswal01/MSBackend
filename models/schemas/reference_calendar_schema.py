from marshmallow import Schema, fields, validate

class ReferenceCalendarSchema(Schema):
    id = fields.Int(dump_only=True)
    day = fields.Int(required=True, validate=validate.Range(min=1))
    description = fields.Str(required=True, validate=validate.Length(max=255))

reference_calendar_schema = ReferenceCalendarSchema()
reference_calendars_schema = ReferenceCalendarSchema(many=True)

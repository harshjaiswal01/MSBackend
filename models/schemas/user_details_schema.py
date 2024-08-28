from marshmallow import Schema, fields, validate

class UserDetailsSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    sex = fields.Str(validate=validate.Length(max=10))
    pronouns = fields.Str(validate=validate.Length(max=20))
    due_date = fields.Str(validate=validate.Length(max=10))
    first_pregnancy = fields.Bool()
    phone_number = fields.Str(validate=validate.Length(max=20))  # New field
    can_receive_text = fields.Bool()  # New field

user_details_schema = UserDetailsSchema()
user_details_update_schema = UserDetailsSchema(partial=True)

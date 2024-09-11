from marshmallow import Schema, fields

class PasswordResetSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    reset_code = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)

# Instantiate the schema
password_reset_schema = PasswordResetSchema()
password_resets_schema = PasswordResetSchema(many=True)

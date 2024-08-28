from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True, validate=validate.Length(max=255))
    first_name = fields.Str(required=True, validate=validate.Length(max=50))
    last_name = fields.Str(required=True, validate=validate.Length(max=50))
    profile_picture = fields.Str()  # To serialize the profile picture URL
    is_google_login = fields.Bool()  # To indicate if the user registered via Google
    is_admin = fields.Bool(dump_only=True)

class UserRegistrationSchema(Schema):
    email = fields.Email(required=True, validate=validate.Length(max=255))
    password = fields.Str(load_only=True, required=True, validate=validate.Length(min=6))
    first_name = fields.Str(required=True, validate=validate.Length(max=50))
    last_name = fields.Str(required=True, validate=validate.Length(max=50))

class UserLoginSchema(Schema):
    email = fields.Email(required=True, validate=validate.Length(max=255))
    password = fields.Str(load_only=True, required=True, validate=validate.Length(min=6))

class GoogleUserSchema(Schema):
    email = fields.Email(required=True, validate=validate.Length(max=255))
    first_name = fields.Str(required=True, validate=validate.Length(max=50))
    last_name = fields.Str(required=True, validate=validate.Length(max=50))
    profile_picture = fields.Str()

class UserUpdateNameSchema(Schema):
    first_name = fields.Str(required=True, validate=validate.Length(max=50))
    last_name = fields.Str(required=True, validate=validate.Length(max=50))

user_update_name_schema = UserUpdateNameSchema()

# Instantiate schemas for use in the application
user_schema = UserSchema()
user_registration_schema = UserRegistrationSchema()
user_login_schema = UserLoginSchema()
google_user_schema = GoogleUserSchema()
users_schema = UserSchema(many=True)

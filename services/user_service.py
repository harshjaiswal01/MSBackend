from database import db
from models.user import User
from models.schemas.user_schema import user_schema, user_registration_schema, user_login_schema, user_update_name_schema
from utils.util import encode_token, verify_password
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import ValidationError

def get_user(id):
    user = db.session.get(User, id)
    if not user:
        return None, {"error": "User not found"}
    return user_schema.dump(user), None

def update_user_to_admin(id):
    user = db.session.get(User, id)
    if not user:
        return None, {"error": "User not found"}

    user.is_admin = True
    db.session.commit()
    return {"message": "User updated to admin"}, None

def register_user(user_data):
    try:
        validated_data = user_registration_schema.load(user_data)
    except ValidationError as err:
        return None, err.messages

    if db.session.query(User).filter_by(email=validated_data['email']).first():
        return None, {"error": "User with this email already exists"}

    # Hash the password before storing it
    hashed_password = generate_password_hash(validated_data['password'])

    new_user = User(
        email=validated_data['email'],
        password=hashed_password,  # Store the hashed password
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name']
    )
    db.session.add(new_user)
    db.session.commit()

    # Generate a token for the newly created user
    token = encode_token(new_user.id, new_user.is_admin)

    return {"user": user_schema.dump(new_user), "token": token}, None

    # return user_schema.dump(new_user), None

# def login_user(credentials):
#     try:
#         validated_data = user_login_schema.load(credentials)
#     except ValidationError as err:
#         return None, err.messages

#     user = db.session.query(User).filter_by(email=validated_data['email']).first()
#     if not user or not check_password_hash(user.password, validated_data['password']):
#         return None, {"error": "Invalid email or password"}

#     token = encode_token(user.id, user.is_admin)
#     return token, None

def login_user(credentials):
    try:
        validated_data = user_login_schema.load(credentials)
    except ValidationError as err:
        return None, err.messages

    user = db.session.query(User).filter_by(email=validated_data['email']).first()
    if not user or not check_password_hash(user.password, validated_data['password']):
        return None, {"error": "Invalid email or password"}

    token = encode_token(user.id, user.is_admin)
    return {
        "token": token,
        "first_name": user.first_name,
        "last_name": user.last_name
    }, None

def update_user_name(user_id, name_data):
    try:
        validated_data = user_update_name_schema.load(name_data)
    except ValidationError as err:
        return None, err.messages

    user = db.session.get(User, user_id)
    if not user:
        return None, {"error": "User not found"}

    user.first_name = validated_data['first_name']
    user.last_name = validated_data['last_name']
    db.session.commit()

    return {"message": "User name updated successfully"}, None
from database import db
from models.user import User
from models.schemas.user_schema import user_schema, user_registration_schema, user_login_schema, user_update_name_schema
from utils.util import encode_token, verify_password
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import ValidationError
from flask_mail import Message
from flask import render_template
from extensions import mail
from models.password_reset import PasswordReset
import random
from datetime import datetime, timedelta


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

    # Prepare the email message
    msg = Message(
        subject='Welcome to The Melanated Sanctuary!',
        recipients=[new_user.email],
        sender='themelanatedsanctuary@gmail.com'
    )

    # Render the email body using Jinja2 templates
    msg.body = render_template('email/welcome.txt', username=new_user.email, firstname=new_user.first_name, lastname = new_user.last_name)  # Plain text
    msg.html = render_template('email/welcome.html', username=new_user.email, firstname=new_user.first_name, lastname = new_user.last_name)  # HTML

    # Send the email
    mail.send(msg)

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

def generate_reset_code():
    return random.randint(100000, 999999)

def send_reset_code(email):
    user = db.session.query(User).filter_by(email=email).first()
    if not user:
        return None, {"error": "User not found"}

    # Generate and store the reset code in PasswordReset table
    reset_code = generate_reset_code()
    new_reset = PasswordReset(user_id=user.id, reset_code=reset_code)
    
    db.session.add(new_reset)
    db.session.commit()
    
    # Send email with the reset code
    msg = Message(
        subject='Password Reset Code for The Melanated Sanctuary',
        recipients=[user.email],
        sender='themelanatedsanctuary@gmail.com'
    )
    
    msg.body = render_template('email/forgotpassword.txt', reset_code=reset_code, username = email)
    msg.html = render_template('email/forgotpassword.html', reset_code=reset_code, username = email)
    
    mail.send(msg)
    
    return {"message": "Reset code sent to your email"}, None

def verify_reset_code(email, reset_code, new_password):
    user = db.session.query(User).filter_by(email=email).first()
    if not user:
        return None, {"error": "User not found"}
    
    # Find the latest reset request
    reset_record = db.session.query(PasswordReset).filter_by(user_id=user.id, reset_code=reset_code).order_by(PasswordReset.created_at.desc()).first()
    
    if not reset_record or not PasswordReset.is_code_valid(reset_record):
        return None, {"error": "Invalid or expired reset code"}
    
    # Hash and save the new password
    user.password = generate_password_hash(new_password)
    db.session.delete(reset_record)  # Delete the reset record once used
    db.session.commit()

    # Send email for password change confirmation
    msg = Message(
        subject='Password Change Confirmation for The Melanated Sanctuary',
        recipients=[email],
        sender='themelanatedsanctuary@gmail.com'
    )
    
    msg.body = render_template('email/passwordchange.txt', username = email)
    msg.html = render_template('email/passwordchange.html', username = email)
    
    mail.send(msg)
    
    return {"message": "Password reset successfully"}, None

def change_password(user_id, old_password, new_password):
    user = db.session.get(User, user_id)
    if not user or not check_password_hash(user.password, old_password):
        return None, {"error": "Invalid current password"}
    
    # Hash and update with the new password
    user.password = generate_password_hash(new_password)
    db.session.commit()

     # Send email for password change confirmation
    msg = Message(
        subject='Password Change Confirmation for The Melanated Sanctuary',
        recipients=[user.email],
        sender='themelanatedsanctuary@gmail.com'
    )
    
    msg.body = render_template('email/passwordchange.txt', username = user.email)
    msg.html = render_template('email/passwordchange.html', username = user.email)
    
    mail.send(msg)
    
    return {"message": "Password changed successfully"}, None

def cleanup_expired_resets():
    expiration_time = datetime.utcnow() - timedelta(minutes=5)
    db.session.query(PasswordReset).filter(PasswordReset.created_at < expiration_time).delete()
    db.session.commit()
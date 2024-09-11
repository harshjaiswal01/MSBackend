import logging
from flask import Flask, redirect, url_for, session, flash, request
from flask_cors import CORS
from database import db, create_db
from models.schemas import ma
from routes import user_routes
from routes.user_details_routes import user_details_bp
from oauth_config import init_oauth, oauth
from limiter import limiter
from flask_swagger_ui import get_swaggerui_blueprint
from routes.user_subscription_routes import user_subscription_bp
from routes.reference_calendar_routes import reference_calendar_bp
from routes.user_calendar_routes import user_calendar_bp
from routes.vision_board_routes import vision_board_bp
from routes.content_item_routes import content_item_bp
from routes.questionnaire_routes import questionnaire_bp
from routes import reference_calendar_routes
from utils.util import encode_token
import os
from extensions import mail
from flask_mail import Message
from flask import render_template

# Swagger
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'
swagger_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': 'User Management API'})

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    app.secret_key = os.urandom(24)  # Required for session management

    # CORS(app)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    db.init_app(app)
    ma.init_app(app)

    # Mail
    mail.init_app(app)
    
    # Initialize OAuth with the app
    oauth.init_app(app)
    init_oauth(app)  # Set up OAuth clients and routes

    return app

def blueprint_config(app):
    app.register_blueprint(user_routes.user_bp)
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)
    app.register_blueprint(user_details_bp)
    app.register_blueprint(user_subscription_bp)
    app.register_blueprint(reference_calendar_routes.reference_calendar_bp)
    app.register_blueprint(user_calendar_bp)
    app.register_blueprint(vision_board_bp)
    app.register_blueprint(content_item_bp)
    app.register_blueprint(questionnaire_bp)

app = create_app()
blueprint_config(app)

# Now define the Google OAuth routes directly in app.py
@app.route('/login/google')
def google_login():
    nonce = os.urandom(16).hex()
    session['nonce'] = nonce  # Store the nonce in the session
    redirect_uri = url_for('google_auth_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri, nonce=nonce)

@app.route('/login/google/callback')
def google_auth_callback():
    token = oauth.google.authorize_access_token()

    # Retrieve the nonce from the session
    nonce = session.pop('nonce', None)
    if nonce is None:
        return "Nonce is missing from the session.", 400

    # Parse the ID token and verify the nonce
    user_info = oauth.google.parse_id_token(token, nonce=nonce)

    # Handle user information and session management here
    validated_user = {
        'email': user_info.get('email'),
        'first_name': user_info.get('given_name', ''),  # Use .get() to avoid KeyError
        'last_name': user_info.get('family_name', ''),  # Use .get() to avoid KeyError
        'profile_picture': user_info.get('picture', '')  # Use .get() to avoid KeyError
    }

    # Check if the user exists in the database
    user = db.session.query(User).filter_by(email=validated_user['email']).first()
    
    if user is None:
        # If the user doesn't exist, create a new user record
        user = User(
            email=validated_user['email'],
            first_name=validated_user['first_name'],
            last_name=validated_user['last_name'],
            profile_picture=validated_user['profile_picture'],
            is_google_login=True  # Mark this user as a Google login user
        )
        db.session.add(user)
        db.session.commit()

        # Prepare the email message
        msg = Message(
            subject='Welcome to The Melanated Sanctuary!',
            recipients=[user.email],
            sender='themelanatedsanctuary@gmail.com'
        )

        # Render the email body using Jinja2 templates
        msg.body = render_template('email/welcome.txt', username=user.email, firstname=user.first_name, lastname = user.last_name)  # Plain text
        msg.html = render_template('email/welcome.html', username=user.email, firstname=user.first_name, lastname = user.last_name)  # HTML

        # Send the email
        mail.send(msg)

    # Generate a JWT token for the user
    jwt_token = encode_token(user.id, user.is_admin)

    # Store the user information in the session
    session['user_id'] = user.id
    session['user_name'] = user.first_name

    # Redirect to the frontend dashboard with the token as a query parameter
    return redirect(url_for('dashboard', token=jwt_token))

@app.route('/dashboard')
def dashboard():
    token = request.args.get('token')
    if not token:
        return redirect(url_for('index'))  # If no token, redirect to the index or login page
    
    # Optionally, validate or refresh the token here

    return f"Welcome, {session['user_name']}! This is your dashboard. Your token is: {token}"


if __name__ == '__main__':
    with app.app_context():
        try:
            from models.role import Role
            from models.user import User
            from models.user_details import UserDetails
            from models.user_subscription import UserSubscription
            from models.reference_calendar import ReferenceCalendar
            from models.user_calendar import UserCalendar
            from models.content_item import ContentItem
            from models.vision_board import VisionBoard
            from models.user_vision_board import UserVisionBoard

            # Logging SQLAlchemy engine
            # logging.basicConfig()
            # logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

            # Drop all tables and recreate them
            # db.drop_all()
            # db.session.commit()
            db.create_all()
            db.session.commit()
            print("Tables created successfully")

            # Print all registered routes
            print("\nRegistered Routes:")
            for rule in app.url_map.iter_rules():
                print(f"{rule.endpoint}: {rule.rule}")
            print()

        except Exception as e:
            print(f"An error occurred: {e}")

    app.run(debug=True, host="0.0.0.0")

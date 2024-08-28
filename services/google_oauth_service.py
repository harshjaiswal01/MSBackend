from database import db
from models.user import User
from utils.util import encode_token
from authlib.integrations.flask_client import OAuth
from flask import url_for, session

oauth = OAuth()

def get_google_login_url():
    google = oauth.create_client('google')
    redirect_uri = url_for('google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

def handle_google_callback():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)

    user = db.session.query(User).filter_by(email=user_info['email']).first()

    if not user:
        user = User(
            email=user_info['email'],
            first_name=user_info['given_name'],
            last_name=user_info['family_name'],
            profile_picture=user_info.get('picture'),
            is_google_login=True
        )
        db.session.add(user)
        db.session.commit()

    token = encode_token(user.id, user.is_admin)
    return token

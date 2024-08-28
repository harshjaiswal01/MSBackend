# from flask import session, redirect, url_for
# from authlib.integrations.flask_client import OAuth

# # Initialize OAuth object
# oauth = OAuth()

# def configure_oauth(app):
#     # Initialize OAuth with the app
#     oauth.init_app(app)
    
#     # Register Google OAuth client
#     oauth.register(
#         name='google',
#         client_id=app.config['GOOGLE_CLIENT_ID'],
#         client_secret=app.config['GOOGLE_CLIENT_SECRET'],
#         access_token_url='https://accounts.google.com/o/oauth2/token',
#         authorize_url='https://accounts.google.com/o/oauth2/auth',
#         api_base_url='https://www.googleapis.com/oauth2/v2/',
#         client_kwargs={'scope': 'openid profile email'},
#     )

# # Google OAuth callback route
# def google_auth_callback():
#     token = oauth.google.authorize_access_token()
#     user_info = oauth.google.parse_id_token(token)
#     session['user'] = user_info
#     return redirect(url_for('index'))

# def init_oauth(app):
#     configure_oauth(app)
#     app.add_url_rule('/login/google/callback', 'google_auth_callback', google_auth_callback)


from authlib.integrations.flask_client import OAuth

# Initialize OAuth object
oauth = OAuth()

def configure_oauth(app):
    # Initialize OAuth with the app
    oauth.init_app(app)

    # Register Google OAuth client
    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        access_token_url='https://accounts.google.com/o/oauth2/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        api_base_url='https://www.googleapis.com/oauth2/v2/',
        client_kwargs={'scope': 'openid profile email'},
        jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
    )

def init_oauth(app):
    configure_oauth(app)

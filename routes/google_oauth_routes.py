from flask import Blueprint
from controllers import google_oauth_controller

google_bp = Blueprint('google_bp', __name__)

google_bp.route('/login/google', methods=['GET'])(google_oauth_controller.google_login)
google_bp.route('/login/google/callback', methods=['GET'])(google_oauth_controller.google_callback)

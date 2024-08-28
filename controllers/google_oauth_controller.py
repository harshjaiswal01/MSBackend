from flask import redirect, jsonify, request
from services import google_oauth_service

def google_login():
    redirect_uri = google_oauth_service.get_google_login_url()
    return redirect(redirect_uri)

def google_callback():
    token, error = google_oauth_service.handle_google_callback()
    if error:
        return jsonify(error), 401
    return jsonify({"token": token}), 200

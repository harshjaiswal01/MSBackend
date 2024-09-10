from flask import request, jsonify
from services.user_subscription_service import create_or_update_subscription, get_subscription
from utils.util import token_required

@token_required
def update_subscription(user_id):
    print(user_id)
    subscription_data = request.json
    subscription, error = create_or_update_subscription(user_id, subscription_data)
    if error:
        return jsonify(error), 400
    return jsonify(subscription), 200

@token_required
def get_subscription_status(user_id):
    subscription, error = get_subscription(user_id)
    if error:
        return jsonify(error), 404
    return jsonify(subscription), 200
from flask import request, jsonify
from services.user_subscription_service import create_or_update_subscription
from utils.util import token_required

@token_required
def update_subscription(user_id):
    subscription_data = request.json
    subscription, error = create_or_update_subscription(user_id, subscription_data)
    if error:
        return jsonify(error), 400
    return jsonify(subscription), 200

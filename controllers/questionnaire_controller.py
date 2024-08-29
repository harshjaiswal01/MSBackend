from flask import request, jsonify
from services import questionnaire_service
from utils.util import token_required

@token_required
def get_available_boards(user_id):
    boards, error = questionnaire_service.get_available_boards(user_id)
    if error:
        return jsonify(error), 400
    return jsonify(boards), 200

@token_required
def submit_questionnaire(user_id):
    data = request.json
    response = questionnaire_service.submit_questionnaire(user_id, data['selected_board_ids'])
    return jsonify(response), 201

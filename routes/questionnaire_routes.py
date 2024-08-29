from flask import Blueprint
from controllers import questionnaire_controller

questionnaire_bp = Blueprint('questionnaire_bp', __name__)

questionnaire_bp.route('/questionnaire', methods=['GET'])(questionnaire_controller.get_available_boards)
questionnaire_bp.route('/questionnaire/submit', methods=['POST'])(questionnaire_controller.submit_questionnaire)

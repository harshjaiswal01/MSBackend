from database import db
from models.vision_board import VisionBoard
from models.user_vision_board import UserVisionBoard
from models.schemas.vision_board_schema import vision_boards_schema

def get_available_boards(user_id):
    boards = db.session.query(VisionBoard).filter(
        (VisionBoard.created_by == None) | (VisionBoard.created_by == user_id)
    ).all()
    return vision_boards_schema.dump(boards), None


def submit_questionnaire(user_id, selected_board_ids):
    # First, clear existing user vision boards
    db.session.query(UserVisionBoard).filter_by(user_id=user_id).delete()

    # Then, add new user vision boards
    for board_id in selected_board_ids:
        user_board = UserVisionBoard(user_id=user_id, vision_board_id=board_id)
        db.session.add(user_board)

    db.session.commit()
    return {"message": "Questionnaire submitted successfully"}

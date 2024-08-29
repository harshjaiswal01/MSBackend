from database import db
from models.vision_board import VisionBoard
from models.user_vision_board import UserVisionBoard
from models.content_item import ContentItem
from models.schemas.vision_board_schema import vision_board_schema, vision_boards_schema
from models.schemas.content_item_schema import content_item_schema, content_items_schema

def create_vision_board(data, user_id=None):
    is_custom = user_id is not None
    vision_board = VisionBoard(name=data['name'], is_custom=is_custom, created_by=user_id)
    db.session.add(vision_board)
    db.session.commit()
    return vision_board_schema.dump(vision_board), None

def get_vision_board(vision_board_id):
    vision_board = db.session.query(VisionBoard).filter_by(id=vision_board_id).first()
    if not vision_board:
        return None, {"error": "Vision board not found"}
    return vision_board_schema.dump(vision_board), None

def update_vision_board(vision_board_id, data):
    vision_board = db.session.query(VisionBoard).filter_by(id=vision_board_id).first()
    if not vision_board:
        return None, {"error": "Vision board not found"}

    vision_board.name = data.get('name', vision_board.name)
    db.session.commit()
    return vision_board_schema.dump(vision_board), None

def delete_vision_board(vision_board_id):
    vision_board = db.session.query(VisionBoard).filter_by(id=vision_board_id).first()
    if not vision_board:
        return None, {"error": "Vision board not found"}

    db.session.delete(vision_board)
    db.session.commit()
    return {"message": "Vision board deleted successfully"}

def get_user_vision_boards(user_id):
    user_boards = db.session.query(UserVisionBoard).filter_by(user_id=user_id).all()
    return vision_boards_schema.dump([board.vision_board for board in user_boards]), None

def add_user_vision_board(user_id, vision_board_id):
    user_board = UserVisionBoard(user_id=user_id, vision_board_id=vision_board_id)
    db.session.add(user_board)
    db.session.commit()
    return vision_board_schema.dump(user_board.vision_board), None

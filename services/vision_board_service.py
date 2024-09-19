from database import db
from models.vision_board import VisionBoard
from models.user_vision_board import UserVisionBoard
from models.user import User
from models.schemas.vision_board_schema import vision_board_schema, vision_boards_schema

def create_vision_board(data, user_id=None):
    # Fetch the user from the database to check if they are an admin
    user = db.session.query(User).filter_by(id=user_id).first()

    if not user:
        return None, {"error": "User not found"}

    # Check if the user is an admin based on the 'is_admin' flag or their role
    is_admin = user.is_admin or (user.role and user.role.name == 'admin')

    # If the user is an admin, the board is admin-created, otherwise it's user-created
    is_custom = not is_admin

    # Create the vision board
    vision_board = VisionBoard(
        name=data['name'], 
        is_custom=is_custom, 
        created_by=user_id if not is_admin else None,  # Admin-created boards have no user assigned
        description=data.get('description', None),
        pic_url=data.get('pic_url', None)
    )
    db.session.add(vision_board)
    db.session.commit()

    # Automatically subscribe the user to their own vision board if they created it (non-admin)
    if not is_admin:
        user_subscription = UserVisionBoard(user_id=user_id, vision_board_id=vision_board.id)
        db.session.add(user_subscription)
        db.session.commit()

    return vision_board_schema.dump(vision_board), None

def get_vision_board(vision_board_id):
    # Retrieve a single vision board by its ID
    vision_board = db.session.query(VisionBoard).filter_by(id=vision_board_id).first()
    if not vision_board:
        return None, {"error": "Vision board not found"}
    return vision_board_schema.dump(vision_board), None

def update_vision_board(vision_board_id, data):
    # Retrieve the vision board and update its information
    vision_board = db.session.query(VisionBoard).filter_by(id=vision_board_id).first()
    if not vision_board:
        return None, {"error": "Vision board not found"}

    vision_board.name = data.get('name', vision_board.name)
    vision_board.description = data.get('description', vision_board.description)
    vision_board.pic_url = data.get('pic_url', vision_board.pic_url)
    db.session.commit()
    return vision_board_schema.dump(vision_board), None

def delete_user_vision_board(user_id, vision_board_id):
    # Check if the board was created by the user and is custom
    vision_board = db.session.query(VisionBoard).filter_by(id=vision_board_id, created_by=user_id, is_custom=True).first()
    if not vision_board:
        return None, {"error": "Cannot delete admin-created or other users' boards"}

    # Delete the user's custom board
    db.session.delete(vision_board)
    db.session.commit()
    return {"message": "Vision board deleted successfully"}, None

def get_all_vision_boards_for_user(user_id):
    # Get user-created vision boards
    user_boards = db.session.query(UserVisionBoard).filter_by(user_id=user_id).all()

    # Get all admin-created boards the user has not unsubscribed from
    unsubscribed_board_ids = [ub.vision_board_id for ub in user_boards]
    admin_boards = db.session.query(VisionBoard).filter(
        VisionBoard.is_custom.is_(False),
        VisionBoard.id.notin_(unsubscribed_board_ids)
    ).all()

    # Combine the user-subscribed and admin-created boards
    subscribed_boards = [ub.vision_board for ub in user_boards] + admin_boards
    return vision_boards_schema.dump(subscribed_boards), None

def get_subscribed_vision_boards(user_id):
    # Get the list of IDs where the user is unsubscribed
    unsubscribed_board_ids = db.session.query(UserVisionBoard.vision_board_id).filter_by(user_id=user_id, is_subscribed=False).all()

    # Convert unsubscribed IDs into a flat list
    unsubscribed_board_ids = [id for (id,) in unsubscribed_board_ids]

    # Fetch all admin-created vision boards (is_custom=False) that the user hasn't unsubscribed from
    admin_boards = db.session.query(VisionBoard).filter(
        VisionBoard.is_custom.is_(False),
        ~VisionBoard.id.in_(unsubscribed_board_ids)  # Exclude unsubscribed admin boards
    ).all()

    # Fetch all user-created boards where the user is still subscribed (is_subscribed=True)
    user_subscribed_boards = db.session.query(UserVisionBoard).filter_by(user_id=user_id, is_subscribed=True).all()

    # Combine the vision boards: admin-created and user-subscribed
    subscribed_boards = [ub.vision_board for ub in user_subscribed_boards] + admin_boards

    return vision_boards_schema.dump(subscribed_boards), None


def add_user_vision_board(user_id, vision_board_id):
    # Check if a record already exists for this user and vision board
    subscription = db.session.query(UserVisionBoard).filter_by(user_id=user_id, vision_board_id=vision_board_id).first()

    if subscription:
        # If the record exists but is marked as unsubscribed, update it to subscribed
        subscription.is_subscribed = True
    else:
        # If no record exists, create a new subscription entry
        subscription = UserVisionBoard(user_id=user_id, vision_board_id=vision_board_id, is_subscribed=True)
        db.session.add(subscription)
    
    db.session.commit()
    return vision_board_schema.dump(subscription.vision_board), None

def unsubscribe_from_vision_board(user_id, vision_board_id):
    # Check if the board is admin-created
    vision_board = db.session.query(VisionBoard).filter_by(id=vision_board_id, is_custom=False).first()

    if not vision_board:
        return None, {"error": "Vision board not found or cannot unsubscribe from user-created boards"}

    # Check if a subscription exists
    subscription = db.session.query(UserVisionBoard).filter_by(user_id=user_id, vision_board_id=vision_board_id).first()

    if subscription:
        # If a subscription exists, mark it as unsubscribed
        subscription.is_subscribed = False
    else:
        # If no subscription exists, create a new one with is_subscribed=False
        subscription = UserVisionBoard(user_id=user_id, vision_board_id=vision_board_id, is_subscribed=False)
        db.session.add(subscription)

    db.session.commit()
    return vision_board_schema.dump(subscription.vision_board), None

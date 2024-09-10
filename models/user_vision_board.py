from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

class UserVisionBoard(Base):
    __tablename__ = 'user_vision_boards'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vision_board_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('vision_boards.id'), nullable=False)
    is_subscribed: Mapped[bool] = mapped_column(db.Boolean, default=True)  # Field to track subscription status

    user: Mapped["User"] = db.relationship("User", back_populates="user_vision_boards")
    vision_board: Mapped["VisionBoard"] = db.relationship("VisionBoard", back_populates="user_vision_boards")

    def __init__(self, user_id, vision_board_id, is_subscribed=True):
        self.user_id = user_id
        self.vision_board_id = vision_board_id
        self.is_subscribed = is_subscribed

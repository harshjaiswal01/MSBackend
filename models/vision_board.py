from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional

class VisionBoard(Base):
    __tablename__ = 'vision_boards'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    is_custom: Mapped[bool] = mapped_column(db.Boolean, default=False)
    description: Mapped[str] = mapped_column(db.String(255), nullable=False)
    created_by: Mapped[Optional[int]] = mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    user: Mapped[Optional["User"]] = relationship("User", back_populates="vision_boards")  # Explicit relationship to User
    content_items: Mapped[List["ContentItem"]] = db.relationship("ContentItem", back_populates="vision_board", cascade="all, delete-orphan")
    user_vision_boards: Mapped[List["UserVisionBoard"]] = db.relationship("UserVisionBoard", back_populates="vision_board", cascade="all, delete-orphan")

    def __init__(self, name, is_custom=False, created_by=None, description = None):
        self.name = name
        self.is_custom = is_custom
        self.created_by = created_by
        self.description = description

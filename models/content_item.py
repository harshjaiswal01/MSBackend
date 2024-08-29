from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class ContentItem(Base):
    __tablename__ = 'content_items'

    id: Mapped[int] = mapped_column(primary_key=True)
    vision_board_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('vision_boards.id'), nullable=False)
    content_url: Mapped[str] = mapped_column(db.String(300), nullable=False)
    title: Mapped[str] = mapped_column(db.String(200), nullable=False)
    description: Mapped[str] = mapped_column(db.String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(db.DateTime, nullable=True)
    main_image_url: Mapped[str] = mapped_column(db.String(300), nullable=True)
    content_type: Mapped[str] = mapped_column(db.String(50), nullable=False)

    vision_board: Mapped["VisionBoard"] = db.relationship("VisionBoard", back_populates="content_items")

    def __init__(self, vision_board_id, content_url, title, description, created_at, main_image_url, content_type):
        self.vision_board_id = vision_board_id
        self.content_url = content_url
        self.title = title
        self.description = description
        self.created_at = created_at
        self.main_image_url = main_image_url
        self.content_type = content_type

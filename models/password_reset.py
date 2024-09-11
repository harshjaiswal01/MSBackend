from database import db, Base
from sqlalchemy.orm import Mapped
from datetime import datetime, timedelta
from typing import Optional

class PasswordReset(Base):
    __tablename__ = 'password_resets'
    
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    user_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reset_code: Mapped[int] = db.Column(db.Integer, nullable=False)
    created_at: Mapped[datetime] = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    user: Mapped[Optional["User"]] = db.relationship("User", back_populates="password_resets")

    @staticmethod
    def is_code_valid(reset_record: "PasswordReset") -> bool:
        expiration_time = reset_record.created_at + timedelta(minutes=5)
        return datetime.utcnow() <= expiration_time

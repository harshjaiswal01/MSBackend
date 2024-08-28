from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy import Boolean, Date, Integer, String
from database import db, Base

class UserDetails(Base):
    __tablename__ = 'user_details'
    
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    sex: Mapped[str] = db.Column(db.String(10), nullable=False)
    pronouns: Mapped[str] = db.Column(db.String(20), nullable=False)
    due_date: Mapped[Optional[str]] = db.Column(db.Date, nullable=True)
    first_pregnancy: Mapped[bool] = db.Column(db.Boolean, default=False)
    phone_number: Mapped[Optional[str]] = db.Column(db.String(20), nullable=True)  # New field
    can_receive_text: Mapped[Optional[bool]] = db.Column(db.Boolean, nullable=True)  # New field
    user_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('users.id'))

    user: Mapped["User"] = db.relationship("User", back_populates="details")

    def __init__(self, sex, pronouns, due_date=None, first_pregnancy=False, phone_number=None, can_receive_text=None):
        self.sex = sex
        self.pronouns = pronouns
        self.due_date = due_date
        self.first_pregnancy = first_pregnancy
        self.phone_number = phone_number  # Initialize the new field
        self.can_receive_text = can_receive_text  # Initialize the new field

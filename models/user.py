from database import db, Base
from sqlalchemy.orm import Mapped
from typing import Optional

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    email: Mapped[str] = db.Column(db.String(100), unique=True, nullable=False)
    password: Mapped[Optional[str]] = db.Column(db.String(200), nullable=True)  # Nullable because Google login users won't have a password
    first_name: Mapped[str] = db.Column(db.String(50), nullable=False)
    last_name: Mapped[str] = db.Column(db.String(50), nullable=False)
    profile_picture: Mapped[Optional[str]] = db.Column(db.String(200), nullable=True)  # Profile picture URL from Google
    is_google_login: Mapped[bool] = db.Column(db.Boolean, default=False)
    is_admin: Mapped[bool] = db.Column(db.Boolean, default=False)
    role_id: Mapped[Optional[int]] = db.Column(db.Integer, db.ForeignKey('roles.id'))

    role: Mapped[Optional["Role"]] = db.relationship("Role", back_populates="users")
    details: Mapped[Optional["UserDetails"]] = db.relationship("UserDetails", back_populates="user", uselist=False)
    subscriptions: Mapped["UserSubscription"] = db.relationship("UserSubscription", uselist=False, back_populates="user")
    calendar_entries = db.relationship("UserCalendar", back_populates="user", cascade="all, delete-orphan")  # One-to-many relationship with UserCalendar


    def __init__(self, email, first_name, last_name, password=None, profile_picture=None, is_google_login=False):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.profile_picture = profile_picture
        self.is_google_login = is_google_login

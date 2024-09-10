from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from database import db, Base
from typing import Optional


class UserCalendar(Base):
    __tablename__ = 'user_calendar'

    id: Mapped[int] = Column(Integer, primary_key=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey('users.id'), nullable=False)
    event_date: Mapped[Date] = Column(Date, nullable=False)
    title: Mapped[str] = Column(String(255), nullable=False)  # New title field
    description: Mapped[str] = Column(String(255), nullable=False)
    location: Mapped[Optional[str]] = Column(String(255), nullable=True)  # New location field

    user = db.relationship("User", back_populates="calendar_entries")

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from database import db, Base

class UserCalendar(Base):
    __tablename__ = 'user_calendar'

    id: Mapped[int] = Column(Integer, primary_key=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey('users.id'), nullable=False)
    event_date: Mapped[Date] = Column(Date, nullable=False)
    description: Mapped[str] = Column(String(255), nullable=False)

    user = db.relationship("User", back_populates="calendar_entries")

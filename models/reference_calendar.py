from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column

class ReferenceCalendar(Base):
    __tablename__ = 'reference_calendar'
    
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    day: Mapped[int] = mapped_column(db.Integer, nullable=False)
    activity: Mapped[str] = mapped_column(db.String(255), nullable=False)
    
    def __init__(self, day, activity):
        self.day = day
        self.activity = activity

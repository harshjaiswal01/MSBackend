from database import db

class ReferenceCalendar(db.Model):
    __tablename__ = 'reference_calendar'
    
    id = db.Column(db.Integer, primary_key=True)
    day_of_pregnancy = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)  # Make sure this line exists
    
    def __init__(self, day_of_pregnancy, description):
        self.day_of_pregnancy = day_of_pregnancy
        self.description = description

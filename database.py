from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass

db = SQLAlchemy(model_class=Base)  # Instantiating our db with the custom Base class

def create_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Create all tables

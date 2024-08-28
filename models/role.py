from database import db, Base
from sqlalchemy.orm import Mapped
from typing import List

class Role(Base):
    __tablename__ = 'roles'
    
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(50), unique=True, nullable=False)
    
    users: Mapped[List["User"]] = db.relationship("User", back_populates="role")

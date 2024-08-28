from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column

class UserSubscription(Base):
    __tablename__ = 'user_subscriptions'
    
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    newsletter_subscription: Mapped[bool] = mapped_column(db.Boolean, default=False)
    text_subscription: Mapped[bool] = mapped_column(db.Boolean, default=False)
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('users.id'))

    user: Mapped["User"] = db.relationship("User", back_populates="subscriptions")

    def __init__(self, newsletter_subscription=False, text_subscription=False):
        self.newsletter_subscription = newsletter_subscription
        self.text_subscription = text_subscription

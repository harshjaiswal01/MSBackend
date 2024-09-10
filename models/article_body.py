from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column

class ArticleBody(Base):
    __tablename__ = 'article_bodies'

    id: Mapped[int] = mapped_column(primary_key=True)
    content_item_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('content_items.id'), nullable=False)  # Correct table name reference
    body: Mapped[str] = mapped_column(db.Text, nullable=False)  # Store the article body

    content_item: Mapped["ContentItem"] = db.relationship("ContentItem", back_populates="article_body")

from db import db
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Boolean, DateTime, func

class Category(db.Model):

    __tablename__ = "categories"

    id_category: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    def to_json(self) -> dict[str, str]:
        return {
            'id_category': self.id_category,
            'name': self.name,
            'description': self.description,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }
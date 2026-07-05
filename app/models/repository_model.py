from db import db
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, DateTime, func

class Repository(db.Model):

    __tablename__ = "repositories"

    id_repository: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    def to_json(self):
        return {
            'id_repository': self.id_repository,
            'name': self.name,
            'location': self.location,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }

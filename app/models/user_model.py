from db import db
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String, Text, Boolean, DateTime, func, ForeignKey

class User(db.Model):

    __tablename__ = "users"

    id_user: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    id_role: Mapped[int] = mapped_column(ForeignKey('roles.id_role'), nullable=False)

    def to_json(self):
        return {
            'id_user': self.id_user,
            'name': self.name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
            'id_role': self.id_role
        }

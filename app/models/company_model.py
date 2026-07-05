from db import db
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, DateTime, func

class Company(db.Model):

    __tablename__ = "companies"

    id_company: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    ruc: Mapped[str] = mapped_column(String(11), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    def to_json(self):
        return {
            'id_company': self.id_company,
            'name': self.name,
            'ruc': self.ruc,
            'address': self.address,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }
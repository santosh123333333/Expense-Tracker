from sqlalchemy import String, Integer,DateTime, Float,Date
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Expense(Base):
    __tablename__="expenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    show: Mapped[bool] = mapped_column(default=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    model_config = {
        "from_attributes": True  # allows pydantic to read SqlAlchemy models and convert them to pydantic models
    }
    



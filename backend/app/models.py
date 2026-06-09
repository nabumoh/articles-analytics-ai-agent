from datetime import datetime
from sqlalchemy import String, Text, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    source: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    reading_time_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    url: Mapped[str] = mapped_column(String(1000), unique=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

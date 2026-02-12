from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
import uuid

from app.db.database import Base

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True, nullable=False)
    location = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    address = Column(String, nullable=True)
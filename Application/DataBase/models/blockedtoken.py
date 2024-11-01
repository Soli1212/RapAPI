from .Base.base import Base
from sqlalchemy import (Column, String, Integer)
class BlockedToken(Base):
    __tablename__ = "blockedtoken"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    token = Column(String, nullable=False, unique=True, index=True)

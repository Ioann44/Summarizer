from sqlalchemy import DateTime, Column, Integer, String, func, Boolean, SmallInteger

from ..common.base_class import Base


class Text(Base):
    __tablename__ = "texts"

    hash = Column(String(64), primary_key=True)
    preview = Column(String(128), nullable=False)
    sourceFile = Column(String(36), nullable=False, unique=True)
    vectFile = Column(String(32))
    primFile = Column(String(32))
    lastModDate = Column(DateTime(timezone=True), server_default=func.now())


class PollRes(Base):
    __tablename__ = "polls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    success = Column(Boolean(), nullable=False)
    percents = Column(SmallInteger(), nullable=False)

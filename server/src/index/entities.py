from sqlalchemy import DateTime, Column, String, func

from ..common.base_class import Base


class Text(Base):
    __tablename__ = "texts"

    hash = Column(String(64), primary_key=True)
    preview = Column(String(128))
    sourceFile = Column(String(36), unique=True)
    vectFile = Column(String(32), unique=True, nullable=True)
    primFile = Column(String(32), unique=True, nullable=True)
    lastModDate = Column(DateTime(timezone=True), server_default=func.now())

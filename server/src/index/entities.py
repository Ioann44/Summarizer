from sqlalchemy import DateTime, Column, String, func

from ..common.base_class import Base


class Text(Base):
    __tablename__ = "texts"

    hash = Column(String(64), primary_key=True)
    preview = Column(String(128), nullable=False)
    sourceFile = Column(String(36), nullable=False, unique=True)
    vectFile = Column(String(32))
    primFile = Column(String(32))
    lastModDate = Column(DateTime(timezone=True), server_default=func.now())

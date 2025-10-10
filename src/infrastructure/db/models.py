from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Index
from sqlalchemy.sql import func
from src.infrastructure.db.database import Base


class ProductModel(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    brand = Column(String)
    category = Column(String)
    size = Column(String)
    color = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    description = Column(String)

class ChatMemoryModel(Base):
    __tablename__ = "chat_memory"

    id = Column(Integer, primary_key=True, autoincrement=True, doc="ID único del mensaje")
    session_id = Column(String(100), index=True, nullable=False, doc="ID de la sesión de chat")
    role = Column(String(20), nullable=False, doc="Rol del mensaje: 'user' o 'assistant'")
    message = Column(Text, nullable=False, doc="Contenido del mensaje")
    timestamp = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), doc="Fecha y hora del mensaje (UTC)")

    __table_args__ = (
        Index('idx_chat_memory_session_id', 'session_id'),
    )
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class ProductDTO(BaseModel):
    id: Optional[int] = None
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("El precio debe ser mayor a 0.")
        return v

    @validator('stock')
    def stock_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError("El stock no puede ser negativo.")
        return v

    class Config:
        orm_mode = True  # CLAVE para FastAPI+SQLAlchemy

class ChatMessageRequestDTO(BaseModel):
    """DTO para recibir mensajes del usuario"""
    session_id: str
    message: str

    @validator('message')
    def message_not_empty(cls, v):
        """Valida que el mensaje no esté vacío"""
        if not v or v.strip() == "":
            raise ValueError("El mensaje no puede estar vacío.")
        return v

    @validator('session_id')
    def session_id_not_empty(cls, v):
        """Valida que session_id no esté vacío"""
        if not v or v.strip() == "":
            raise ValueError("El session_id no puede estar vacío.")
        return v
    

class ChatMessageResponseDTO(BaseModel):
    """DTO para enviar respuestas del chat"""
    session_id: str
    user_message: str
    assistant_message: str
    timestamp: datetime  # Este campo es obligatorio

    @classmethod
    def from_entities(cls, session_id, user_message, assistant_message, timestamp=None):
        # Soporte para construir desde entidades y rellenar el timestamp si falta
        if timestamp is None:
            timestamp = datetime.utcnow()
        return cls(
            session_id=session_id,
            user_message=user_message,
            assistant_message=assistant_message,
            timestamp=timestamp
        )


class ChatHistoryDTO(BaseModel):
    """DTO para mostrar historial de chat"""
    id: int
    role: str
    message: str
    timestamp: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_entity(cls, entity):
        # Si tu entidad tiene 'sender' en lugar de 'role', lo mapea correctamente
        return cls(
            id=entity.id,
            role=getattr(entity, "role", getattr(entity, "sender", "")),
            message=entity.message,
            timestamp=entity.timestamp,
        )
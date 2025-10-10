from src.domain.repositories import IChatRepository
from src.domain.entities import ChatMessage
from src.infrastructure.db.models import ChatMemoryModel
from sqlalchemy.orm import Session

class SQLChatRepository(IChatRepository):
    def __init__(self, db: Session):
        self.db = db

    def save_message(self, message: ChatMessage):
        model = self._entity_to_model(message)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)

    def get_session_history(self, session_id: str, limit: int = 50):
        models = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .order_by(ChatMemoryModel.timestamp.desc())
            .limit(limit)
            .all()
        )
        models.reverse()
        return [self._model_to_entity(m) for m in models]

    def delete_session_history(self, session_id: str):
        self.db.query(ChatMemoryModel).filter(ChatMemoryModel.session_id == session_id).delete()
        self.db.commit()

    def get_recent_messages(self, session_id: str, n: int):
        models = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .order_by(ChatMemoryModel.timestamp.desc())
            .limit(n)
            .all()
        )
        models.reverse()
        return [self._model_to_entity(m) for m in models]

    # Métodos auxiliares
    def _model_to_entity(self, model):
        if not model:
            return None
        return ChatMessage(
            id=model.id,
            session_id=model.session_id,
            role=model.role,         # <-- ¡Aquí!
            message=model.message,
            timestamp=model.timestamp,
        )

    def _entity_to_model(self, entity):
        return ChatMemoryModel(
            id=entity.id,
            session_id=entity.session_id,
            role=entity.role,        # <-- ¡Aquí!
            message=entity.message,
            timestamp=entity.timestamp,
        )
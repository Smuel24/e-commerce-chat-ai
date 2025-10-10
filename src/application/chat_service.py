from ..domain.repositories import IProductRepository, IChatRepository
from ..domain.entities import ChatMessage, ChatContext
from ..domain.exceptions import ChatServiceError
from .dtos import ChatMessageRequestDTO, ChatMessageResponseDTO, ChatHistoryDTO
from datetime import datetime
from typing import List, Optional

class ChatService:
    """
    Servicio de chat con IA para procesamiento de mensajes y gestión de historial.
    """

    def __init__(self, product_repository: IProductRepository, chat_repository: IChatRepository, ai_service):
        self.product_repository = product_repository
        self.chat_repository = chat_repository
        self.ai_service = ai_service

    async def process_message(self, request: ChatMessageRequestDTO) -> ChatMessageResponseDTO:
        """
        Procesa el mensaje del usuario, llama a la IA y guarda historial.
        """
        try:
            # 1. Obtener todos los productos
            products = self.product_repository.get_all()

            # 2. Obtener historial reciente (últimos 6 mensajes)
            recent_messages = self.chat_repository.get_recent_messages(request.session_id, 6)

            # 3. Crear ChatContext
            chat_context = ChatContext(messages=recent_messages)

            # 4. Llamar a la IA (simulado aquí con await ai_service.generate_response)
            ai_reply = await self.ai_service.generate_response(
                user_message=request.message,
                products=products,
                context=chat_context
            )

            # 5. Guardar mensaje del usuario
            user_msg = ChatMessage(
                id=None,
                session_id=request.session_id,
                role='user',
                message=request.message,
                timestamp=datetime.utcnow()
            )
            saved_user_msg = self.chat_repository.save_message(user_msg)

            # 6. Guardar respuesta de asistente
            assistant_msg = ChatMessage(
                id=None,
                session_id=request.session_id,
                role='assistant',
                message=ai_reply,
                timestamp=datetime.utcnow()
            )
            saved_assistant_msg = self.chat_repository.save_message(assistant_msg)

            # 7. Retornar DTO de respuesta
            return ChatMessageResponseDTO(
                session_id=request.session_id,
                user_message=saved_user_msg.message,
                assistant_message=saved_assistant_msg.message,
                timestamp=saved_assistant_msg.timestamp
            )

        except Exception as e:
            raise ChatServiceError(f"Error al procesar el mensaje: {str(e)}")

    def get_session_history(self, session_id: str, limit: Optional[int] = None) -> List[ChatHistoryDTO]:
        """
        Obtiene el historial de una sesión.
        """
        history = self.chat_repository.get_session_history(session_id, limit)
        return [
            ChatHistoryDTO(
                id=msg.id,
                role=msg.role,
                message=msg.message,
                timestamp=msg.timestamp
            ) for msg in history
        ]

    def clear_session_history(self, session_id: str) -> int:
        """
        Elimina todo el historial de una sesión.
        Retorna la cantidad de mensajes eliminados.
        """
        return self.chat_repository.delete_session_history(session_id)
from dotenv import load_dotenv
load_dotenv()

import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime

from src.infrastructure.db.database import init_db, get_db
from src.infrastructure.repositorie.product_repository import SQLProductRepository
from src.infrastructure.repositorie.chat_repository import SQLChatRepository
from src.infrastructure.llm_providers.gemini_service import GeminiService

from src.application.dtos import ProductDTO, ChatMessageRequestDTO, ChatMessageResponseDTO, ChatHistoryDTO

print("ANTES DE CREAR APP")
app = FastAPI(
    title="E-commerce Shoes Chat API",
    description="API para e-commerce con chat AI y catálogo de productos de zapatos",
    version="1.0.0"
)
print("APP FASTAPI CREADA")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    print("STARTUP: Antes de init_db")
    init_db()
    print("STARTUP: Después de init_db")

@app.get("/", tags=["Root"])
def read_root():
    print("Entrando a endpoint raíz /")
    return {
        "api": "E-commerce Shoes Chat API",
        "version": app.version,
        "description": app.description,
        "endpoints": [
            "GET /products",
            "GET /products/{product_id}",
            "POST /chat",
            "GET /chat/history/{session_id}",
            "DELETE /chat/history/{session_id}",
            "GET /health",
            "GET /test"
        ]
    }

@app.get("/test", tags=["Test"])
def test():
    print("Entrando a /test")
    return {"ok": True}

@app.get("/products", response_model=list[ProductDTO], tags=["Products"])
def get_all_products(db: Session = Depends(get_db)):
    print("Entrando a /products")
    repo = SQLProductRepository(db)
    products = repo.get_all()
    print("Productos encontrados:", products)
    return products

@app.get("/products/{product_id}", response_model=ProductDTO, tags=["Products"])
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    print(f"Entrando a /products/{product_id}")
    repo = SQLProductRepository(db)
    product = repo.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    print("Producto encontrado:", product)
    return product

@app.post("/chat", response_model=ChatMessageResponseDTO, tags=["Chat"])
async def chat(
    request: ChatMessageRequestDTO,
    db: Session = Depends(get_db)
):
    try:
        print("Entrando a /chat")
        chat_repo = SQLChatRepository(db)
        product_repo = SQLProductRepository(db)
        gemini = GeminiService()

        products = product_repo.get_all()
        context = chat_repo.get_session_history(request.session_id, limit=20)
        context_fmt = [
            {"role": m.role, "message": m.message} for m in context
        ]

        response_text = await gemini.generate_response(
            user_message=request.message,
            products=products,
            context=context_fmt
        )

        # Guarda el mensaje del usuario y de la IA en el historial
        from src.domain.entities import ChatMessage
        now = datetime.utcnow()
        user_msg = ChatMessage(
            id=None,
            session_id=request.session_id,
            role="user",
            message=request.message,
            timestamp=now
        )
        assistant_msg = ChatMessage(
            id=None,
            session_id=request.session_id,
            role="assistant",
            message=response_text,
            timestamp=now
        )
        chat_repo.save_message(user_msg)
        chat_repo.save_message(assistant_msg)

        print("Respondiendo mensaje de chat")
        return ChatMessageResponseDTO(
            session_id=request.session_id,
            user_message=request.message,
            assistant_message=response_text,
            timestamp=now  # ¡IMPORTANTE! Ahora sí lo incluyes.
        )
    except Exception as e:
        print("ERROR EN /chat", str(e))
        raise HTTPException(status_code=500, detail=f"Error en el chat: {str(e)}")

@app.get("/chat/history/{session_id}", response_model=list[ChatHistoryDTO], tags=["Chat"])
def get_chat_history(session_id: str, limit: int = 10, db: Session = Depends(get_db)):
    print(f"Entrando a /chat/history/{session_id}")
    chat_repo = SQLChatRepository(db)
    history = chat_repo.get_session_history(session_id, limit=limit)
    print("Historial encontrado:", history)
    return [ChatHistoryDTO.from_entity(m) for m in history]

@app.delete("/chat/history/{session_id}", tags=["Chat"])
def delete_chat_history(session_id: str, db: Session = Depends(get_db)):
    print(f"Entrando a DELETE /chat/history/{session_id}")
    chat_repo = SQLChatRepository(db)
    deleted = chat_repo.delete_session_history(session_id)
    print("Mensajes eliminados:", deleted)
    return {"deleted": deleted}

@app.get("/health", tags=["Health"])
def health_check():
    print("Entrando a /health")
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

logging.basicConfig(level=logging.DEBUG)
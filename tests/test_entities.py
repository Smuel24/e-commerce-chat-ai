import pytest
from pydantic import ValidationError
from datetime import datetime

# Asumiendo que tus entidades están en src.domain.entities y usan Pydantic/BaseModel
from src.domain.entities import Product, ChatMessage, ChatContext

# ----- Tests de Product -----

def test_product_validation_price_negative():
    with pytest.raises(ValidationError):
        Product(id=1, name="Zapato", brand="Nike", category="Deportivo", size="42", color="Rojo", price=-10.0, stock=5, description="Zapato rojo")

def test_product_validation_stock_negative():
    with pytest.raises(ValidationError):
        Product(id=1, name="Zapato", brand="Nike", category="Deportivo", size="42", color="Rojo", price=100.0, stock=-2, description="Zapato rojo")

def test_product_is_available_true():
    p = Product(id=1, name="Zapato", brand="Nike", category="Deportivo", size="42", color="Rojo", price=100.0, stock=2, description="Zapato rojo")
    assert p.is_available() is True

def test_product_is_available_false():
    p = Product(id=1, name="Zapato", brand="Nike", category="Deportivo", size="42", color="Rojo", price=100.0, stock=0, description="Zapato rojo")
    assert p.is_available() is False

def test_product_reduce_stock():
    p = Product(id=1, name="Zapato", brand="Nike", category="Deportivo", size="42", color="Rojo", price=100.0, stock=10, description="Zapato rojo")
    p.reduce_stock(3)
    assert p.stock == 7

def test_product_reduce_stock_not_enough():
    p = Product(id=1, name="Zapato", brand="Nike", category="Deportivo", size="42", color="Rojo", price=100.0, stock=2, description="Zapato rojo")
    with pytest.raises(ValueError):
        p.reduce_stock(3)

# ----- Tests de ChatMessage -----

def test_chat_message_validation_message_empty():
    with pytest.raises(ValidationError):
        ChatMessage(id=1, session_id="abc", role="user", message="", timestamp=datetime.utcnow())

def test_chat_message_validation_session_id_empty():
    with pytest.raises(ValidationError):
        ChatMessage(id=1, session_id="   ", role="user", message="Hola", timestamp=datetime.utcnow())

def test_chat_message_valid():
    m = ChatMessage(id=1, session_id="abc", role="user", message="Hola", timestamp=datetime.utcnow())
    assert m.session_id == "abc"
    assert m.message == "Hola"

# ----- Tests de ChatContext -----

def test_chat_context_format_for_prompt():
    # Simula una entidad ChatContext con una lista de mensajes
    messages = [
        ChatMessage(id=1, session_id="abc", role="user", message="Hola", timestamp=datetime.utcnow()),
        ChatMessage(id=2, session_id="abc", role="assistant", message="¡Hola! ¿En qué puedo ayudarte?", timestamp=datetime.utcnow()),
    ]
    context = ChatContext(messages=messages)
    prompt = context.format_for_prompt()
    assert isinstance(prompt, list)
    assert prompt[0]["role"] == "user"
    assert prompt[0]["message"] == "Hola"
    assert prompt[1]["role"] == "assistant"
    assert "puedo ayudarte" in prompt[1]["message"]
import pytest
from unittest.mock import MagicMock
from datetime import datetime

# Asumiendo que tus servicios están en src.application.services

from src.application.product_service import ProductService
from src.application.chat_service import ChatService

# ----- Fixtures y Mocks -----a

@pytest.fixture
def mock_product_repo():
    repo = MagicMock()
    return repo

@pytest.fixture
def mock_chat_repo():
    repo = MagicMock()
    return repo

@pytest.fixture
def mock_llm_service():
    service = MagicMock()
    return service

@pytest.fixture
def product_service(mock_product_repo):
    return ProductService(mock_product_repo)

@pytest.fixture
def chat_service(mock_chat_repo, mock_product_repo, mock_llm_service):
    return ChatService(mock_chat_repo, mock_product_repo, mock_llm_service)

# ----- Test ProductService con mock repository -----

def test_get_all_products(product_service, mock_product_repo):
    mock_product_repo.get_all.return_value = ["producto1", "producto2"]
    products = product_service.get_all_products()
    assert products == ["producto1", "producto2"]
    mock_product_repo.get_all.assert_called_once()

def test_get_product_by_id_exists(product_service, mock_product_repo):
    mock_product_repo.get_by_id.return_value = "producto1"
    product = product_service.get_product_by_id(1)
    assert product == "producto1"
    mock_product_repo.get_by_id.assert_called_once_with(1)

def test_get_product_by_id_not_found(product_service, mock_product_repo):
    mock_product_repo.get_by_id.return_value = None
    with pytest.raises(ValueError):
        product_service.get_product_by_id(99)

# ----- Test ChatService con mocks -----

def test_generate_chat_response(chat_service, mock_chat_repo, mock_product_repo, mock_llm_service):
    mock_chat_repo.get_session_history.return_value = []
    mock_product_repo.get_all.return_value = ["producto1"]
    mock_llm_service.generate_response.return_value = "respuesta"
    response = chat_service.generate_chat_response("session1", "hola")
    assert response == "respuesta"
    mock_chat_repo.get_session_history.assert_called_once_with("session1", limit=20)
    mock_product_repo.get_all.assert_called_once()
    mock_llm_service.generate_response.assert_called_once()

# ----- Test manejo de excepciones -----

def test_generate_chat_response_llm_error(chat_service, mock_chat_repo, mock_product_repo, mock_llm_service):
    mock_chat_repo.get_session_history.return_value = []
    mock_product_repo.get_all.return_value = []
    mock_llm_service.generate_response.side_effect = Exception("LLM error")
    with pytest.raises(Exception) as exc_info:
        chat_service.generate_chat_response("session1", "error")
    assert "LLM error" in str(exc_info.value)
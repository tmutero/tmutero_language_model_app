import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app
from app.services.openai import OpenAIService
from app.services.user import UserService
from app.models.user import User as UserModel

async def mock_get_current_user():
    return UserModel(id=1, email="testuser@example.com", password="hashedpassword")

app.dependency_overrides[UserService.get_current_user] = mock_get_current_user


client = TestClient(app)

@pytest.fixture
def mock_openai_service():
    with patch("app.services.openai.OpenAIService") as MockService:
        mock_instance = MockService.return_value
        mock_instance.suggest_grammar_correction = AsyncMock(return_value={"corrected_text": "Corrected text"})
        mock_instance.suggest_summarization = AsyncMock(return_value={"summary": "Summarized text"})
        mock_instance.suggest_keyword_extraction = AsyncMock(return_value={"keywords": ["keyword1", "keyword2"]})
        mock_instance.suggest_text_categorization = AsyncMock(return_value={"category": "example"})
        mock_instance.suggest_sentiment_analysis = AsyncMock(return_value={"sentiment": "positive"})
        yield mock_instance


def test_suggest_grammar_correction1(mock_openai_service):

    response = client.post(
        "/api/v1/model/suggest_grammar_correction",
        json={"text": "This is a test."},
    )
    print(response.json())

    assert response.status_code == 200
    assert response.json() == "This is a test."


def test_suggest_grammar_correction(mock_openai_service):
    payload = {
          "text": "This are an example sentence with bad grammarr.",
          "max_tokens": 100,
          "temperature": 0.7
        }
    response = client.post("/api/v1/model/suggest_grammar_correction", json=payload)
    assert response.status_code == 200
    assert response.json() == "This is an example sentence with bad grammar."


def test_suggest_summarization(mock_openai_service):
    sample_text = (
        "Large language models have revolutionized the field of AI, but they also come with several "
        "security concerns including prompt injection and insecure output handling. It is important "
        "to mitigate these risks to ensure safe deployment."
    )
    payload = {
        "text": sample_text,
        "max_tokens": 100,
        "temperature": 0.7
    }
    response = client.post("/api/v1/model/suggest_summarization", json=payload)
    assert response.status_code == 200


def test_suggest_keyword_extraction(mock_openai_service):
    payload = {
        "text": "This is a test.",
        "max_tokens": 100,
        "temperature": 0.7
    }
    response = client.post("/api/v1/model/suggest_keyword_extraction", json=payload)
    assert response.status_code == 200
    assert response.json() == "Test"


def test_suggest_text_categorization(mock_openai_service):
    payload = {
      "text":  "I had an amazing day at the park. The weather was perfect and everything went smoothly.",
      "max_tokens": 100,
      "temperature": 0.7
    }
    category = "?category=Technology&category=Health&category=Finance"
    response = client.post(f"/api/v1/model/suggest_text_categorization{category}", json=payload)
    assert response.status_code == 200
    assert response.json() == "Health"


def test_suggest_sentiment_analysis(mock_openai_service):
    payload = {
        "text": "I'm extremely disappointed with the service; nothing was as promised.",
        "max_tokens": 100,
        "temperature": 0.7
    }
    response = client.post("/api/v1/model/suggest_sentiment_analysis", json=payload)
    assert response.status_code == 200
    assert response.json() == "Negative"

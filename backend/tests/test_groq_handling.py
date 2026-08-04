from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient


@patch("api.main.groq_client")
def test_call_groq_rag_raises_on_malformed_json(mock_groq_client):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "not valid json{{{"
    mock_groq_client.chat.completions.create.return_value = mock_response

    from api.main import call_groq_rag

    with pytest.raises(HTTPException) as exc_info:
        call_groq_rag("some prompt")

    assert exc_info.value.status_code == 502


@patch("api.main.groq_client")
def test_call_groq_rag_parses_valid_response(mock_groq_client):
    mock_response = MagicMock()
    mock_response.choices[
        0
    ].message.content = '{"answer": "Yes.", "cited_sections": ["1946"]}'
    mock_groq_client.chat.completions.create.return_value = mock_response

    from api.main import call_groq_rag

    answer, cited = call_groq_rag("some prompt")

    assert answer == "Yes."
    assert cited == ["1946"]


@patch("api.main.groq_client")
def test_call_groq_rag_raises_on_api_error(mock_groq_client):
    mock_groq_client.chat.completions.create.side_effect = Exception("connection error")

    from api.main import call_groq_rag

    with pytest.raises(HTTPException) as exc_info:
        call_groq_rag("some prompt")

    assert exc_info.value.status_code == 502


@patch("api.main.embedder")
@patch("api.main.collection")
@patch("api.main.call_groq_rag")
def test_ask_falls_back_when_llm_fails(
    mock_call_groq_rag, mock_collection, mock_embedder
):
    import numpy as np

    mock_embedder.encode.return_value = np.array([0.1, 0.2, 0.3])
    mock_collection.query.return_value = {
        "metadatas": [
            [
                {
                    "section_num": "1946",
                    "citation_url": "x",
                    "raw_text": "a",
                    "summary": "s",
                }
            ]
        ],
        "distances": [[0.1]],
    }
    mock_call_groq_rag.side_effect = HTTPException(status_code=502, detail="LLM down")

    from api.main import app

    client = TestClient(app)
    response = client.post("/ask", json={"question": "test question"})

    assert response.status_code == 200
    body = response.json()
    assert "temporarily unavailable" in body["answer"]
    assert body["cited_sections"] == ["1946"]


def test_query_rejects_empty_situation():
    from api.main import app

    client = TestClient(app)
    response = client.post("/query", json={"situation": "   "})

    assert response.status_code == 400


def test_ask_rejects_empty_question():
    from api.main import app

    client = TestClient(app)
    response = client.post("/ask", json={"question": ""})

    assert response.status_code == 400

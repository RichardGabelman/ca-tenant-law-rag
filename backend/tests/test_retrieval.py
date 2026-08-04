from unittest.mock import patch

import numpy as np


@patch("api.main.collection")
@patch("api.main.embedder")
def test_retrieve_top_sections_deduplicates(mock_embedder, mock_collection):
    mock_embedder.encode.return_value = np.array([0.1, 0.2, 0.3])
    mock_collection.query.return_value = {
        "metadatas": [
            [
                {
                    "section_num": "1946",
                    "citation_url": "x",
                    "raw_text": "a",
                    "summary": "s",
                },
                {
                    "section_num": "1946",
                    "citation_url": "x",
                    "raw_text": "a",
                    "summary": "s",
                },  # duplicate
                {
                    "section_num": "1950",
                    "citation_url": "x",
                    "raw_text": "b",
                    "summary": "s",
                },
            ]
        ],
        "distances": [[0.1, 0.1, 0.2]],
    }

    from api.main import retrieve_top_sections

    results = retrieve_top_sections("test question", k_fetch=10, k_context=3)

    assert len(results) == 2
    assert {r.section_num for r in results} == {"1946", "1950"}


@patch("api.main.collection")
@patch("api.main.embedder")
def test_retrieve_top_sections_respects_k_context(mock_embedder, mock_collection):
    mock_embedder.encode.return_value = np.array([0.1, 0.2, 0.3])
    mock_collection.query.return_value = {
        "metadatas": [
            [
                {
                    "section_num": str(i),
                    "citation_url": "x",
                    "raw_text": "a",
                    "summary": "s",
                }
                for i in range(10)
            ]
        ],
        "distances": [[0.1] * 10],
    }

    from api.main import retrieve_top_sections

    results = retrieve_top_sections("test question", k_fetch=10, k_context=3)

    assert len(results) == 3


@patch("api.main.collection")
@patch("api.main.embedder")
def test_retrieve_top_sections_computes_score_from_distance(
    mock_embedder, mock_collection
):
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
        "distances": [[0.25]],
    }

    from api.main import retrieve_top_sections

    results = retrieve_top_sections("test question", k_fetch=10, k_context=3)

    assert results[0].score == 0.75

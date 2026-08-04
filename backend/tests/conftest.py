import os
import tempfile

import chromadb
import pytest


@pytest.fixture(scope="session", autouse=True)
def fake_chroma_db():
    """Creates a throwaway Chroma collection so api.main can import successfully in CI,
    without needing the real ~production chroma_db artifact checked out."""
    tmp_dir = tempfile.mkdtemp()
    os.environ["CHROMA_DIR"] = tmp_dir

    client = chromadb.PersistentClient(path=tmp_dir)
    collection = client.create_collection("tenant_rights")
    collection.add(
        ids=["1946"],
        embeddings=[[0.1] * 384],
        metadatas=[
            {
                "section_num": "1946",
                "citation_url": "https://example.com",
                "raw_text": "Placeholder statute text.",
                "summary": "Placeholder summary.",
            }
        ],
    )
    yield

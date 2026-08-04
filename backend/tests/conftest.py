import os
import tempfile

import chromadb

_tmp_dir = tempfile.mkdtemp()
os.environ["CHROMA_DIR"] = _tmp_dir
os.environ.setdefault("GROQ_API_KEY", "dummy-key-for-ci")

_client = chromadb.PersistentClient(path=_tmp_dir)
_collection = _client.create_collection("tenant_rights")
_collection.add(
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

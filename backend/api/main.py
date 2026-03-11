import os
import chromadb
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

CHROMA_DIR = os.getenv("CHROMA_DIR", "../chroma_db")

app = FastAPI()

model = SentenceTransformer("all-MiniLM-l6-v2")
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = chroma_client.get_collection("tenant_rights")


class QueryRequest(BaseModel):
    situation: str


class SectionResult(BaseModel):
    section_num: str
    citation_url: str
    raw_text: str


class QueryResponse(BaseModel):
    results: list[SectionResult]


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    query_embedding = model.encode(request.situation).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        include=["documents", "metadatas", "distances"],
    )
    assert results["documents"] is not None
    assert results["metadatas"] is not None

    output = []
    for doc, metadata in zip(results["documents"][0], results["metadatas"][0]):
        output.append(
            SectionResult(
                section_num=str(metadata["section_num"]),
                citation_url=str(metadata["citation_url"]),
                raw_text=doc,
            )
        )

    return QueryResponse(results=output)

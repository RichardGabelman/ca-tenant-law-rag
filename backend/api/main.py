import os
import chromadb
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

CHROMA_DIR = os.getenv("CHROMA_DIR", "../chroma_db")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
SIMILARITY_THRESHOLD = 0.3

origins = [origin.strip() for origin in ALLOWED_ORIGINS.split(",")]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

model = SentenceTransformer("all-MiniLM-l6-v2")
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = chroma_client.get_collection("tenant_rights")


class QueryRequest(BaseModel):
    situation: str


class SectionResult(BaseModel):
    section_num: str
    citation_url: str
    raw_text: str
    summary: str
    score: float


class QueryResponse(BaseModel):
    results: list[SectionResult]


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    if not request.situation:
        raise HTTPException(status_code=400, detail="Please describe your situation.")

    query_embedding = model.encode(request.situation).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=25,
        include=["documents", "metadatas", "distances"],
    )
    assert results["documents"] is not None
    assert results["metadatas"] is not None
    assert results["distances"] is not None

    seen: set[str] = set()
    output = []

    for metadata, distance in zip(results["metadatas"][0], results["distances"][0]):
        section_num = str(metadata["section_num"])
        score = round(1 - distance, 3)

        if distance > SIMILARITY_THRESHOLD:
            continue

        if section_num in seen:
            continue
        seen.add(section_num)

        output.append(
            SectionResult(
                section_num=section_num,
                citation_url=str(metadata["citation_url"]),
                raw_text=str(metadata["raw_text"]),
                summary=str(metadata["summary"]),
                score=score,
            )
        )

        if len(output) == 5:
            break

    return QueryResponse(results=output)

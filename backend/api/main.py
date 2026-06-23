import os
import json
import chromadb
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

CHROMA_DIR = os.getenv("CHROMA_DIR", "../chroma_db")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
RAG_MODEL = os.getenv("RAG_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")

origins = [origin.strip() for origin in ALLOWED_ORIGINS.split(",")]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

embedder = SentenceTransformer("all-MiniLM-l6-v2")
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = chroma_client.get_collection("tenant_rights")
groq_client = Groq(api_key=GROQ_API_KEY)


class SectionResult(BaseModel):
    section_num: str
    citation_url: str
    raw_text: str
    summary: str
    score: float


class QueryRequest(BaseModel):
    situation: str


class QueryResponse(BaseModel):
    results: list[SectionResult]


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    if not request.situation.strip():
        raise HTTPException(status_code=400, detail="Please describe your situation.")

    query_embedding = embedder.encode(request.situation).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=50,
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

    return QueryResponse(results=output)


TOP_K_FETCH = 10
TOP_K_CONTEXT = 3


def retrieve_top_sections(
    question: str, k_fetch: int, k_context: int
) -> list[SectionResult]:
    """Embed the question, query Chroma, deduplicate by section, return top k_context."""
    embedding = embedder.encode(question).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=k_fetch,
        include=["metadatas", "distances"],
    )
    assert results["metadatas"] is not None
    assert results["distances"] is not None

    seen: set[str] = set()
    sections: list[SectionResult] = []

    for metadata, distance in zip(results["metadatas"][0], results["distances"][0]):
        section_num = str(metadata["section_num"])
        if section_num in seen:
            continue
        seen.add(section_num)

        sections.append(
            SectionResult(
                section_num=section_num,
                citation_url=str(metadata["citation_url"]),
                raw_text=str(metadata["raw_text"]),
                summary=str(metadata["summary"]),
                score=round(1 - distance, 3),
            )
        )

        if len(sections) == k_context:
            break

    return sections


def build_rag_prompt(question: str, sections: list[SectionResult]) -> str:
    context_blocks = "\n\n".join(
        f"--- California Civil Code § {s.section_num} ---\n{s.raw_text}"
        for s in sections
    )

    return f"""You are a legal information assistant helping California tenants understand their rights.
You are NOT a lawyer and must not provide legal advice. Provide clear, accurate information based only on the statutes provided.

A tenant has asked the following question:
"{question}"

Below are the relevant sections of California Civil Code. Use ONLY these sections to answer. If the answer cannot be determined from the provided text, say so clearly.

{context_blocks}

Respond ONLY with a JSON object in exactly this format, no preamble, no markdown:
{{
  "answer": "A plain-English explanation (3-6 sentences) a non-lawyer renter could understand. Do not invent anything not supported by the statutes above. End with a reminder that this is general legal information, not legal advice.",
  "cited_sections": ["1234", "1235"]
}}

cited_sections must contain only section numbers from the statutes provided above that you actually drew from to write the answer. Omit any that were not relevant."""


def call_groq_rag(prompt: str) -> tuple[str, list[str]]:
    """Call Groq and parse the structured JSON response. Returns (answer, cited_sections)."""
    response = groq_client.chat.completions.create(
        model=RAG_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=600,
        response_format={"type": "json_object"},
    )

    raw = str(response.choices[0].message.content)

    try:
        data = json.loads(raw)
        answer = str(data["answer"])
        cited = [str(s) for s in data.get("cited_sections", [])]
    except (json.JSONDecodeError, KeyError) as e:
        raise HTTPException(
            status_code=502,
            detail=f"LLM returned malformed JSON: {e}. Raw: {raw[:200]}",
        )

    return answer, cited


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    cited_sections: list[str]
    context_sections: list[SectionResult]


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Please provide a question.")

    sections = retrieve_top_sections(request.question, TOP_K_FETCH, TOP_K_CONTEXT)

    if not sections:
        raise HTTPException(status_code=404, detail="No relevant sections found.")

    prompt = build_rag_prompt(request.question, sections)
    answer, cited_sections = call_groq_rag(prompt)

    return AskResponse(
        answer=answer,
        cited_sections=cited_sections,
        context_sections=sections,
    )

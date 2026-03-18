"""Embeds California Civil Code sections into a Chroma vector database."""

import os
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from ingest.summarize import build_chunks, enrich_chunks

load_dotenv()

CHROMA_DIR = os.getenv("CHROMA_DIR", "../chroma_db")
MODEL_NAME = "all-MiniLM-L6-v2"


def embed_chunks():
    """Embed all tenant rights chunks and stores them in Chroma."""
    model = SentenceTransformer(MODEL_NAME)

    chunks = build_chunks()
    enriched = enrich_chunks(chunks)

    client = chromadb.PersistentClient(path=CHROMA_DIR)

    try:
        client.delete_collection("tenant_rights")
    except ValueError:
        pass

    collection = client.create_collection(
        "tenant_rights", metadata={"hnsw:space": "cosine"}
    )

    for chunk in enriched:
        section_num = chunk["section_num"]
        section_id = chunk["section_id"]

        metadata = {
            "section_num": section_num,
            "citation_url": chunk["citation_url"],
            "summary": chunk["summary"],
            "raw_text": chunk["full_text"],
        }

        summary_embedding = model.encode(chunk["summary"]).tolist()
        collection.add(
            ids=[f"{section_id}_summary"],
            embeddings=[summary_embedding],
            documents=[chunk["summary"]],
            metadatas=[metadata],
        )

        for i, question in enumerate(chunk["questions"]):
            question_embedding = model.encode(question).tolist()
            collection.add(
                ids=[f"{section_id}_q{i}"],
                embeddings=[question_embedding],
                documents=[question],
                metadatas=[metadata],
            )

        print(f"{chunk['section_num']} OK")
    print(f"\nDone - {collection.count()} chunks stored in Chroma")


if __name__ == "__main__":
    embed_chunks()

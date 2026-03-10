import os
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from load import build_chunks

load_dotenv()

CHROMA_DIR = os.getenv("CHROMA_DIR", "../chroma_dub")
MODEL_NAME = "all-MiniLM-L6-v2"


def embed_chunks():
    model = SentenceTransformer(MODEL_NAME)

    chunks = build_chunks()

    client = chromadb.PersistentClient(path=CHROMA_DIR)

    try:
        client.delete_collection("tenant_rights")
    except:
        pass

    collection = client.create_collection("tenant_rights")

    for chunk in chunks:
        embedding = model.encode(chunk["full_text"]).tolist()

        collection.add(
            ids=[chunk["section_id"]],
            embeddings=[embedding],
            documents=[chunk["full_text"]],
            metadatas=[
                {
                    "section_num": chunk["section_num"],
                    "citation_url": chunk["citation_url"],
                    "enactment_history": chunk["enactment_history"],
                    "subdivision_count": len(chunk["subdivisions"]),
                }
            ],
        )
        print(f"{chunk['section_num']} OK")
    
    print(f"\nDone - {collection.count()} chunks stored in Chroma")

if __name__ == "__main__":
    embed_chunks()

"""Generates plain-English summaries and example questions for each Civil Code chunk"""

import os
import time
import json
from groq import Groq
from dotenv import load_dotenv
from ingest.load import build_chunks

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
DELAY_SECONDS = 3


def build_prompt(chunk: dict) -> str:
    return f"""You are helping build a legal information tool for California tenants.

Below is the full text of California Civil Code § {chunk["section_num"]}.

Your task is to produce two things:
1. A plain-English summary (3-5 sentences) that a non-lawyer renter could understand. Cover the key rights and obligations this section establishes.
2. Exactly 5 example questions that a tenant might ask whose answer would be found in this section. Questions should be natural, conversational, and varied — not just paraphrases of each other.

Respond ONLY with a JSON object in exactly this format, no preamble, no markdown:
{{
  "summary": "...",
  "questions": [
    "...",
    "...",
    "...",
    "...",
    "..."
  ]
}}

Civil Code § {chunk["section_num"]}:
{chunk["full_text"]}"""


def enrich_chunks(chunks: list[dict]) -> list[dict]:
    client = Groq(api_key=GROQ_API_KEY)
    enriched = []

    for i, chunk in enumerate(chunks):
        print(f"[{i + 1}/{len(chunks)}] § {chunk['section_num']}...")

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": build_prompt(chunk)}],
                temperature=0.3,
                max_tokens=500,
                response_format={"type": "json_object"},
            )

            raw = str(response.choices[0].message.content)
            data = json.loads(raw)

            chunk["summary"] = data["summary"]
            chunk["questions"] = data["questions"]
            enriched.append(chunk)
            print(f" OK summary + {len(data['questions'])} questions")

        except (json.JSONDecodeError, KeyError) as e:
            print(f" parse error - {e}, skipping")
        except Exception as e:
            print(f" API error - {e}, skipping")

        if i < len(chunks) - 1:
            time.sleep(DELAY_SECONDS)

    print(f"\nEnriched {len(enriched) / len(chunks)} chunks")
    return enriched


if __name__ == "__main__":
    chunks = build_chunks()
    enriched = enrich_chunks(chunks)

    if enriched:
        sample = enriched[0]
        print(f"\n--- Sample: {sample['section_num']} ---")
        print(f"Summary: {sample['summary'][:200]}...")
        print("Questions:")
        for q in sample["questions"]:
            print(f" - {q}")

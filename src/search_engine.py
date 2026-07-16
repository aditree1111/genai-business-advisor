from pathlib import Path
import re

# ------------------------------------
# Load Apple Report
# ------------------------------------

project_root = Path(__file__).resolve().parent.parent

text_file = project_root / "documents" / "apple_report.txt"

with open(text_file, "r", encoding="utf-8") as f:
    text = f.read()

# ------------------------------------
# Create Chunks
# ------------------------------------

chunk_size = 1000

chunks = []

for i in range(0, len(text), chunk_size):
    chunks.append(text[i:i+chunk_size])

print(f"Loaded {len(chunks)} chunks.")

# ------------------------------------
# Search Function
# ------------------------------------

def search_chunks(query, chunks, top_k=3):

    query_words = re.findall(r"\w+", query.lower())

    scores = []

    for chunk in chunks:

        score = 0

        chunk_lower = chunk.lower()

        for word in query_words:

            score += chunk_lower.count(word)

        scores.append(score)

    ranked = sorted(
        zip(scores, chunks),
        reverse=True,
        key=lambda x: x[0]
    )

    return [chunk for score, chunk in ranked[:top_k] if score > 0]


# ------------------------------------
# Test
# ------------------------------------

question = "What are Apple's biggest risks?"

results = search_chunks(question, chunks)

print("\nTop Matching Chunks\n")

for i, chunk in enumerate(results, start=1):

    print("=" * 60)

    print(f"Chunk {i}")

    print("=" * 60)

    print(chunk[:600])

    print()
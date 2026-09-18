import json
import numpy as np
import faiss
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

# Load FAISS index
index = faiss.read_index("faiss_index.bin")

# Load original chunks
with open("chunks.json", "r", encoding="utf-8") as file:
    chunks = json.load(file)

# We only created embeddings for the first 100 chunks
chunks = chunks[:100]


def search_knowledge(query, top_k=3):

    # Convert user question into an embedding
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=query
    )

    query_embedding = np.array(
        [result.embeddings[0].values],
        dtype="float32"
    )

    # Search FAISS
    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for i in indices[0]:
        results.append(chunks[i])

    return results


# Test
query = "How does biodiversity help agriculture?"

results = search_knowledge(query)

print("\nRetrieved knowledge:\n")

for i, result in enumerate(results, 1):
    print(f"\n--- Result {i} ---\n")
    print(result)
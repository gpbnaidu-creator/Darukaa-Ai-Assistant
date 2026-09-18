import os
import json
import numpy as np
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Load chunks
with open("chunks.json", "r", encoding="utf-8") as file:
    chunks = json.load(file)

chunks = chunks[:100]

print("Chunks selected:", len(chunks))


all_embeddings = []

# Process 50 chunks at a time
batch_size = 10

for i in range(0, len(chunks), batch_size):

    batch = chunks[i:i + batch_size]

    print(f"Processing chunks {i + 1} to {i + len(batch)}...")

    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=batch
    )

    for embedding in result.embeddings:
        all_embeddings.append(embedding.values)

# Convert to NumPy array
embeddings_array = np.array(all_embeddings, dtype="float32")

print("\nEmbeddings created:", len(embeddings_array))
print("Embedding size:", embeddings_array.shape[1])

# Save embeddings
np.save("embeddings.npy", embeddings_array)

print("Embeddings saved to embeddings.npy")
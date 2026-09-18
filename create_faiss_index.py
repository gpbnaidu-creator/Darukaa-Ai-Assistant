import numpy as np
import faiss

# Load embeddings
embeddings = np.load("embeddings.npy")

print("Embeddings shape:", embeddings.shape)

# Create FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])

# Add embeddings to the index
index.add(embeddings)

print("Vectors in FAISS:", index.ntotal)

# Save index
faiss.write_index(index, "faiss_index.bin")

print("FAISS index saved!")
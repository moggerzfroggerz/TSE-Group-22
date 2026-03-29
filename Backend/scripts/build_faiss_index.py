import numpy as np, faiss
from pathlib import Path

DATA=Path("data")
X=np.load(DATA/"embeddings.npy").astype("float32")

index=faiss.IndexFlatIP(X.shape[1])
index.add(X)
faiss.write_index(index,"faiss_index.bin")
print("Index saved")

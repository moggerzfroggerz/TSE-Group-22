from pathlib import Path
import faiss
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
EMBEDDINGS_PATH = BASE_DIR / "data" / "embeddings.npy"
FAISS_INDEX_OUTPUT_PATH = BASE_DIR / "faiss_index.bin"

def main() -> None:
    embeddings = np.load(EMBEDDINGS_PATH).astype("float32")
    if embeddings.ndim != 2 or embeddings.shape[0] == 0:
        raise ValueError("Embeddings file is empty or invalid.")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, str(FAISS_INDEX_OUTPUT_PATH))

    print("FAISS index created successfully.")
    print(f"Number of vectors: {index.ntotal}")
    print(f"Vector dimension: {embeddings.shape[1]}")

if __name__ == "__main__":
    main()

import json
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CLEANED_DOCS_PATH = DATA_DIR / "cleaned_docs.json"
EMBEDDINGS_OUTPUT_PATH = DATA_DIR / "embeddings.npy"
METADATA_OUTPUT_PATH = DATA_DIR / "embeddings_meta.json"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def main() -> None:
    records = json.loads(CLEANED_DOCS_PATH.read_text(encoding="utf-8"))
    texts = [record["text"] for record in records]

    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
    embeddings = np.asarray(embeddings, dtype="float32")

    np.save(EMBEDDINGS_OUTPUT_PATH, embeddings)

    metadata = [
        {
            "document_id": record["document_id"],
            "chunk_id": record["chunk_id"],
            "mode": record["mode"],
            "source_file": record["source_file"]
        }
        for record in records
    ]

    METADATA_OUTPUT_PATH.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Embedding generation completed.")
    print(f"Embedding shape: {embeddings.shape}")

if __name__ == "__main__":
    main()

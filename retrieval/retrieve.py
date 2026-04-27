import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

CLEANED_DOCS_PATH = DATA_DIR / "cleaned_docs.json"
METADATA_PATH = DATA_DIR / "embeddings_meta.json"
FAISS_INDEX_PATH = BASE_DIR / "faiss_index.bin"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class DocumentRetriever:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self.index = faiss.read_index(str(FAISS_INDEX_PATH))

        self.documents = self.load_json(CLEANED_DOCS_PATH)
        self.metadata = self.load_json(METADATA_PATH)

    def load_json(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def create_query_embedding(self, query):
        embedding = self.model.encode([query], normalize_embeddings=True)
        return np.asarray(embedding, dtype="float32")

    def retrieve(self, query, mode="all", top_k=5):
        query_embedding = self.create_query_embedding(query)

        search_k = min(top_k, self.index.ntotal)
        scores, indexes = self.index.search(query_embedding, search_k)

        results = []

        for score, index_id in zip(scores[0], indexes[0]):
            if index_id == -1:
                continue

            document = self.documents[index_id]
            metadata = self.metadata[index_id]

            if mode != "all" and metadata["mode"] != mode:
                continue

            results.append({
                "score": float(score),
                "mode": metadata["mode"],
                "source": metadata["source_file"],
                "text": document["text"]
            })

        return results


def print_results(results):
    if not results:
        print("\nNo relevant results found.")
        return

    print("\nTop Results:")

    for number, result in enumerate(results, start=1):
        print("\n" + "-" * 60)
        print(f"Result {number}")
        print(f"Score: {result['score']:.4f}")
        print(f"Mode: {result['mode']}")
        print(f"Source: {result['source']}")
        print(f"Text: {result['text'][:500]}...")


def main():
    retriever = DocumentRetriever()

    print("\nEDUCARE AI Retrieval System")
    print("This system searches patient and professional medical documents.")
    print("Type 'exit' to stop.\n")

    while True:
        query = input("Enter your question: ").strip()

        if query.lower() == "exit":
            print("Program stopped.")
            break

        if not query:
            print("Please enter a question.")
            continue

        mode = input("Choose mode (patient / professional / all): ").strip().lower()

        if mode not in ["patient", "professional", "all"]:
            print("Invalid mode, using 'all' instead.")
            mode = "all"

        results = retriever.retrieve(query=query, mode=mode, top_k=5)
        print_results(results)


if __name__ == "__main__":
    main()
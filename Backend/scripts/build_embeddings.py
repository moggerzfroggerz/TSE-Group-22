import json, numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

DATA=Path("data")
chunks=json.loads((DATA/"cleaned_docs.json").read_text())
texts=[c["text"] for c in chunks]

model=SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
emb=model.encode(texts,normalize_embeddings=True)

np.save(DATA/"embeddings.npy",emb)

meta=[{"doc_id":c["doc_id"],"chunk_id":c["chunk_id"],"source":c["source"]} for c in chunks]
(DATA/"embeddings_meta.json").write_text(json.dumps(meta,indent=2))
print("Embeddings done")

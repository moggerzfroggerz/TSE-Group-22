import os
os.system("python scripts/build_cleaned_docs.py")
os.system("python scripts/build_embeddings.py")
os.system("python scripts/build_faiss_index.py")
os.system("python retrieval/retrieve.py")

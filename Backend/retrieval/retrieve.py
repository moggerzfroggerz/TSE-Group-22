import json, numpy as np, faiss
from sentence_transformers import SentenceTransformer

model=SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
index=faiss.read_index("faiss_index.bin")

chunks=json.load(open("data/cleaned_docs.json"))
meta=json.load(open("data/embeddings_meta.json"))

def retrieve(q,k=5):
    emb=model.encode([q],normalize_embeddings=True).astype("float32")
    scores,idx=index.search(emb,k)
    res=[]
    for i,s in zip(idx[0],scores[0]):
        res.append({"score":float(s),"text":chunks[i]["text"],"source":meta[i]["source"]})
    return res

if __name__=="__main__":
    for r in retrieve("What is asthma?"):
        print(r["score"],r["text"][:120])

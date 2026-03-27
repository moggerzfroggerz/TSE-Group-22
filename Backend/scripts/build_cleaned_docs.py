import os
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw_docs"
OUT_FILE = DATA_DIR / "cleaned_docs.json"

MIN_WORDS = 50
MAX_WORDS = 200
OVERLAP_WORDS = 30

def read_text_file(path):
    return path.read_text(encoding="utf-8", errors="ignore")

def strip_html(html):
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script","style","nav","header","footer","aside"]):
        tag.decompose()
    return soup.get_text(" ")

def clean_text(text, ext):
    if ext in [".html", ".htm"]:
        text = strip_html(text)
    return re.sub(r"\s+", " ", text).strip()

def chunk(words):
    chunks = []
    i = 0

    if len(words) < MIN_WORDS:
        return [" ".join(words)]

    while i < len(words):
        part = words[i:i + MAX_WORDS]
        if len(part) >= MIN_WORDS:
            chunks.append(" ".join(part))
        i += MAX_WORDS - OVERLAP_WORDS

    return chunks

def main():
    all_chunks = []
    cid = 0

    print("Looking in:", RAW_DIR)

    if not RAW_DIR.exists():
        print("ERROR: raw_docs folder not found")
        return

    files = list(RAW_DIR.rglob("*"))
    print("Files found:", len(files))

    for did, path in enumerate(files):
        if not path.is_file():
            continue

        print(f"Processing: {path}")

        txt = clean_text(read_text_file(path), path.suffix.lower())
        words = txt.split()

        print(f"Word count: {len(words)}")

        chunks = chunk(words)

        for c in chunks:
            all_chunks.append({
                "doc_id": did,
                "chunk_id": cid,
                "source": str(path),
                "text": c
            })
            cid += 1

    OUT_FILE.write_text(json.dumps(all_chunks, indent=2))

    print("Saved", len(all_chunks), "chunks")

if __name__ == "__main__":
    main()
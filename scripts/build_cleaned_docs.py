import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DOCS_DIR = BASE_DIR / "data" / "raw_docs"
CLEANED_OUTPUT_PATH = BASE_DIR / "data" / "cleaned_docs.json"

MIN_WORDS = 50
MAX_WORDS = 180
OVERLAP_WORDS = 25

def detect_mode(file_path: Path) -> str:
    file_name = file_path.name.lower()
    if file_name.startswith("patient_"):
        return "patient"
    if file_name.startswith("professional_"):
        return "professional"
    return "unknown"

def normalise_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def split_into_chunks(text: str) -> list[str]:
    words = text.split()
    if not words:
        return []
    if len(words) <= MAX_WORDS:
        return [" ".join(words)]

    chunks = []
    start = 0
    step = MAX_WORDS - OVERLAP_WORDS
    while start < len(words):
        chunk_words = words[start:start + MAX_WORDS]
        if len(chunk_words) >= MIN_WORDS:
            chunks.append(" ".join(chunk_words))
        start += step
    return chunks

def build_cleaned_records() -> list[dict]:
    cleaned_records = []
    chunk_id = 0
    files = sorted(RAW_DOCS_DIR.glob("*.txt"))
    print(f"Files found: {len(files)}")

    for document_id, file_path in enumerate(files):
        cleaned_text = normalise_text(file_path.read_text(encoding="utf-8", errors="ignore"))
        chunks = split_into_chunks(cleaned_text)
        mode = detect_mode(file_path)
        print(f"Processing: {file_path.name} | Mode: {mode} | Chunks: {len(chunks)}")

        for chunk_text in chunks:
            cleaned_records.append({
                "document_id": document_id,
                "chunk_id": chunk_id,
                "mode": mode,
                "source_file": str(file_path),
                "text": chunk_text
            })
            chunk_id += 1
    return cleaned_records

def main() -> None:
    records = build_cleaned_records()
    if not records:
        raise ValueError("No cleaned records were created.")
    CLEANED_OUTPUT_PATH.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved {len(records)} cleaned chunks to {CLEANED_OUTPUT_PATH}")

if __name__ == "__main__":
    main()

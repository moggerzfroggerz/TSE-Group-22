import os
import sys

PYTHON = sys.executable

COMMANDS = [
    f'"{PYTHON}" scripts/generate_dataset.py',
    f'"{PYTHON}" scripts/build_cleaned_docs.py',
    f'"{PYTHON}" scripts/build_embeddings.py',
    f'"{PYTHON}" scripts/build_faiss_index.py',
    f'"{PYTHON}" retrieval/retrieve.py'
]

def main() -> None:
    for command in COMMANDS:
        print("\nRunning:", command)
        result = os.system(command)
        if result != 0:
            print("Command failed:", command)
            break

if __name__ == "__main__":
    main()

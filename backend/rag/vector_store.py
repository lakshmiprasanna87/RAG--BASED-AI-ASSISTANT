import os
import pickle
import numpy as np
import faiss

from backend.rag.text_splitter import create_chunks
from backend.rag.embeddings import create_embeddings


# Folder where vector databases are stored
VECTOR_DB_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../vector_db")
)


# National files
NATIONAL_INDEX_FILE = os.path.join(
    VECTOR_DB_DIR, "national.index"
)

NATIONAL_CHUNKS_FILE = os.path.join(
    VECTOR_DB_DIR, "national_chunks.pkl"
)


# International files
INTERNATIONAL_INDEX_FILE = os.path.join(
    VECTOR_DB_DIR, "international.index"
)

INTERNATIONAL_CHUNKS_FILE = os.path.join(
    VECTOR_DB_DIR, "international_chunks.pkl"
)


def get_source(chunk):
    """
    Get the source/file path from a chunk.
    Supports several possible metadata formats.
    """

    if "source" in chunk:
        return str(chunk["source"])

    if "file_path" in chunk:
        return str(chunk["file_path"])

    if "file" in chunk:
        return str(chunk["file"])

    if "metadata" in chunk:
        metadata = chunk["metadata"]

        if isinstance(metadata, dict):
            if "source" in metadata:
                return str(metadata["source"])

            if "file_path" in metadata:
                return str(metadata["file_path"])

    return ""


def get_scope(chunk):
    """
    Determine whether a document is National or International
    based on its folder location.
    """

    source = get_source(chunk).lower().replace("\\", "/")

    if "/national/" in source or source.startswith("national/"):
        return "National"

    if "/international/" in source or source.startswith("international/"):
        return "International"

    return None


def save_faiss_index(chunks, index_file, chunks_file):
    """
    Create and save a FAISS index for a group of chunks.
    """

    if not chunks:
        print(f"No chunks found for {index_file}")
        return

    texts = [chunk["text"] for chunk in chunks]

    print(f"Creating embeddings for {len(texts)} chunks...")

    embeddings = create_embeddings(texts)

    embeddings = np.asarray(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    faiss.write_index(index, index_file)

    with open(chunks_file, "wb") as file:
        pickle.dump(chunks, file)

    print("Index saved:", index_file)
    print("Chunks saved:", chunks_file)
    print("Number of vectors:", index.ntotal)


def build_vector_store():
    """
    Build separate FAISS databases for:

    National
    International
    """

    print("\n========================================")
    print("BUILDING VECTOR DATABASE")
    print("========================================\n")

    print("Loading and splitting documents...")

    chunks = create_chunks()

    if not chunks:
        print("No document chunks found.")
        print("Please add PDF files inside the data folder.")
        return

    print("Total chunks:", len(chunks))

    # Separate documents by scope
    national_chunks = []
    international_chunks = []

    for chunk in chunks:

        scope = get_scope(chunk)

        if scope == "National":
            national_chunks.append(chunk)

        elif scope == "International":
            international_chunks.append(chunk)

    print("\n----------------------------------------")
    print("National chunks:", len(national_chunks))
    print("International chunks:", len(international_chunks))
    print("----------------------------------------\n")

    # Create vector_db directory
    os.makedirs(VECTOR_DB_DIR, exist_ok=True)

    # Build National database
    print("\nBuilding NATIONAL vector database...")

    save_faiss_index(
        national_chunks,
        NATIONAL_INDEX_FILE,
        NATIONAL_CHUNKS_FILE
    )

    # Build International database
    print("\nBuilding INTERNATIONAL vector database...")

    save_faiss_index(
        international_chunks,
        INTERNATIONAL_INDEX_FILE,
        INTERNATIONAL_CHUNKS_FILE
    )

    print("\n========================================")
    print("VECTOR DATABASE CREATION COMPLETE")
    print("========================================")


if __name__ == "__main__":
    build_vector_store()
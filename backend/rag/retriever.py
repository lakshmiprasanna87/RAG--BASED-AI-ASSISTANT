import os
import pickle
import faiss
import numpy as np
from typing import Optional

from backend.rag.embeddings import create_embeddings


# ============================================================
# VECTOR DATABASE DIRECTORY
# ============================================================

VECTOR_DB_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../vector_db"
    )
)


# ============================================================
# NATIONAL DATABASE
# ============================================================

NATIONAL_INDEX_FILE = os.path.join(
    VECTOR_DB_DIR,
    "national.index"
)

# Support both possible filenames
NATIONAL_CHUNKS_FILE = os.path.join(
    VECTOR_DB_DIR,
    "national_chunks.pkl"
)

NATIONAL_DATA_FILE = os.path.join(
    VECTOR_DB_DIR,
    "national_data.pkl"
)


# ============================================================
# INTERNATIONAL DATABASE
# ============================================================

INTERNATIONAL_INDEX_FILE = os.path.join(
    VECTOR_DB_DIR,
    "international.index"
)

# Support both possible filenames
INTERNATIONAL_CHUNKS_FILE = os.path.join(
    VECTOR_DB_DIR,
    "international_chunks.pkl"
)

INTERNATIONAL_DATA_FILE = os.path.join(
    VECTOR_DB_DIR,
    "international_data.pkl"
)


# ============================================================
# LOAD DATABASE
# ============================================================

def load_database(scope: str):

    scope = scope.strip().title()

    if scope == "National":

        index_file = NATIONAL_INDEX_FILE

        possible_chunk_files = [
            NATIONAL_CHUNKS_FILE,
            NATIONAL_DATA_FILE
        ]

    elif scope == "International":

        index_file = INTERNATIONAL_INDEX_FILE

        possible_chunk_files = [
            INTERNATIONAL_CHUNKS_FILE,
            INTERNATIONAL_DATA_FILE
        ]

    else:

        raise ValueError(
            "Scope must be either 'National' or 'International'"
        )

    # --------------------------------------------------------
    # Check FAISS index
    # --------------------------------------------------------

    if not os.path.exists(index_file):

        raise FileNotFoundError(
            f"{scope} vector database not found:\n"
            f"{index_file}\n\n"
            f"Please rebuild the vector database."
        )

    # --------------------------------------------------------
    # Find chunks/data file
    # --------------------------------------------------------

    chunks_file = None

    for file_path in possible_chunk_files:

        if os.path.exists(file_path):

            chunks_file = file_path
            break

    if chunks_file is None:

        raise FileNotFoundError(
            f"{scope} chunks file not found.\n"
            f"Expected one of:\n"
            f"{possible_chunk_files}"
        )

    # --------------------------------------------------------
    # Load FAISS
    # --------------------------------------------------------

    index = faiss.read_index(index_file)

    # --------------------------------------------------------
    # Load chunks
    # --------------------------------------------------------

    with open(chunks_file, "rb") as file:

        chunks = pickle.load(file)

    return index, chunks


# ============================================================
# SEARCH DOCUMENTS
# ============================================================

def search_documents(
    question: str,
    top_k: int = 5,
    scope: Optional[str] = "National"
):

    # --------------------------------------------------------
    # Validate scope
    # --------------------------------------------------------

    if scope is None:
        scope = "National"

    scope = scope.strip().title()

    if scope not in [
        "National",
        "International"
    ]:

        raise ValueError(
            "Scope must be either "
            "'National' or 'International'"
        )

    print(
        f"\nSearching {scope} knowledge base..."
    )

    # --------------------------------------------------------
    # IMPORTANT:
    # Load ONLY the selected database
    # --------------------------------------------------------

    index, chunks = load_database(scope)

    print(
        f"{scope} vectors available: "
        f"{index.ntotal}"
    )

    if index.ntotal == 0:

        print(
            f"No vectors found in {scope} database."
        )

        return []

    # --------------------------------------------------------
    # Create question embedding
    # --------------------------------------------------------

    query_embedding = create_embeddings(
        [question]
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    # --------------------------------------------------------
    # FAISS search
    # --------------------------------------------------------

    number_to_search = min(
        top_k,
        index.ntotal
    )

    distances, indices = index.search(
        query_embedding,
        number_to_search
    )

    # --------------------------------------------------------
    # Collect results
    # --------------------------------------------------------

    retrieved_documents = []

    for position in indices[0]:

        if position == -1:
            continue

        if position >= len(chunks):
            continue

        document = chunks[position]

        # ----------------------------------------------------
        # Extra safety check
        #
        # Even though we are using separate FAISS databases,
        # make sure the returned metadata agrees with scope.
        # ----------------------------------------------------

        document_scope = document.get(
            "scope",
            ""
        ).strip().title()

        if document_scope:

            if document_scope != scope:

                print(
                    "WARNING: Ignoring document with "
                    f"wrong scope: {document_scope}"
                )

                continue

        retrieved_documents.append(
            document
        )

    print(
        f"Retrieved {len(retrieved_documents)} "
        f"{scope} documents."
    )

    return retrieved_documents
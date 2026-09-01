from backend.rag.document_loader import load_documents


def split_text(text, chunk_size=1000, overlap=200):
    """
    Split text into overlapping chunks.

    chunk_size = maximum number of characters in each chunk
    overlap = characters repeated between consecutive chunks
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_chunks():
    """
    Load documents and create chunks while preserving
    National / International scope information.
    """

    documents = load_documents()

    all_chunks = []

    for document in documents:

        chunks = split_text(
            document["text"]
        )

        for chunk_number, chunk in enumerate(
            chunks,
            start=1
        ):

            all_chunks.append({
                "text": chunk,

                # PDF source
                "source": document["source"],

                # National / International
                "scope": document.get(
                    "scope",
                    "Other"
                ),

                # Category
                "category": document["category"],

                # PDF page
                "page": document["page"],

                # Chunk number
                "chunk": chunk_number
            })

    print(
        f"Created {len(all_chunks)} chunks."
    )

    # Show scope counts
    national_chunks = sum(
        1
        for chunk in all_chunks
        if chunk["scope"] == "National"
    )

    international_chunks = sum(
        1
        for chunk in all_chunks
        if chunk["scope"] == "International"
    )

    print(
        f"National chunks: {national_chunks}"
    )

    print(
        f"International chunks: {international_chunks}"
    )

    return all_chunks


if __name__ == "__main__":

    chunks = create_chunks()

    for chunk in chunks[:5]:

        print("\n--------------------")

        print(
            "Source:",
            chunk["source"]
        )

        print(
            "Scope:",
            chunk["scope"]
        )

        print(
            "Category:",
            chunk["category"]
        )

        print(
            "Page:",
            chunk["page"]
        )

        print(
            "Chunk:",
            chunk["chunk"]
        )

        print(
            "Text:",
            chunk["text"][:500]
        )
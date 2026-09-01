from pathlib import Path
from pypdf import PdfReader


# Project data folder
DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def get_scope(pdf_file: Path) -> str:
    """
    Determine whether the PDF belongs to National or International
    based on its folder.
    """

    relative_path = pdf_file.relative_to(DATA_DIR)

    parts = [part.lower() for part in relative_path.parts]

    if "national" in parts:
        return "National"

    if "international" in parts:
        return "International"

    return "Other"


def load_documents():
    documents = []

    if not DATA_DIR.exists():
        print(f"Data folder not found: {DATA_DIR}")
        return documents

    for pdf_file in DATA_DIR.rglob("*.pdf"):

        try:
            reader = PdfReader(str(pdf_file))

            # Path relative to data/
            relative_path = pdf_file.relative_to(DATA_DIR)

            # National / International
            scope = get_scope(pdf_file)

            for page_number, page in enumerate(
                reader.pages,
                start=1
            ):

                text = page.extract_text() or ""

                if text.strip():

                    documents.append({
                        "text": text,

                        # Keep complete relative path
                        "source": str(relative_path).replace("\\", "/"),

                        # Scope used for filtering
                        "scope": scope,

                        # Immediate folder
                        "category": pdf_file.parent.name,

                        "page": page_number
                    })

        except Exception as e:

            print(
                f"Error reading {pdf_file}: {e}"
            )

    print(f"Loaded {len(documents)} pages.")

    # Show scope counts
    national_count = sum(
        1 for doc in documents
        if doc["scope"] == "National"
    )

    international_count = sum(
        1 for doc in documents
        if doc["scope"] == "International"
    )

    print(f"National pages: {national_count}")
    print(f"International pages: {international_count}")

    return documents


if __name__ == "__main__":

    docs = load_documents()

    for doc in docs[:5]:

        print("\n---")
        print("Source:", doc["source"])
        print("Scope:", doc["scope"])
        print("Category:", doc["category"])
        print("Page:", doc["page"])
        print(doc["text"][:300])
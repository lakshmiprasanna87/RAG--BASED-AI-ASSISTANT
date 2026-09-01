from sentence_transformers import SentenceTransformer


# Multilingual embedding model
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

model = SentenceTransformer(MODEL_NAME)


def create_embeddings(texts):
    """
    Convert a list of text chunks into numerical vectors.
    """

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    return embeddings


if __name__ == "__main__":

    sample_texts = [
        "How can I register a trademark?",
        "ట్రేడ్‌మార్క్‌ను ఎలా నమోదు చేయాలి?"
    ]

    embeddings = create_embeddings(sample_texts)

    print("Number of texts:", len(sample_texts))
    print("Embedding shape:", embeddings.shape)
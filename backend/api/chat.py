from fastapi import APIRouter
from pydantic import BaseModel

from backend.rag.retriever import search_documents
from backend.llm.generator import generate_answer


router = APIRouter()


# ============================================================
# REQUEST MODEL
# ============================================================

class ChatRequest(BaseModel):

    question: str

    language: str = "English"

    scope: str = "National"


# ============================================================
# CHAT API
# ============================================================

@router.post("/chat")
def chat(request: ChatRequest):

    # --------------------------------------------------------
    # Clean scope
    # --------------------------------------------------------

    scope = request.scope.strip().title()

    # --------------------------------------------------------
    # Validate scope
    # --------------------------------------------------------

    if scope not in [
        "National",
        "International"
    ]:

        return {
            "error": (
                "Invalid scope. "
                "Use 'National' or 'International'."
            )
        }

    # --------------------------------------------------------
    # STEP 1
    # Search ONLY selected knowledge base
    # --------------------------------------------------------

    retrieved_documents = search_documents(
        question=request.question,
        top_k=5,
        scope=scope
    )

    # --------------------------------------------------------
    # STEP 2
    # Generate answer
    # --------------------------------------------------------

    result = generate_answer(
        request.question,
        retrieved_documents,
        request.language
    )

    # --------------------------------------------------------
    # STEP 3
    # Return response
    # --------------------------------------------------------

    return {
        "question": request.question,
        "language": request.language,
        "scope": scope,
        "answer": result["answer"],
        "sources": result["sources"]
    }
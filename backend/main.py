from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.chat import router as chat_router


app = FastAPI(
    title="Multilingual IP & Regulatory AI Assistant",
    description="RAG-based AI assistant for IP and regulatory guidance",
    version="1.0.0"
)


# Allow the React frontend to communicate with the backend

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Connect the chat API
app.include_router(
    chat_router,
    prefix="/api"
)


@app.get("/")
def home():
    return {
        "message": "Multilingual IP RAG Assistant is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }